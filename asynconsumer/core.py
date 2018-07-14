import asyncio
import itertools
import logging

logger = logging.getLogger(__name__)


async def _bound_coro(target,
                      coro,
                      semaphore,
                      sleep):
    """排他処理を行いながら非同期で処理を実行する

    :param urls: 処理対象一覧
    :param coro: 処理内容を記述したコルーチン
    :param semaphore: セマフォ。
    :param sleep: スリープ時間（秒）。
    :return: coroの戻り値
    """
    async with semaphore:
        await asyncio.sleep(sleep)
        return await coro(target)


async def _run(targets,
               coro,
               concurrency,
               sleep):
    """リストに対して非同期処理を行う

    :param urls: 処理対象一覧
    :param coro: 処理内容を記述したコルーチン
    :param concurrency: 並列実行の最大数。デフォルトは1。
    :param sleep: スリープ時間（秒）。
    :return: coroの戻り値
    """
    responses = []
    semaphore = asyncio.Semaphore(concurrency)
    for chunk in get_chunk(targets, n=concurrency * 10):
        tasks = (asyncio.ensure_future(_bound_coro(target, coro, semaphore, sleep))
                 for target in chunk)
        responses.extend(await asyncio.gather(*tasks))
        logger.info('{} targets are completed.'.format(len(responses)))
    return responses


def async_run(targets,
              coro,
              concurrency=1,
              sleep=0):
    """リストに対して非同期処理を行う

    :param urls: 処理対象一覧
    :param coro: 処理内容を記述したコルーチン
    :param concurrency: 並列実行の最大数。デフォルトは1。
    :param sleep: スリープ時間（秒）。
    :return: coroの戻り値の一覧。順番は保持される。
    """
    targets = targets or []
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(_run(targets, coro, concurrency, sleep))
    return results


def get_chunk(iterable, n=5):
    for i, item in itertools.groupby(enumerate(iterable), lambda x: x[0] // n):
        yield (x[1] for x in item)
