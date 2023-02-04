import subprocess


def enable_netadapter(adapter_name: str) -> bool:
    cmd: list[str] = ["powershell.exe", f"Enable-NetAdapter -Name{adapter_name} ; exit -not ($?)"]
    process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return bool(process.returncode == 0)


def disable_netadapter(adapter_name: str) -> bool:
    cmd: list[str] = ["powershell.exe", f"Disable-NetAdapter -Name{adapter_name} ; exit -not ($?)"]
    process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return bool(process.returncode == 0)


if __name__ == "__main":
    disable_netadapter("Ethernet")
    enable_netadapter("Ethernet")
