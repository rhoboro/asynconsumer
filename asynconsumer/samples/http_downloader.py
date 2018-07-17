import logging

from asynconsumer.core import async_run
from . import to_md5

logger = logging.getLogger(__name__)


def fetch_http_resources(urls, directory, naming=None, timeout=10, concurrency=3, sleep=0.5):
    """HTTPリソースをdirectoryに取得し、そのファイルパスを返す。

    :param urls: urlの一覧
    :param directory: オブジェクトを格納するディレクトリのパス
    :param naming: urlを引数に取り、ファイル名を返すCallableオブジェクト。デフォルトはmd5化。
    :param timeout: タイムアウト時間（秒）。
    :param concurrency: 並列実行の最大数。デフォルトは3。
    :param sleep: スリープ時間（秒）。デフォルトは0.5。
    :return: 渡したurisと同潤のファイルパスの一覧。取得できない場合はファイルパスはNoneにする。
    """
    import aiohttp
    import async_timeout

    naming = naming or to_md5

    async def _fetch(url):
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(timeout):
                try:
                    head = await session.head(url)
                    if head and 200 <= head.status < 300:
                        response = await session.get(url)
                        if response and not (200 <= response.status < 300):
                            if response.status != 404:
                                logger.info(
                                    'can not get some data: {} {}'.format(url, response.status))
                            response = None
                    else:
                        response = None
                except Exception as e:
                    logger.info('can not get some data: {} {}'.format(url, e))
                    response = None

            local_path = directory + '/' + naming(url)
            if response:
                with open(local_path, 'wb') as f:
                    f.write(await response.read())
            return local_path if response else None

    return async_run(urls, _fetch, concurrency=concurrency, sleep=sleep)
