# import driver from NAPALM
from napalm_base import get_network_driver
# select driver for XR
d = get_network_driver('iosxr')
# provide credentials for connecting to the device
e = d('10.10.20.70', 'admin', 'admin', optional_args={'config_lock': False, 'port': 2221})
# open the connection
e.open()
# close the connection
e.close()

# repeat for router 2
f = d('10.10.20.70', 'admin', 'admin', optional_args={'config_lock': False, 'port': 2231})
f.open()
f.close()