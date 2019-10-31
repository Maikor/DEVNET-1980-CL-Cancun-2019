---
published: true
date: '2019-10-17 03:24 -0400'
title: 'Step 1: Modern Configuration Management '
author: Mike Korshunov
excerpt: >-
  Get the main ideas behind Salt anf figure out how it's different from Ansible.
tags:
  - iosxr
  - cisco
  - salt
  - lab
---

{% include toc %}

# Why Hobbits?  

Created by Thomas Hatch in 2011, Salt—now known as SaltStack—is a modular, Python-based CM tool designed for high-speed
 data collection/execution. The tool has gained considerable traction in the enterprise for its performance benefits
  over competing solutions, including Ansible.

SaltStack's speed and performance benefits are made possible by its lightweight ZeroMQ messaging library: a concurrency 
framework for establishing persistent TCP connections between the server and agents (i.e., Salt master and minions).
 The platform is available as an open source project or enterprise commercial offering known as SaltStack Enterprise. 
 
The project needed a name. While watching Lord of the Rings, Thomas noticed that in a scene between Gimli the dwarf
 and the two hobbits Peregrin Took and Meriadoc Brandybuck, Gimli fixated on the salted pork the hobbits were eating. 
 Tom thought to himself, “Well, everything is better with Salt,” and the name was born.

Just as almost everything is better with salt, SaltStack effectively adds spice to today’s modern IT infrastructure.
 Organizations are using Salt to discover, monitor, respond, orchestrate, automate, and secure assets across 
 on-premises, hybrid, cloud, and IoT systems. There’s a vital difference that sets Salt apart from its competitors: Salt
  is designed to scale, and can easily handle tens of thousands of managed systems per master.

The Salt project also has a massive and dynamic community, with 2000+ developers committing to its code base and close 
to 100,000 commits to the project since its inception.

# Salt Architecture 

The core of the Salt ecosystem consists of two critical components: the Salt Master and the Salt Minion.
 The other components play a supporting role to make the ecosystem work.

The following diagram provides a high-level architecture view of an example Salt architecture:

![salt_1.png]({{site.baseurl}}/images/salt/salt-1.png)  


# Main Use Cases 

## Asset Inventory

Asset monitoring goes with the Salt Minion. The Salt Minion is a Python-based endpoint that can be deployed on all
 major *nix and Windows operating systems. The Minions are connected to the Master, and can be asked to do a variety
 of tasks by the Master through an easy-to-understand YAML file or by directly running commands from the Master.
                                        


## Monitoring

Salt Minions can be configured to monitor files, processes, services, and a host of other things.
 They can also generate events when certain criteria are met such as failed logins, unauthorized
 changes to critical files or processes, or even unexpected changes in CPU load or disk usage.


## Respond (Reactor Engine)

Perhaps the most powerful feature of Salt is its ability to react to events and take actions using the Salt
 Reactor system. Salt Reactor can be configured to take predefined actions based on certain event criteria.
  For example, restart MySQL service if it stopped. This power helps organizations achieve a state of 
  event-driven automation.

Here’s an overview of how it works:

* The Salt Master and Salt Minions are connected to each other through an event bus.
* When a Salt Master requests Salt Minions to perform an operation, such as run a command or install a package, the 
    Salt Minion on completion registers the success or failure of that operation on the event bus.
* Salt Beacons can also register their events on the event bus.
    	
    start a process if it is stopped or send an alert to Slack.


## Orchestration

The true power of Salt starts to become evident once the building blocks that make up Salt are used to orchestrate 
and deploy complex applications by running a single command. With orchestration capability, it is now possible to define
 the infrastructure as code.

## Automate

Salt helps organizations automate routine IT jobs such as adding or removing users and updating servers with a single 
command. All of this is possible through its robust remote execution framework. The remote execution framework is made
 up of 477 execution modules that ship with Salt.

In the example below, “pkg” is the name of the execution module and “install” is the function being called within that
 module. Once the command is run it installs “vim” on all the available minions (the * represents all minions). Salt is
  intelligent enough to automatically detect the operating system, and will call “yum” for Red Hat OS and “apt-get” for
   Ubuntu under the hood to perform the function.

## Secure

Salt helps organizations secure their infrastructure. Remediation actions once the vulnerabilities or configuration 
drifts were discovered, or block threats by killing a process or closing down a port.
 Salt is perfectly designed to solve that part of the problem.

