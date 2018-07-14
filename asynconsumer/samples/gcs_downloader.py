import asyncio

from asynconsumer.core import async_run
from . import to_md5


def fetch_gcs_objects(uris, directory, naming=None, concurrency=3, sleep=0):
    """GCSから取得したオブジェクトをdirectoryに取得し、そのファイルパスを返す。

    :param uris: uriの一覧
    :param directory: オブジェクトを格納するディレクトリのパス
    :param naming: uriを引数に取り、ファイル名を返すCallableオブジェクト。デフォルトはmd5化。
    :param concurrency: 並列実行の最大数。デフォルトは3。
    :param sleep: スリープ時間（秒）。デフォルトは0。
    :return: 渡したurisと同潤のファイルパスの一覧。取得できない場合はファイルパスはNoneにする。
    """
    from google.cloud import storage

    client = storage.Client()
    loop = asyncio.get_event_loop()
    naming = naming or to_md5

    async def _fetch(uri):
        local_path = directory + '/' + naming(uri)
        try:
            params = [client, uri, local_path]
            filename = await loop.run_in_executor(None, _get_gcs_object, *params)
        except Exception:
            filename = None
        return filename

    return async_run(uris, _fetch, concurrency=concurrency, sleep=sleep)


def _get_gcs_object(client, uri, filename):
    try:
        bucket_name, blob_name = uri[5:].split('/', 1)
        data = client.bucket(bucket_name).get_blob(blob_name)
    except Exception as e:
        raise e
    if not data:
        return None
    data.download_to_filename(filename)
    return filename
