# asynconsumer

リストを受け取り、その各要素に並列で任意の処理を行うライブラリ

## インストール

```sh
$ pip install asynconsumer
```

## クイックスタート

### 任意の処理を書く

`async_run()`にリストとリストの要素を処理する任意のコルーチンを渡す。
[asynconsumer/samples](./asynconsumer/samples)ディレクトリにサンプルを置いています。


```python
>>> from asynconsumer.core import async_run
>>> import asyncio
# リストの要素を引数に取るコルーチン関数を定義する
>>> async def coro(target):
...   print('start: {}'.format(target))
...   await asyncio.sleep(1)
...   print('end: {}'.format(target))
...   # 戻り値のリストがasync_runの戻り値になる
...   return target.upper()
...
# 並列数を指定して実行
>>> results = async_run(['ham', 'egg', 'spam'], coro, concurrency=2)
start: ham
start: egg
end: ham
end: egg
start: spam
end: spam
>>>
>>> results
['HAM', 'EGG', 'SPAM']
>>>
```

## サンプル実装例

### [URLの一覧からHTTPリソースを取得する](./asynconsumer/samples/http_downloader.py)

```python
$ pip install aiohttp
$ python3 -q
>>> from asynconsumer import fetch_http_resources
>>> urls = ['https://avatars3.githubusercontent.com/u/13819005?s=460&v=4']
>>> fetch_http_resources(urls, '.')
['./8ee20d7c992fee4ac009f4d33c13e276']
>>>
>>> fetch_http_resources(urls=urls, directory='.', naming=lambda url: 'image_{}.jpg'.format(urls.index(url)))
['./image_0.jpg']
```

### [GCSのURI一覧からオブジェクトを取得する](./asynconsumer/samples/gcs_downloader.py)

```python
$ pip install google-cloud-storage
$ python3 -q
>>> from asynconsumer import fetch_gcs_object
>>> uris = ['gs://...']
>>> fetch_gcs_object(uris, '.')
['./md5string']
>>>
>>> fetch_http_resources(uris, '.', naming=lambda uri: 'image_{}.jpg'.format(uris.index(uri)))
['./image_0.jpg']
```
