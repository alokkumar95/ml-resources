import requests
import json
import asyncio
import httpx
import time

# https://github.com/ejaj/rest-api-intermediate/blob/main/number_of_drawn_matches.py
# to_read - https://klaviyo.tech/a-deep-dive-into-high-performance-http-requests-for-python-engineers-2546772c50ae
# https://realpython.com/async-io-python/
# https://oxylabs.io/blog/httpx-vs-requests-vs-aiohttp

def get_number_of_drawn_matches(year):
    url = f"https://jsonmock.hackerrank.com/api/football_matches?year={year}"

    total_drawn_matches = 0

    # assume goal would be in 0,1,2, ..., 11,12
    for goal in range(12):
        try:
            r = requests.get(url + f"&team1goals={goal}&team2goals={goal}")
            res = r.json()
            total_drawn_matches += res['total']
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    return total_drawn_matches

start = time.perf_counter()
print("total: ", get_number_of_drawn_matches(2011))
print("Total time", time.perf_counter()  - start)


def getNumDraws(year):
    url = "https://jsonmock.hackerrank.com/api/football_matches?year=" + str(year)
    response = requests.get(url)
    result = json.loads(response.content)
    current_page = 1
    total_page_url = result['total_pages']
    total = 0
    for i in range(0, 12):
        url = "https://jsonmock.hackerrank.com/api/football_matches?year={0}&team1goals={1}&team2goals={1}".format(
            year, i, i)
        response = requests.get(url)
        result = json.loads(response.content)
        total += result['total']

    print(total)
# getNumDraws(2011)

# since requests is synchronous and blocks the entire event loop
# use asyncio to make the requests asynchronous and non-blocking
# and faster

async def fetch_drawn_matches(year):
    # Use AsyncClient for non-blocking HTTP requests
    total_drawn_matches = 0

    async with httpx.AsyncClient() as client:
        for goal in range(12):
            r = await client.get(f"https://jsonmock.hackerrank.com/api/football_matches?year={year}&team1goals={goal}&team2goals={goal}")
            data = r.json()
            total_drawn_matches += data['total']
            # print("--",data)
    # print(f"Total drawn matches in {year}: {total_drawn_matches}")
# asyncio.run(fetch_drawn_matches(2011))

# Each request waits for the previous one to finish before starting the next, so the timeline looks like:

# Request 1 ------>
#                 Request 2 ------>
#                                Request 3 ------>
# ...

# The advantage of asyncio comes when you run the requests concurrently.

# fetch_goal coroutine
async def fetch_goal(client, year, goal):
    r = await client.get(f"https://jsonmock.hackerrank.com/api/football_matches?year={year}&team1goals={goal}&team2goals={goal}")
    return r.json()['total']

async def fetch_drawn_matches_concurrent(year):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_goal(client, year, goal) for goal in range(12)]

        results = await asyncio.gather(*tasks)

        print("results--",results)
        return sum(results)

start_time = time.perf_counter()
print("---",asyncio.run(fetch_drawn_matches_concurrent(2011)))
print(time.perf_counter() - start_time)

# Now the requests are started together:
# Times roughly = max(request_times) instead of sum(request_times)
# Request 1 ------>
# Request 2 ------->
# Request 3 -------->
# ...

# what is coroutine
# async def fetch(goal):
#     ...

# Calling it doesn't execute it immediately.
# coro = fetch(2)

# print(coro) # <coroutine object fetch at 0x...>

# await fetch(0)
# await fetch(1)
# await fetch(2)

# fetch(0) finishes
#       ↓
# fetch(1) finishes
#       ↓
# fetch(2) finishes

# So although it's asynchronous, it's still one after another.

#***************** A Task is a coroutine that has been scheduled to run by the event loop.*********************

# task = asyncio.create_task(fetch(0))

# Now fetch(0) starts running in the background.

# task1 = asyncio.create_task(fetch(0))
# task2 = asyncio.create_task(fetch(1))
# task3 = asyncio.create_task(fetch(2))

# Now all three are running concurrently.

# Imagine three people downloading three files instead of one person downloading them one at a time.

# What does gather() do?

# suppose you have three coroutines

# fetch(0)
# fetch(1)
# fetch(2)

# you can tell asyncio

# results = await asyncio.gather(
#     fetch(0),
#     fetch(1),
#     fetch(2)
# )

# gather():

# starts them all
# waits until all are finished
# returns their results in order

# results = [5, 8, 2]