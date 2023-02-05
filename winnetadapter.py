import subprocess
import time

from contextlib import contextmanager


class WinNetAdapter:
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
            adapters = process.stdout.casefold().split("\n")
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
        return output.casefold().strip()

    @staticmethod
    def disable_all_adapters():
        if not WinNetAdapter.disable_netadapter("*"):
            return False
        adapters = WinNetAdapter.get_netadapters()
        for adapter in adapters:
            if WinNetAdapter.get_adapter_status(adpter_name=adapter) != "disabled":
                return False
        return True

    @staticmethod
    def enable_all_adapters():
        if not WinNetAdapter.enable_netadapter("*"):
            return False
        adapters = WinNetAdapter.get_netadapters()
        for adapter in adapters:
            if WinNetAdapter.get_adapter_status(adpter_name=adapter) == "disabled":
                return False
        return True


@contextmanager
def ctx_disable_all_adapters():
    try:
        if not (WinNetAdapter.disable_netadapter("*")):
            raise ResourceWarning("Could not disable Adapters try runing as Admin")
        yield
    finally:
        WinNetAdapter.enable_netadapter("*")
        time.sleep(10)
        adapters = WinNetAdapter.get_netadapters()
        adapters_status = [WinNetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters]
        if "disabled" in adapters_status:
            raise ResourceWarning("Not all adapters were enabled")


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
    adapters = WinNetAdapter.get_netadapters()
    print(adapters)

    print(WinNetAdapter.get_adapter_status("Ethernet"))

    # with ctx_disable_all_adapters():
    #     print([WinNetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters])
    # print([WinNetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters])
    print(f"Disable all: {WinNetAdapter.disable_all_adapters()}")
    print(f"Enable all: {WinNetAdapter.enable_all_adapters()}")
