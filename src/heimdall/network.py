import psutil
from psutil._common import bytes2human

def get_network():
    net = psutil.net_io_counters(pernic=True)
    stats = psutil.net_if_stats()

    for name, data in net.items():
        info = stats.get(name)

        if info and info.isup and info.speed > 0:
            return {
                "name": name,
                "sent": data.bytes_sent,
                "recv": data.bytes_recv,
                "speed": info.speed,
            }
    return None    