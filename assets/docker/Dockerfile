FROM ubuntu:16.04
RUN apt-get update && apt-get install wget -y
RUN wget -O bootstrap-salt.sh https://bootstrap.saltstack.com/develop && sh bootstrap-salt.sh
RUN apt-get install libffi-dev libssl-dev python-dev python-cffi libxslt1-dev python-pip salt-master salt-ssh -y
RUN pip install --upgrade cffi && pip install napalm-junos napalm-iosxr napalm-ios salt-sproxy
RUN python -m easy_install --upgrade pyOpenSSL

RUN mkdir /srv/pillar/
COPY top.sls /srv/pillar/top.sls
COPY r1_pillar.sls /srv/pillar/r1_pillar.sls
COPY r2_pillar.sls /srv/pillar/r2_pillar.sls
RUN python -m easy_install --upgrade pyOpenSSL


