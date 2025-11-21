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

    async def pack_resources(self):
        resources = {
            'mem_total': self.mem_total,
            'mem_used': self.mem_used,
            'mem_prcnt': self.mem_prcnt,
            'cpu_prcnt': self.cpu_prcnt,
            'cpu_freq': self.cpu_freq,
            'cpu_temp': self.cpu_temp
        }

        return resources