import platform
import psutil
import subprocess

system = platform.system()

def get_cpu():

    if system == "Linux":
        cpu_name = 0
        cpu_core = 0
        threads = 0

        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if not line.strip():
                    continue

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key == "model name" and not cpu_name:
                    cpu_name = value

                elif key == "cpu cores" and cpu_core == 0:
                    cpu_core = int(value)

                elif key == "processor":
                    threads += 1

        return {"name": cpu_name, "cores": cpu_core, "threads": threads}

    elif system == "Windows":
        import winreg


        
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        value, _ = winreg.QueryValueEx(key, "ProcessorNameString")
        cpu_name = value
        cpu_cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True) 
        return {
                "name": cpu_name,
                "cores": cpu_cores,
                "threads": threads
                }