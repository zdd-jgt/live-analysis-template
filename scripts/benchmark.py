import asyncio
import httpx
from datetime import datetime

async def simulate_danmu_load(url: str, qps: int, duration: int):
    """模拟弹幕压力测试"""
    success = 0
    fail = 0

    async def send_request():
        nonlocal success, fail
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{url}/api/v1/danmu/analyze",
                    json={"text": "测试弹幕" * 10}
                )
                if resp.status_code == 200:
                    success += 1
                else:
                    fail += 1
        except Exception:
            fail += 1

    start = datetime.now()
    tasks = []

    # 创建持续负载
    while (datetime.now() - start).total_seconds() < duration:
        for _ in range(qps):
            tasks.append(asyncio.create_task(send_request()))
        await asyncio.sleep(1)

    await asyncio.gather(*tasks)

    print(f"Total: {success + fail} | Success: {success} | Fail: {fail}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--qps", type=int, default=1000)
    parser.add_argument("--duration", type=int, default=60)

    args = parser.parse_args()

    asyncio.run(simulate_danmu_load(args.url, args.qps, args.duration))
