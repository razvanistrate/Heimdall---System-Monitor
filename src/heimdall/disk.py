import psutil
import platform

def get_disks():
    disks = []

    for partition in psutil.partitions(all=False):
        if platform.system() != 'Windows':
            skip_types = {'tmpfs', 'devtmpfs', 'squashfs', 'overlay', 'devfs'}

            if partition.fstype in skip_types:
                continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

          disks.append({
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'fstype': partition.fstype,
            'total_gb': usage.total / (1024 ** 3),
            'used_gb': usage.used / (1024 ** 3),
            'free_gb': usage.free / (1024 ** 3),
            'percent': usage.percent,
        })
return disks



