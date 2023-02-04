import subprocess
import time


class NetAdapter:
    @staticmethod
    def enable_netadapter(adapter_name: str) -> bool:
        cmd: list[str] = ["powershell.exe", f"Enable-NetAdapter -Name {adapter_name} ; exit -not ($?)"]
        process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if bool(process.returncode == 0):
            return True
        print(process.stdout)
        print(process.stderr)
        return False

    @staticmethod
    def disable_netadapter(adapter_name: str) -> bool:
        cmd: list[str] = ["powershell.exe", f"Disable-NetAdapter -Name {adapter_name} -Confirm:$False; exit -not ($?)"]
        process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if bool(process.returncode == 0):
            return True
        print(process.stdout)
        print(process.stderr)
        return False

    @staticmethod
    def get_netadapters():
        cmd: list[str] = ["powershell.exe", "(Get-NetAdapter).Name; exit -not ($?)"]
        process: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if bool(process.returncode == 0):
            print(process.stdout)
            adapters = process.stdout.split("\n")
            adapters.pop()
            return adapters
        print(process.stdout)
        print(process.stderr)
        return []

    @staticmethod
    def get_adapter_status(adpter_name: str):
        cmd: list[str] = ["powershell.exe", f'(Get-NetAdapter | Where-Object {{$_.Name -eq "{adpter_name}"}}).Status']
        output: str = subprocess.check_output(cmd, text=True, timeout=10)
        if not output:
            raise AttributeError(f"The Adapter {adpter_name} has no status attribute, ensure that the adapter exists")
        return output.strip()


if __name__ == "__main__":
    # if disable_netadapter("Ethernet"):
    #     print("Adapter disabled")
    # else:
    #     print("Adapter not disabled")

    # time.sleep(10)
    # if enable_netadapter("Ethernet"):
    #     print("Adapter enabled")
    # else:
    #     print("Adapter not enabled")
    adapters = NetAdapter.get_netadapters()
    print(adapters)

    print(NetAdapter.get_adapter_status("Ethernet"))
