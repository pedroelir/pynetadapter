import pytest
from netadapter import NetAdapter


adapter_name = "Ethernet"


def test_get_adapters():
    adpaters = NetAdapter.get_netadapters()
    assert adapter_name in adpaters


def test_disable_adapter():
    assert NetAdapter.disable_netadapter(adapter_name=adapter_name)


def test_enable_adapter():
    assert NetAdapter.enable_netadapter(adapter_name=adapter_name)


def test_adapter_status():
    assert NetAdapter.get_adapter_status(adpter_name=adapter_name)


def test_bad_adapter_status():
    with pytest.raises(AttributeError):
        NetAdapter.get_adapter_status(adpter_name=adapter_name[:-2])
