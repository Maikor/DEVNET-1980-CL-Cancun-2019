---
published: false
date: '2019-10-18 03:24 -0400'
title: 'Step 2: Salt Concepts'
author: Mike Korshunov
excerpt: >-
  Salt Concepts: get familiar with Salt proxy approach based on NAPALM and YAML syntax language. 
tags:
  - iosxr
  - cisco
  - Salt
  - lab
---

{% include toc %}

Before start playing with Salt it would be good to go through multiple concepts utilized in this piece of software. 
Current article will cover Salt vocabulary, _YAML_ - King of definition languages nowadays (sorry JSON) and NAPALM, one 
of components for network elements abstraction. 

## Salt Vocabulary

Salt was born as a distributed remote execution system used to execute commands and query data on remote nodes,
 or `minions`, either individually or by arbitrary selection criteria, or `targeting`.
 
Salt has been extended to a configuration management system, capable of maintaining remote nodes in defined states 
(for example, ensuring that specific packages are installed and specific services are running). There are lots of 
components in Salt!

- `master`, the server that runs the core services to communicate with Salt minions. It also contains the key store for 
encryption between the minions.

- `minions`, the agents that run a micro version of Salt for local execution and communication back to the master.

- `engines`, Salt Engines are long-running, external system processes that leverage Salt.

- `states, or formulas`, files that contain YAML and templated data to configure minions. The templating engine is also 
very flexible. It’s not limited to Jinja, but also chetah, genshi, mako (very important for those from a Puppet 
background), wempy or even pure python.


Minions (proxy or regular) can be targeted using grains, pillars or identifiers. There are other targeting plugins
 (and you can develop your own, based on something like a SQL query or a KV store).

- `grains`, Salt comes with an interface to derive information about the underlying system. This is called the grains 
interface, because it presents Salt with grains of information. Grains are collected for the operating system,
 domain name, IP address, kernel, OS type, memory, and many other system properties. The grains interface is made 
 available to Salt modules and components so that the right Salt minion commands are automatically available on the 
 right systems.
 
- `pillars`, A pillar is an interface for Salt designed to offer global values that can be distributed to minions. A 
pillar is a free form resource of data (that can be either JSON, YAML or whatever you need), and can either be stored 
in files, or externally. This is a unique property of Salt and allows integration with other systems where a shared 
data store would be of value (e.g. an ITSM or asset register).


For data fetching you can also return data from minions and store it in the Salt `mine` to be used in other tasks like 
template-based state configuration. Unlike Ansible (which only supports YAML), this can be in a variety of formats.

## YAML

### YAML Intro

YAML stands for "YAML Ain't Markup Language" and it is used extensively in Salt/Ansible for its configuration files,
 blueprints.

YAML is to configuration what markdown is to markup. It’s basically a human-readable structured data format.
 It is less complex and ungainly than XML or JSON, but provides similar capabilities. It essentially allows you to
provide powerful configuration settings, without having to learn a more complex code type like CSS, JavaScript, and PHP.

YAML is built from the ground up to be simple to use. At its core, a YAML file is used to describe data. 
One of the benefits of using YAML is that the information in a single YAML file can be easily translated to 
multiple language types.

### Basic Data Types

YAML excels at working with mappings (hashes / dictionaries), sequences (arrays / lists), and scalars
 (strings / numbers). While it can be used with most programming languages, it works best with languages that
  are built around these data structure types. This includes: PHP, Python, Perl, JavaScript, and Ruby.
    
#### Scalars

Scalars are a pretty basic concept. They are the strings and numbers that make up the data on the page. A scalar could 
be a boolean property, like Yes, integer (number) such as 5, or a string of text, like a sentence or the hostname of your
 router.
    
Scalars are often called variables in programming. If you were making a list of types of animals, 
they would be the names given to those animals.
    
 Most scalars are unquoted, but if you are typing a string that uses punctuation and other elements that can be 
 confused with YAML syntax (dashes, colons, etc.) you may want to quote this data using single ' or double " 
 quotation marks. Double quotation marks allow you to use escapings to represent ASCII and Unicode characters.
 
```   
integer: 25
string: "25"
float: 25.0
boolean: Yes
```
 
#### Sequences

Here is a simple sequence you might find in Grav. It is a basic list with each item in the list placed in its own 
line with an opening dash.
    
  - Cat
  - Dog
  - Goldfish
    
This sequence places each item in the list at the same level. If you want to create a nested sequence with items and sub-items, you can do so by placing a single space before each dash in the sub-items. YAML uses spaces, NOT tabs, for indentation. You can see an example of this below.    

```

-
  - Cat
  - Dog
  - Goldfish
-
   - Python
   - Lion
   - Tiger
```


If you wish to nest your sequences even deeper, you just need to add more levels.
    
```    

-
  -
    - Cat
    - Dog
    - Goldfish

```

