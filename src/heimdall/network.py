import psutil
import platform

EXCLUDED_PREFIXES = (
    "lo", "utun", "awdl", "llw", "gif", "stf", "anpi", "bridge", "ap", "tun", "tap", "wg", 
    "tailscale", "docker", "veth", "virbr", "vbox", "vmnet", "vmx", "hyperv", "vEthernet",
    "istap", "teredo",
)

EXCLUDED_EXACT = (
    "tailscale0", "lo0", "dummy0",
)


def get_network():
    net = psutil.net_io_counters(pernic=True)
    stats = psutil.net_if_stats()
    system = platform.system()

    best = None 
    best_trafic = -1

    for name, data in net.items():
        if any(name.startswith(p) for p in EXCLUDED_PREFIXES):
            continue

        if name in EXCLUDED_EXACT:
            continue

        info = stats.get(name)
        if info is None or not info.isup:
            continue

#        if system != ('Darwin', 'Linux') and info.speed == 0:
#            continue

        total_trafic = data.bytes_sent + data.bytes_recv

        if total_trafic > best_trafic:
            best_trafic = total_trafic
            best = (name, data, info)

            if best is None:
                return None

    name, data, info = best
    return {
        "name": name,
        "sent": data.bytes_sent,
        "recv": data.bytes_recv,
        "speed": info.speed,
    }


