from napalm_base import get_network_driver
d = get_network_driver('iosxr')
e = d('10.10.20.70', 'admin', 'admin', optional_args={'config_lock': False, 'port': 2221})
e.open()
e.close()

f = d('10.10.20.70', 'admin', 'admin', optional_args={'config_lock': False, 'port': 2231})
f.open()
f.close()