Sequences can be added to other data structure types, such as mappings or scalars.
    
#### Mappings

Mapping gives you the ability to list keys with values. This is useful in cases where you are assigning a name or a 
property to a specific element.

```    

animal: pets

```
 
 This example maps the value of **pets** to the **animal** key. When used in conjunction with a sequence, 
 you can see that you are starting to build a list of pets. In the following example, the dash used to label each
  item counts as indentation, making the line items the child and the mapping line pets the parent.
 
```
   
    pets:
     - Cat
     - Dog
     - Goldfish
  
```

Check out Official YAML [Guide](https://yaml.org/) 

### Linters

Shortest subsection of the article. Keep one of your YAML Linters in bookmarks. Here is my personal favorite
 [https://codebeautify.org/yaml-validator](https://codebeautify.org/yaml-validator)

## NAPALM

NAPALM (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python
 library that implements a set of functions to interact with different router vendor devices using a unified API.
NAPALM supports several methods to connect to the devices, to manipulate configurations or to retrieve data.

Installation:
```
pip install napalm
```

The plan to upgrade napalm as fast as possible. Adding new methods and bugfixes. 
To upgrade napalm it's a simple as repeating the steps you performed while installing but adding the -U flag. 
For example:

```

pip install napalm -U

```

Beginning with release code named Carbon (2016.11), NAPALM is fully integrated in SaltStack -
 no additional modules required. For setup recommendations, please see napalm-Salt. For 
 documentation and usage examples, you can check the modules documentation, starting from the 
 release notes and this blog post.


### Config Load / Replace

```python

# Sample script to demonstrate loading a config for a device.
#
# Note: this script is as simple as possible: it assumes that you have
# followed the lab setup in the quickstart tutorial, and so hardcodes
# the device IP and password.  You should also have the
# 'new_good.conf' configuration saved to disk.
from __future__ import print_function

import napalm
import sys
import os


def main(config_file):
    """Load a config for the device."""

    if not (os.path.exists(config_file) and os.path.isfile(config_file)):
        msg = "Missing or invalid config file {0}".format(config_file)
        raise ValueError(msg)

    print("Loading config file {0}.".format(config_file))

    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver("ios")

    # Connect:
    device = driver(
        hostname="127.0.0.1",
        username="vagrant",
        password="vagrant",
        optional_args={"port": 12443},
    )

    print("Opening ...")
    device.open()

    print("Loading replacement candidate ...")
    device.load_replace_candidate(filename=config_file)

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print("\nDiff:")
    print(device.compare_config())

    # You can commit or discard the candidate changes.
    try:
        choice = raw_input("\nWould you like to commit these changes? [yN]: ")
    except NameError:
        choice = input("\nWould you like to commit these changes? [yN]: ")
    if choice == "y":
        print("Committing ...")
        device.commit_config()
    else:
        print("Discarding ...")
        device.discard_config()

    # close the session with the device.
    device.close()
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please supply the full path to "new_good.conf"')
        sys.exit(1)
    config_file = sys.argv[1]
    main(config_file)

```


Run the script, passing the path to the new_good.conf file as an argument:

```
python load_replace.py ../sample_configs/new_good.conf
```

### Presentations

* [NANOG 64 Presentation & Demo](https://youtu.be/93q-dHC0u0I) by David Barroso and Elisa Jasinska
* [Netnod Autumn Meeting 2015 Presentation](https://www.netnod.se/sites/default/files/NAPALM-david_barroso-Netnodautumnmeeting2015.pdf) by David Barroso
* [Automating IXP Device Configurations with Ansible at the Euro-IX Forum](https://www.euro-ix.net/m/uploads/2015/10/26/euroix-berlin-v2.pdf) by Elisa Jasinska
* [Network Automation with Salt and NAPALM at NANOG 68](https://www.nanog.org/sites/default/files/NANOG68%20Network%20Automation%20with%20Salt%20and%20NAPALM%20Mircea%20Ulinic%20Cloudflare%20(1).pdf); [video](https://www.youtube.com/watch?v=gV2918bH5_c); [recorded demo](https://www.youtube.com/watch?v=AqBk5fM7qZ0) by Mircea Ulinic


### NAPALM  Authors

 * David Barroso ([dbarrosop@dravetech.com](mailto:dbarrosop@dravetech.com))
 * Elisa Jasinska ([elisa@bigwaveit.org](mailto:elisa@bigwaveit.org))
 * Many others, check the [contributors](https://github.com/napalm-automation/napalm/graphs/contributors) page 
 for details.


Next chapter:

[Step 1]({{site.baseurl}}/wkinstructions/2019-10-17-step-1-Salt-overview/){: .btn } or
 [Step 3]({{site.baseurl}}/wkinstructions/2019-10-19-step-3-Salt-in-action/){: .btn }


