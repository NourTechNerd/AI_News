import asyncio
import time 


async def fetch_data(delay):
    print("Fetching...")
    await asyncio.sleep(delay)
    print("Data Fetched")
    return "{data : 'abcd'}"
    
async def main():
    print("Start of main coroutine")
    fetch = fetch_data(2) # We just create the Coroutine object here we don't await it.
    print("End of main Coroutine")
    result = await fetch
    print("Received data :",{result})

#asyncio.run(main())


async def fetch_data1(id ,delay):
    print(f"Fetching by Couroutine {id}...")
    await asyncio.sleep(delay)
    print(f"Data Fetched by Couroutine {id}")
    return f" aabbabbaa{id}"

async def main1():
    
    start_time = time.time()
    task1 = asyncio.create_task(fetch_data1(1, 2)) # Coroutine/awaitble Object
    task2 = asyncio.create_task(fetch_data1(2, 2))
    task3 = asyncio.create_task(fetch_data1(3, 2))
   
    result1 = await task1
    result2 = await task2 
    result3 = await task3
    
    # We create a new Coroutine object here Will not be executed until the previous coroutines are completed.
    
    end_time = time.time()
    print("Time taken for coroutines to complete is :",end_time-start_time)
    print("Received data :",{result1},{result2},{result3})
    #print("Time taken for coroutines to complete is :",end_time-Start_time)
    

#asyncio.run(main1())


async def Loop():
    s = 0
    print("Start of loop")
    while s < 100000:
        #print(s)
        s += 1
        await asyncio.sleep(0.1)
    print("End of loop")
    return s

        
async def main2():
    start_time = time.time()
    
    # Run tasks concurrently and wait for all to complete
    result1, result2,sum,result3 = await asyncio.gather(
        fetch_data1(1, 2),
        fetch_data1(2, 2),
        Loop(),
        fetch_data1(3, 2),
    )
    

    
    end_time = time.time()
    
    print("Received data:", result1, result2, result3,sum)
    print(f"Execution time: {end_time - start_time:.4f} seconds")


asyncio.run(main2())