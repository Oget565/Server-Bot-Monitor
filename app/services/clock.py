import asyncio

class Clock:
    clock_event = asyncio.Event()

    async def five_min_clock(self):
        while True:
            self.clock_event.set()
            await asyncio.sleep(0)
            self.clock_event.clear()
            await asyncio.sleep(300)
