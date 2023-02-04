from netadapter import NetAdapter

adapter_name = "Ethernet"


def test_get_adapters():
    adpaters = NetAdapter.get_netadapters()
    assert adapter_name in adpaters


def test_disable_adapter():
    assert NetAdapter.disable_netadapter(adapter_name=adapter_name)


def test_enable_adapter():
    assert NetAdapter.enable_netadapter(adapter_name=adapter_name)
