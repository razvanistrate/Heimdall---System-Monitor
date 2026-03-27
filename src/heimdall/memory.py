import psutil

def get_memory():
    mem = psutil.virtual_memory()

    return {
        "total_mb": mem.total / 1024 / 1024,
        "used_mb": mem.used / 1024 / 1024,
        "used_percent": mem.percent
    }