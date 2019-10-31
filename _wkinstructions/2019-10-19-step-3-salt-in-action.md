---
published: true
date: '2019-10-19 03:18 -0400'
title: 'Step 3: Salt in Action'
author: Mike Korshunov
excerpt: >-
  Understanding the basic Salt operations infrastructure of
   IOS-XR and libraries available automation
tags:
  - iosxr
  - cisco
  - salt
  - lab
---

{% include toc %}  

We are ready to start some actions! Let's proceed! 💻📚

## Establish connectivity to your POD

>Connect to your Pod first! Make sure your Anyconnect VPN connection to the Pod assigned to you is active. 
>
> If you haven't connected yet, check out the instructions to do so here: 
><https://xr-dev.net/assets/CLC19-Mikhail%20Korshunov-IOS-XR-Programmability.pdf>
>
>
> Once you're connected, use the following instructions to connect to the individual nodes.
> The instructions in the workshop will simply refer to the Name of the box to connect without
> repeating the connection details and credentials. So refer back to this list when you need it.
>  
>
> The 3 nodes in the topology are: 
> 
><p style="font-size: 16px;"><b>Development Linux System (DevBox)</b></p> 
>      IP Address: 10.10.20.70
>      Username/Password: [admin/admin]
>      SSH Port: 2211
> 
>
><p style="font-size: 16px;"><b>IOS-XRv9000 R1: (Router r1)</b></p> 
>
>     IP Address: 10.10.20.70  
>     Username/Password: [admin/admin]   
>     Management IP: 10.10.20.70  
>     XR SSH Port: 2221    
>     NETCONF Port: 8321   
>     gRPC Port: 57021  
>     XR-Bash SSH Port: 2222    
>
>
><p style="font-size: 16px;"><b>IOS-XRv9000 R2:  (Router r2)</b></p> 
>
>     IP Address: 10.10.20.70   
>     Username/Password: [admin/admin]   
>     Management IP: 10.10.20.70   
>     XR SSH Port: 2231    
>     NETCONF Port: 8331   
>     gRPC Port: 57031    
>     XR-Bash SSH Port: 2232
{: .notice--info}



The Topology in use is shown below:
![topology_devnet.png]({{site.baseurl}}/images/topology_devnet.png)  



## Connect to router r1

<p style="margin: 2em 0!important;padding: 0.85em;font-family: CiscoSans,Arial,Helvetica,sans-serif;font-size: 0.85em !important;text-indent: initial;background-color: #e6f2f7;border-radius: 5px;box-shadow: 0 1px 1px rgba(0,127,171,0.25);"><b>Username</b>: admin<br/><b>Password</b>: admin<br/><b>SSH port</b>: 2221<br/><b>IP</b>: 10.10.20.170
</p>  

```
Laptop-terminal:$ ssh -p 2221 admin@10.10.20.70


--------------------------------------------------------------------------
  Router 1 (Cisco IOS XR Sandbox)
--------------------------------------------------------------------------


Password:


RP/0/RP0/CPU0:r1#
RP/0/RP0/CPU0:r1#
RP/0/RP0/CPU0:r1#

```

## Enable XML Agent on the Box commands

Current proxy support for IOS-XR devices relies on NAPALM. NAPALM using XML Agent API for communication with routers. 
Let's enable it on both devices. 

```

RP/0/RP0/CPU0:r1#conf t
Wed Oct 30 16:50:03.197 UTC
RP/0/RP0/CPU0:r1(config)#xml agent tty
RP/0/RP0/CPU0:r1(config-xml-tty)#iteration off
RP/0/RP0/CPU0:r1(config-xml-tty)#root
RP/0/RP0/CPU0:r1(config)#show
Wed Oct 30 16:50:14.913 UTC
Building configuration...
!! IOS XR Configuration version = 6.4.1
xml agent tty
 iteration off
!
end

RP/0/RP0/CPU0:r1(config)#commit
Wed Oct 30 16:50:19.368 UTC
RP/0/RP0/CPU0:r1(config)#

```

Now we can repeat the procedure for **r2**

## Checking connection with NAPALM Code 

```python

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

```

### Start Salt on your Laptop in a Docker container

We will be running Salt in a Docker container. First command to pull the image and the second one to run the container.
```
docker pull maikor/salt-ubuntu


docker run -it --rm --name salty maikor/salt-ubuntu bash

```

To attach to the Salt container use following command:

```
docker exec -it salty bash
```



#### Configure the connection with a device


The `master` config file is expecting pillar to be in `/srv/pillar`. This directory was created during container build 
process, but on a fresh install it may be missing.


