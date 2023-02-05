import os
import ctypes

import pytest
from winnetadapter import WinNetAdapter, ctx_disable_all_adapters


adapter_name = "Ethernet"
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()


def test_get_adapters():
    adpaters = WinNetAdapter.get_netadapters()
    assert adapter_name.casefold() in adpaters


@pytest.mark.xfail(not is_admin, reason="Will fail if not Admin")
def test_disable_adapter():
    assert WinNetAdapter.disable_netadapter(adapter_name=adapter_name)


def test_enable_adapter():
    assert WinNetAdapter.enable_netadapter(adapter_name=adapter_name)


def test_adapter_status():
    assert WinNetAdapter.get_adapter_status(adpter_name=adapter_name)


def test_bad_disable_adapter():
    assert not WinNetAdapter.disable_netadapter(adapter_name=adapter_name[:-2])


def test_bad_enable_adapter():
    assert not WinNetAdapter.enable_netadapter(adapter_name=adapter_name[:-2])


def test_bad_adapter_status():
    with pytest.raises(AttributeError):
        WinNetAdapter.get_adapter_status(adpter_name=adapter_name[:-2])


@pytest.mark.xfail(not is_admin, reason="Will fail if not Admin", raises=ResourceWarning, strict=True)
def test_ctx_diable_all():
    adapters = WinNetAdapter.get_netadapters()
    with ctx_disable_all_adapters():
        adapters_status: dict[str, str] = {
            adapter: WinNetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters
        }
        for adapter, adapter_status in adapters_status.items():
            assert adapter_status == "disabled"

    adapters_status: dict[str, str] = {
        adapter: WinNetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters
    }
    for adapter, adapter_status in adapters_status.items():
        assert adapter_status != "disabled"


@pytest.mark.xfail(not is_admin, reason="Will fail if not Admin", raises=ResourceWarning, strict=True)
def test_ctx_diable_all_with_exception():
    adapters = WinNetAdapter.get_netadapters()
    try:
        with ctx_disable_all_adapters():
            raise RuntimeError
    except RuntimeError:
        adapters_status: dict[str, str] = {
            adapter: WinNetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters
        }
        for adapter, adapter_status in adapters_status.items():
            assert adapter_status != "disabled"
