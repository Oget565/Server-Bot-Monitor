import asyncio
from app.services.clock import Clock
from app.database.database import save_to_db
import psutil
p = psutil

class Resources:
    def __init__(self):
        pass

    async def get_resources(self):
        self.mem_total = round(p.virtual_memory()[0] / (1024**3), 2)
        self.mem_used = round(p.virtual_memory()[3] / (1024**3), 2)
        self.mem_prcnt = p.virtual_memory()[2]

        self.cpu_prcnt = p.cpu_percent()
        self.cpu_freq = round(p.cpu_freq()[0] / 1000, 1)

        temps = psutil.sensors_temperatures()
        self.cpu_temp = None
        if temps:
            cpu_keys = ['coretemp', 'cpu_thermal', 'k10temp']
            for key in cpu_keys:
                if key in temps:
                    cores = temps[key]
                    self.cpu_temp = round(sum([c.current for c in cores]) / len(cores), 1)
                    break

    def pack_resources(self):
        resources = {
            'mem_total': self.mem_total,
            'mem_used': self.mem_used,
            'mem_prcnt': self.mem_prcnt,
            'cpu_prcnt': self.cpu_prcnt,
            'cpu_freq': self.cpu_freq,
            'cpu_temp': self.cpu_temp
        }

        return resources

async def wait_for_clock():
    clock = Clock()
    asyncio.create_task(clock.five_min_clock())

    res = Resources()

    while True:
        await Clock.clock_event.wait()
        Clock.clock_event.clear()  # Clear the event after processing
        await res.get_resources()
        data = res.pack_resources()
        await save_to_db(data)
        print("saved")