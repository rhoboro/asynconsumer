# asynconsumer

asynconsumer is a simple library for processing each items within iterable using asyncio.

## How to install

```sh
$ pip3 install asynconsumer
```

## Quick start

1. Define a function or a coroutine function which takes one argument.
2. Now, call `async_run(iterable, function)` and you can get list which each items was applied with the function.  
`concurrency` is an optional parameter can changes number of concurrently executed coroutines(default: 1).


### Examples

`coro` in the following code is a coroutine function that convert a word passed as an argument to an upper case.  
So, `async_run(['ham', 'egg', 'spam'], coro, concurrency=2)` will return `['HAM', 'EGG', 'SPAM']`.

```python
>>> from asynconsumer.core import async_run
>>> import asyncio
>>> async def coro(target):
...   print('start: {}'.format(target))
...   await asyncio.sleep(1)
...   print('end: {}'.format(target))
...   return target.upper()
...
>>> results = async_run(['ham', 'egg', 'spam'], coro, concurrency=2)
start: ham
start: egg
end: ham
end: egg
start: spam
end: spam
>>> results
['HAM', 'EGG', 'SPAM']
>>>
```

You can also pass the normal functions.

```python
>>> from asynconsumer.core import async_run
>>> import time
>>> def func(target):
...   print('start: {}'.format(target))
...   time.sleep(1)
...   print('end: {}'.format(target))
...   return target.upper()
...
>>> results = async_run(['ham', 'egg', 'spam'], func, concurrency=2)
start: ham
start: egg
end: ham
end: egg
start: spam
end: spam
>>> results
['HAM', 'EGG', 'SPAM']
>>>
```

## More samples.

Sample codes are put in [asynconsumer/samples](./asynconsumer/samples).

### [Concurrent get HTTP resources](./asynconsumer/samples/http_downloader.py)

```python
$ pip3 install aiohttp
$ python3 -q
>>> from asynconsumer import fetch_http_resources
>>> urls = ['https://avatars3.githubusercontent.com/u/13819005?s=460&v=4']
>>> fetch_http_resources(urls, '.')
['./8ee20d7c992fee4ac009f4d33c13e276']
>>>
>>> fetch_http_resources(urls=urls, directory='.', naming=lambda url: 'image_{}.jpg'.format(urls.index(url)))
['./image_0.jpg']
```

### [Concurrent get GCS objects](./asynconsumer/samples/gcs_downloader.py)

```python
$ pip3 install google-cloud-storage
$ python3 -q
>>> from asynconsumer import fetch_gcs_objects
>>> uris = ['gs://...']
>>> fetch_gcs_objects(uris, '.')
['./md5string']
>>>
>>> fetch_http_resources(uris, '.', naming=lambda uri: 'image_{}.jpg'.format(uris.index(uri)))
['./image_0.jpg']
```

