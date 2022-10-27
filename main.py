import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.driver import drive


async def async_drive():
    print("\n\nStarting loop again\n\n")
    drive()

loop = asyncio.get_event_loop()
loop.run_until_complete(async_drive())

scheduler = AsyncIOScheduler(timezone="UTC", daemon=True)
scheduler.add_job(async_drive, "interval", seconds=84_000)  # 24 hours
scheduler.start()

asyncio.get_event_loop().run_forever()
