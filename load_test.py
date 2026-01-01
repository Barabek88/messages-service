#!/usr/bin/env python3
"""
Load testing script for comparing Citus vs Tarantool performance
"""
import asyncio
import aiohttp
import time
import statistics
from uuid import uuid4

BASE_URL = "http://localhost:8001/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2NmOWNmMjQtODRiMy00YTQ2LTgzMWQtYzJiZjVkZTQ0ZWExIiwiZmlyc3RfbmFtZSI6Ik1ha3MyMjM0OTkiLCJzZWNvbmRfbmFtZSI6IkVybSIsImV4cCI6MTc2NjcwMzA1NH0.PeMR40Fs2cLUd2mv1L1TcJD3FY7Ft2bUjYUNoGZ-K_c"  # Replace with actual token
USER_ID = "017aa90c-b475-402e-a27e-1b7783a6cb88"
NUM_REQUESTS = 1000
CONCURRENT = 50


async def send_request(session, url, method="GET", json_data=None):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    start = time.time()
    try:
        if method == "POST":
            async with session.post(url, json=json_data, headers=headers) as resp:
                await resp.text()
                status = resp.status
        else:
            async with session.get(url, headers=headers) as resp:
                await resp.text()
                status = resp.status
        duration = time.time() - start
        return {"success": status == 200, "duration": duration}
    except Exception as e:
        return {"success": False, "duration": time.time() - start, "error": str(e)}


async def run_test(endpoint_prefix, test_name):
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")

    send_url = f"{BASE_URL}/{endpoint_prefix}/{USER_ID}/send"
    list_url = f"{BASE_URL}/{endpoint_prefix}/{USER_ID}/list"

    async with aiohttp.ClientSession() as session:
        # Test SEND
        # print(
        #     f"\n[SEND] Testing {NUM_REQUESTS} requests with {CONCURRENT} concurrent..."
        # )
        # send_results = []
        # start_time = time.time()

        # for i in range(0, NUM_REQUESTS, CONCURRENT):
        #     batch = min(CONCURRENT, NUM_REQUESTS - i)
        #     tasks = [
        #         send_request(session, send_url, "POST", {"text": f"Test message {i+j}"})
        #         for j in range(batch)
        #     ]
        #     results = await asyncio.gather(*tasks)
        #     send_results.extend(results)

        # send_duration = time.time() - start_time
        # send_durations = [r["duration"] for r in send_results if r["success"]]
        # send_failures = sum(1 for r in send_results if not r["success"])

        # print(f"Total time: {send_duration:.2f}s")
        # print(f"RPS: {NUM_REQUESTS/send_duration:.2f}")
        # print(f"Success: {len(send_durations)}/{NUM_REQUESTS}")
        # print(f"Failures: {send_failures}")
        # if send_durations:
        #     print(f"Avg latency: {statistics.mean(send_durations)*1000:.2f}ms")
        #     print(f"Min latency: {min(send_durations)*1000:.2f}ms")
        #     print(f"Max latency: {max(send_durations)*1000:.2f}ms")
        #     print(
        #         f"P95 latency: {statistics.quantiles(send_durations, n=20)[18]*1000:.2f}ms"
        #     )
        #     print(
        #         f"P99 latency: {statistics.quantiles(send_durations, n=100)[98]*1000:.2f}ms"
        #     )

        # Test LIST
        print(
            f"\n[LIST] Testing {NUM_REQUESTS} requests with {CONCURRENT} concurrent..."
        )
        list_results = []
        start_time = time.time()

        for i in range(0, NUM_REQUESTS, CONCURRENT):
            batch = min(CONCURRENT, NUM_REQUESTS - i)
            tasks = [send_request(session, list_url, "GET") for _ in range(batch)]
            results = await asyncio.gather(*tasks)
            list_results.extend(results)

        list_duration = time.time() - start_time
        list_durations = [r["duration"] for r in list_results if r["success"]]
        list_failures = sum(1 for r in list_results if not r["success"])

        print(f"Total time: {list_duration:.2f}s")
        print(f"RPS: {NUM_REQUESTS/list_duration:.2f}")
        print(f"Success: {len(list_durations)}/{NUM_REQUESTS}")
        print(f"Failures: {list_failures}")
        if list_durations:
            print(f"Avg latency: {statistics.mean(list_durations)*1000:.2f}ms")
            print(f"Min latency: {min(list_durations)*1000:.2f}ms")
            print(f"Max latency: {max(list_durations)*1000:.2f}ms")
            print(
                f"P95 latency: {statistics.quantiles(list_durations, n=20)[18]*1000:.2f}ms"
            )
            print(
                f"P99 latency: {statistics.quantiles(list_durations, n=100)[98]*1000:.2f}ms"
            )


async def main():
    print("Load Testing: Citus vs Tarantool")
    print(f"Requests: {NUM_REQUESTS}, Concurrent: {CONCURRENT}")

    # Test Citus
    await run_test("dialog", "Citus (PostgreSQL)")

    # Wait a bit
    await asyncio.sleep(2)

    # Test Tarantool
    await run_test("dialog-tarantool", "Tarantool (In-Memory)")

    print(f"\n{'='*60}")
    print("Testing completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
