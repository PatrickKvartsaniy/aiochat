import asyncio

async def foo():
    print("Foo start")
    await asyncio.sleep(1)
    print("Foo finish")

async def bar():
    print("Bar start")
    await asyncio.sleep(1)
    print("Bar finish")

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(foo()),
    loop.create_task(bar())
]

loop.run_until_complete(asyncio.wait(tasks))
