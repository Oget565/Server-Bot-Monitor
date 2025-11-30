import asyncio
import datetime
from zoneinfo import ZoneInfo

class Clock:
    five_min_event = asyncio.Event()
    daily_event = asyncio.Event()

    async def five_min_clock(self):
        while True:
            self.five_min_event.set()
            await asyncio.sleep(1)
            self.five_min_event.clear()
            await asyncio.sleep(20)
            print("Five minute clock triggered")

    async def day_cycle_clock(self):
        tz = ZoneInfo("America/New_York")
        while True:
            now = datetime.datetime.now(tz)
            print(now)
            wakeup = now.replace(hour=8, minute=00, second=0, microsecond=0)

            if now >= wakeup:
                wakeup += datetime.timedelta(days=1)
                print("Wakeup delayed")

            time_left = (wakeup - now).total_seconds()
            await asyncio.sleep(time_left)

            self.daily_event.set()
            print("Wakeup triggered")
            await asyncio.sleep(5)
            self.daily_event.clear()
