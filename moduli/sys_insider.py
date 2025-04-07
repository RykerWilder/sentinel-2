import platform
import socket
import psutil
import requests
import shutil
from colorama import Style, Fore


def print_dynamic_dots(label, value, width=40):
    """
    Print a label and value with dots in between for alignment.

    Args:
        label: The label to print
        value: The value to print
        width: The width to align the value at
    """
    dots = "." * (width - len(label))
    print(f"{label} {dots} {value}")


class SysInsider:

    def get_public_ip(self):
        try:
            return requests.get("https://api.ipify.org?format=json").json().get("ip", "not available")
        except:
            return "Not available"

    def get_os_details(self):
        system = platform.system()
        details = {
            "system": system,
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "machine": platform.machine()
        }

        if system == "Darwin":
            details["version"] = f"macOS {platform.mac_ver()[0]}"
        elif system == "Windows":
            details["version"] = f"Windows {platform.release()}"
        elif system == "Linux":
            details["version"] = f"Linux {platform.release()}"

        return details

    def get_cpu_info(self):
        return {
            "name": platform.processor(),
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "usage": psutil.cpu_percent(interval=1)
        }

    def get_ram_info(self):
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024 ** 3), 2),
            "available": round(mem.available / (1024 ** 3), 2),
            "used": round(mem.used / (1024 ** 3), 2),
            "percent": mem.percent
        }

    def get_disk_usage(self):
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total": round(usage.total / (1024 ** 3), 2),
                    "used": round(usage.used / (1024 ** 3), 2),
                    "free": round(usage.free / (1024 ** 3), 2),
                    "percent": usage.percent
                })
            except:
                continue
        return disks

    def get_network_info(self):
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        return {
            "interfaces": {
                name: {
                    "addresses": [addr.address for addr in addrs if addr.family == socket.AF_INET],
                    "is_up": stats[name].isup if name in stats else False
                } for name, addrs in interfaces.items()
            }
        }

    def get_battery_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged
                }
            return "Not available"
        except:
            return "Not available"

    def print_system_info(self):
        terminal_width = shutil.get_terminal_size().columns
        print(f"\n{'='*40}{Fore.GREEN} SysInsider {Style.RESET_ALL}{'='*40}")

        # OS Information
        os_details = self.get_os_details()
        print_dynamic_dots('OS', f"{os_details['version']} ({os_details['architecture']})")
        print_dynamic_dots('Hostname', socket.gethostname())

        # Hardware Information
        cpu = self.get_cpu_info()
        print_dynamic_dots('CPU', f"{cpu['name']} ({cpu['cores']} cores, {cpu['threads']} threads) - {cpu['usage']}% usage")

        ram = self.get_ram_info()
        print_dynamic_dots('RAM', f"{ram['total']} GB total, {ram['used']} GB used ({ram['percent']}%)")

        # Network Information
        print("Network:")
        print_dynamic_dots('  Public IP', self.get_public_ip())
        network_info = self.get_network_info()
        for name, data in network_info.get("interfaces", {}).items():
            if data.get("is_up", False) and data.get("addresses", []):
                print_dynamic_dots(f"  {name}", f"{', '.join(data['addresses'])}")

        # Storage Information
        print("Storage:")
        for disk in self.get_disk_usage():
            print(f"  {disk['device']} ({disk['mountpoint']}):")
            print(f"    Total: {disk['total']} GB, Used: {disk['used']} GB ({disk['percent']}%)")
        print("=" * terminal_width + "\n")

if __name__ == "__main__":
            system_info = SysInsider()
            system_info.print_system_info()
