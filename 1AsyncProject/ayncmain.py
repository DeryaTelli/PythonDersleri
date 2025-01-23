import asyncio
#async ifadesi fonksiyonun asenkron calistirilicagini belirtiyor

async def func1():
    print("1. function start")
    await asyncio.sleep(5) #non blocking delay simulasyonu 5 saniye beklicek ama digerlerini etkilememesini saglicak
    print("1. function end")
    return 5


async def func2():
    print("2. function start")
    await asyncio.sleep(5)
    print("2. function end")
    return 10

async def main():
    task1=asyncio.create_task(func1())
    task2 = asyncio.create_task(func2())
    x= await task1
    y=await task2
    print(x)
    print(y)

if __name__ =="__main__":
    asyncio.run(main())