To configure store the pillars in a different directory, see the
 [`pillar_roots`](https://docs.saltstack.com/en/latest/ref/configuration/master.html#pillar-roots)
  (and [`file_roots`](https://docs.saltstack.com/en/latest/ref/configuration/master.html#file-roots)) 
  configuration options in the master configuration file (typically `/etc/salt/master` or `/srv/master` - depending on
   the operating system).

Next, we need to have a `top.sls` file in that directory, which tells the salt-master which minions receive which
 pillar. Check `/srv/pillar/top.sls` file. It should look like this:

```yaml
base:
  [DEVICE_ID]:
    - [DEVICE_SLS_FILENAME]
```

where:

  - DEVICE_ID will be the name used to interact with the device, from the CLI of the server
  - DEVICE_SLS_FILENAME is the name of the file containing the specifications of the device

Workshop Example:

```yaml
base:
  r1:
    - r1_pillar
  r2:
    - r2_pillar
```

where:

  - r1 is the name used to interact with the device: `salt 'r1' test.ping`
  - `/srv/pillar/r1_pillar.sls` is the file containing the specifications of this device
  
Pay attention to this structure⚠️
{: .notice--warning}


 
 Notice that the `- r1_pillar` portion of the `top.sls` file is
 missing the `.sls` extension, even though this line is expecting to see a file in the same directory
  called `r1_pillar.sls`. In addition, note that there should not be dots used when referencing the `.sls` file, 
  as this will be interpreted as a directory structure. For example, if you had the line configured as `- r1.pillar`,
 salt would look in the `/srv/pillar` directory for a folder called `r1`, and then for a file in that directory
 called `pillar.sls`. One last thing - I'm referring to the pillar file as `r1_pillar` in this example to make 
it explicitly clear that the last line is referencing a pillar file, but it is more common to call the pillar file 
 the name of the device itself, so:

```yaml
base:
  r1:
    - r1_pillar
```    
Now that we've referenced this `r1_pillar` file, we need to create it and add the pillar. Create and edit the `/srv/pillar/router1_pillar.sls` file and add the following:

```yaml
proxy:
  proxytype: napalm
  driver: [DRIVER]
  host: [HOSTNAME]
  username: [USERNAME]
  passwd: [PASSWORD]
```

where:

  - DRIVER is the driver to be used when connecting to the device. For the complete list of supported operating systems, please check the [NAPALM readthedocs page](https://napalm.readthedocs.io/en/latest/#supported-network-operating-systems)
  - HOSTNAME, USERNAME, PASSWORD are the connection details

Example ```r1_pillar.sls```:

```yaml
proxy:
  proxytype: napalm
  driver: iosxr
  host: 10.10.20.70
  username: admin
  passwd: admin
  optional_args:
    port: 2221
```

Make sure the pillar is a valid YAML file! Use Linters to validate it. 
{: .notice--warning}


In one Terminal window we will run the Salt Master itself.  

```
root@d48d7fce9e74:/#
root@d48d7fce9e74:/#
root@d48d7fce9e74:/# salt-master
```

Create a new terminal window and access the container:

```
docker exec -it salty bash

```

Before executing the command, we should review the structure of CLI:

![salt_4.png]({{site.baseurl}}/images/salt/salt-4.png)  


We are ready to start leverage [salt-sproxy](https://github.com/mirceaulinic/salt-sproxy) 

```
root@d48d7fce9e74:/# salt-sproxy r1 test.ping
r1:
    True

```


``` yaml




root@d48d7fce9e74:/srv/pillar# salt-sproxy r2 net.interfaces
r2:
    ----------
    comment:
    out:
        ----------
        GigabitEthernet0/0/0/0:
            ----------
            description:
            is_enabled:
                False
            is_up:
                False
            last_flapped:
                -1.0
            mac_address:
                52:54:00:93:8A:B0
            speed:
                1000
        GigabitEthernet0/0/0/1:
            ----------
            description:
            is_enabled:
                False
            is_up:
                False
            last_flapped:
                -1.0
            mac_address:
                52:54:00:93:8A:B1
            speed:
                1000
        GigabitEthernet0/0/0/2:
            ----------
            description:
            is_enabled:
                False
            is_up:
                False
            last_flapped:
                -1.0
            mac_address:
                52:54:00:93:8A:B2
            speed:
                1000
        GigabitEthernet0/0/0/3:
            ----------
            description:
            is_enabled:
                False
            is_up:
                False
            last_flapped:
                -1.0
            mac_address:
                52:54:00:93:8A:B3
            speed:
                1000
        GigabitEthernet0/0/0/4:
            ----------
            description:
            is_enabled:
                False
            is_up:
                False
            last_flapped:
                -1.0
            mac_address:
                52:54:00:93:8A:B4
            speed:
                1000
        MgmtEth0/RP0/CPU0/0:
            ----------
            description:
                *** MANAGEMENT INTERFACE ***
            is_enabled:
                True
            is_up:
                True
            last_flapped:
                -1.0
            mac_address:
                52:54:00:DE:0A:EF
            speed:
                1000
        Null0:
            ----------
            description:
            is_enabled:
                True
            is_up:
                True
            last_flapped:
                -1.0
            mac_address:
            speed:
                0
    result:
        True
root@d48d7fce9e74
```


### Ready for More? 

Few other examples to give a try:

```
salt r1 net.arp
salt r1 net.mac
salt r1 net.lldp
salt r1 net.ipaddrs
salt r1 net.interfaces
salt r1 ntp.peers
salt r1 ntp.set_peers 192.168.0.1 172.17.17.1 172.17.17.2
salt r1 bgp.config  # returns the BGP configuration
salt r1 bgp.neighbors  # provides statistics regarding the BGP sessions
salt r1 snmp.config
salt r1 route.show 1.2.3.4/24 bgp
salt r1 probes.config
salt r1 probes.results
salt r1 net.commit
salt r1 net.rollback
```

Congratulations with Salt workshop completion! Now you should have a understanding how Salt architecture looks like,
main pros and cons for Salt and you are ready to elaborate your further knowledge on Salt! 
 

## Resources

- [Salt in 10 minutes](https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html)
- [https://www.saltstack.com/blog/whats-saltstack/](https://www.saltstack.com/blog/whats-saltstack/ )
- [https://xrdocs.io](https://xrdocs.io) 
- [https://github.com/napalm-automation/napalm-salt](https://github.com/napalm-automation/napalm-salt)
- [https://github.com/mirceaulinic/salt-sproxy](https://github.com/mirceaulinic/salt-sproxy), author Mircea Ulinic
