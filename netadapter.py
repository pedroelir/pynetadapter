import subprocess
import time


def enable_netadapter(adapter_name: str) -> bool:
    cmd: list[str] = ["powershell.exe", f"Enable-NetAdapter -Name {adapter_name} ; exit -not ($?)"]
    process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if bool(process.returncode == 0):
        return True
    print(process.stdout)
    print(process.stderr)
    return False


def disable_netadapter(adapter_name: str) -> bool:
    cmd: list[str] = ["powershell.exe", f"Disable-NetAdapter -Name {adapter_name} -Confirm:$False; exit -not ($?)"]
    process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if bool(process.returncode == 0):
        return True
    print(process.stdout)
    print(process.stderr)
    return False


if __name__ == "__main__":
    if disable_netadapter("Ethernet"):
        print("Adapter disabled")
    else:
        print("Adapter not disabled")

    time.sleep(10)
    if enable_netadapter("Ethernet"):
        print("Adapter enabled")
    else:
        print("Adapter not enabled")
