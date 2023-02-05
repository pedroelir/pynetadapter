import os
import ctypes

import pytest
from netadapter import NetAdapter, disable_all_adapters


adapter_name = "Ethernet"
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()


def test_get_adapters():
    adpaters = NetAdapter.get_netadapters()
    assert adapter_name in adpaters


@pytest.mark.xfail(not is_admin, reason="Will fail if not Admin")
def test_disable_adapter():
    assert NetAdapter.disable_netadapter(adapter_name=adapter_name)


def test_enable_adapter():
    assert NetAdapter.enable_netadapter(adapter_name=adapter_name)


def test_adapter_status():
    assert NetAdapter.get_adapter_status(adpter_name=adapter_name)


def test_bad_disable_adapter():
    assert not NetAdapter.disable_netadapter(adapter_name=adapter_name[:-2])


def test_bad_enable_adapter():
    assert not NetAdapter.enable_netadapter(adapter_name=adapter_name[:-2])


def test_bad_adapter_status():
    with pytest.raises(AttributeError):
        NetAdapter.get_adapter_status(adpter_name=adapter_name[:-2])


@pytest.mark.xfail(not is_admin, reason="Will fail if not Admin", raises=ResourceWarning, strict=True)
def test_ctx_diable_all():
    adapters = NetAdapter.get_netadapters()
    with disable_all_adapters():
        adapters_status: dict[str, str] = {
            adapter: NetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters
        }
        for adapter, adapter_status in adapters_status.items():
            assert adapter_status == "disabled"

    adapters_status: dict[str, str] = {
        adapter: NetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters
    }
    for adapter, adapter_status in adapters_status.items():
        assert adapter_status != "disabled"


@pytest.mark.xfail(not is_admin, reason="Will fail if not Admin", raises=ResourceWarning, strict=True)
def test_ctx_diable_all_with_exception():
    adapters = NetAdapter.get_netadapters()
    try:
        with disable_all_adapters():
            raise RuntimeError
    except RuntimeError:
        adapters_status: dict[str, str] = {
            adapter: NetAdapter.get_adapter_status(adpter_name=adapter).casefold() for adapter in adapters
        }
        for adapter, adapter_status in adapters_status.items():
            assert adapter_status != "disabled"
