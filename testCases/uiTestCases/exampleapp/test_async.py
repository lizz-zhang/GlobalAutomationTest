import asyncio


async def task_1():
    print("Task 1: Start")
    await asyncio.sleep(1)  # Simulates an I/O operation
    print("Task 1: End")


async def task_2():
    print("Task 2: Start")
    await asyncio.sleep(1)  # Simulates an I/O operation
    print("Task 2: End")


async def main():
    await asyncio.gather(task_1(), task_2())


asyncio.run(main())
