import asyncio
def decor(func):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper
@decor
async def async_func():
    await asyncio.sleep(1)
    print("All good!")
async def main():
    await async_func()
    print("All good!??")
    await async_func()
    print("All good!__")
    await async_func()
    print("All good!+++")
    await async_func()
asyncio.run(main())
