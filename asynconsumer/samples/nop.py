import asyncio

from asynconsumer.core import async_run


def nop(targets):
    async def coro(target):
        print('start: {}'.format(target))
        await asyncio.sleep(1)
        print('end: {}'.format(target))
        return target.upper()

    return async_run(targets, coro, concurrency=2)


def nop_2(targets):
    def heavy_synchronous_process(target):
        print('processing: {}'.format(target))
        return target.upper()

    loop = asyncio.get_event_loop()

    async def coro(target):
        params = [target]
        result = await loop.run_in_executor(None, heavy_synchronous_process, *params)
        return result

    return async_run(targets, coro, concurrency=2)