## Integrator 

Salt is designed from the ground up to integrate with a variety of applications and services. The input to Salt is 
typically a YAML file, and output can be in YAML, json, or XML, output formats conducive for automation and integration.
 It can also be configured to return the data from jobs to a third-party data source (referred to as the Salt Returner
 ) such as S3 or the PostgreSQL database for example. The combination of all these capabilities makes Salt a great
  candidate to play the role of conductor in this complex symphony of systems, code, and components we all now rely
   on as modern IT infrastructure.

# Salt vs Ansible 

Before we start to dive into tools available on the market, let's look on them from historical perspective. 
The sysadmin or devops pro of today typically needs to manage a large numbers of servers, often automating some tasks 
or performing the same action several times over, like installing and provisioning a new server, rebooting a set of 
servers at specific times every day, deploying the same package to a group of servers, and so on. For such busy folks, 
Configuration Management (CM) tools like Ansible and Salt are absolute lifesavers.


Up to around 2011, the CM market had been dominated by 2 main players – Puppet and Chef. Two up and comers are 
Ansible and Salt. They have both been developed in Python, and one of their major raison d’etre was a lingering 
dissatisfaction on their founders’ parts with the performance and execution of the big boys Puppet and Chef.


![salt_3.png]({{site.baseurl}}/images/salt/salt-3.png)  


Salt and Ansible both define their configurations using YAML, with slightly differing syntax. 
The workflow for implementation in Ansible usually involves pulling down your tasks/playbooks 
from Git, modifying if necessary, pushing out the configurations to devices, and then committing back
 to Git so others on your team can do the same thing. Conversely, Salt has a central location for 
 the configurations on the master, so there is less capability for drift when someone decides to go 
 rogue and stop checking in their changes. The biggest differentiation is reaction to events 
 on remote devices.
 
  There really isn’t a concept of reaction in Ansible. You can schedule jobs to reach out and 
 enforce configuration state on an interval or actively poll systems for changes… but the remote system can’t 
 initiate an event because there isn’t any software installed on the device. On the other hand, Salt was built 
 for exactly this use case. It has a great mechanism for triggering events from a minion in order to take action or
  notify someone of a change. An example might be watching an important configuration file for changes, triggering
   an event if it’s modified, and then having the master push out the “proper” configuration and squash local changes.
    The sky is the limit with what you can accomplish with the event bus.



![salt_2.png]({{site.baseurl}}/images/salt/salt-2.png)  

|         | Pros                                                                                                                                                                                                                                                                                                          | Cons                                                                                                                                             |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Ansible | Agent-less deployment and communication<br> CLI supports almost any programming language<br> Uses Python, which is omnipresent in Linux distros<br> Excellent security using SSH / SSH2<br> Additional Tower dashboard allows for visual management of nodes/resources  (available in the commercial version) | Prone to performance issues at times<br> Introspection (i.e., seeing Playbook variable values) is lacking                                        |
| Salt    | Quickly scalable, very resilient and efficient because of multi-master capability<br> Use of minions offers more options and flexibility than Ansible.                                                                                                                                                        | Forces users to learn Python or PyDSL<br> Underdeveloped GUI<br> Minions not as efficient as agent-less communication for small-scale deployment |

# Sources

 * [https://stackshare.io/stackups/ansible-vs-salt](https://stackshare.io/stackups/ansible-vs-salt)
 * [https://www.saltstack.com/blog/whats-saltstack/](https://www.saltstack.com/blog/whats-saltstack/)
 * [https://eitr.tech/blog/2019/05/31/ansible-vs-salt.html](https://eitr.tech/blog/2019/05/31/ansible-vs-salt.html)
 * [https://www.upguard.com/articles/ansible-vs-salt](https://www.upguard.com/articles/ansible-vs-salt)
 * [https://medium.com/@anthonypjshaw/ansible-v-s-salt-saltstack-v-s-stackstorm-3d8f57149368](https://medium.com/@anthonypjshaw/ansible-v-s-salt-saltstack-v-s-stackstorm-3d8f57149368)
 * []()

Proceed to the [Second Step]({{site.baseurl}}/wkinstructions/2019-10-18-step-2-salt-concepts/){: .btn }


 