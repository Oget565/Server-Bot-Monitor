import asyncio
import datetime
from zoneinfo import ZoneInfo
from app.settings.read_write_settings import Settings

sett = Settings()

class Clock:
    five_min_event = asyncio.Event()
    daily_event = asyncio.Event()

    async def five_min_clock(self):
        while True:
            self.five_min_event.set()
            await asyncio.sleep(1)
            self.five_min_event.clear()

            sleep_time = int(sett.read_settings("update_interval")) * 60
            await asyncio.sleep(sleep_time)
            print("Five minute clock triggered")

    async def day_cycle_clock(self):
        while True:
            tz = ZoneInfo(sett.read_settings("timezone"))
            now = datetime.datetime.now(tz)
            print(now)

            time = sett.read_settings("notification_time")
            hour, minute = time.split(":")

            wakeup = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

            if now >= wakeup:
                wakeup += datetime.timedelta(days=1)
                print("Wakeup delayed")

            time_left = (wakeup - now).total_seconds()
            await asyncio.sleep(time_left)

            self.daily_event.set()
            print("Wakeup triggered")
            await asyncio.sleep(5)
            self.daily_event.clear()