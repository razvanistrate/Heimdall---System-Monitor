import os
import psutil
import platform

def get_processes():
    processes = []

    if platform.system() == "Linux":

        for pid in os.listdir("/proc"):
            if pid.isdigit():
                try:
                    with open(f"/proc/{pid}/comm") as f:
                        name = f.read().strip()
                    processes.append((int(pid), name))
                except:
                    continue
        return processes

    elif platform.system() == "Windows":
        for p in psutil.process_iter(['pid', 'name']):
            processes.append((p.info['pid'], p.info['name']))
        return processes
    
    elif platform.system() == "Darwin":
        for p in psutil.process_iter(['pid', 'name']):
            processes.append((p.info['pid'], p.info['name']))
        return processes
    
