#!/usr/bin/env python

from keystoneauth1.identity import v3
from keystoneauth1 import session
import novaclient.client
import os
from neutronclient.v2_0 import client
from pprint import pprint
import sys

SECURITY_GROUP_NAME="all_ports_ingress"
INSTANCE_NAME="donaas"

def makeSecGroup(sess):
  neutron = client.Client(session=sess)
  existing = neutron.list_security_groups(name=SECURITY_GROUP_NAME)
  if not existing["security_groups"]:
    resp = neutron.create_security_group({
      "security_group": {
        "name": SECURITY_GROUP_NAME,
        "description": "auto generated by donaas"
      }
    })
    secGroupId = resp["security_group"]["id"]
    neutron.create_security_group_rule({
      "security_group_rule": {
        "direction": "ingress",
        "port_range_min": "1",
        "ethertype": "IPv4",
        "port_range_max": "65535",
        "protocol": "tcp",
        "security_group_id": secGroupId
      }
    })
    print("Created " + SECURITY_GROUP_NAME)

def makeInstance(sess):
  nova = novaclient.client.Client(2, session=sess)
  search = {
    "name": INSTANCE_NAME
  }
  existing = nova.servers.list(search_opts=search, limit=1)
  ip = None
  try:
    ip = existing[0].networks.values()[0][0]
  except:
    pass
  return ip

def launchFor(username, password):
  auth = v3.Password(auth_url='https://keystone.rc.nectar.org.au:35357/v3',
                     username=username,
                     password=password,
                     user_domain_name='default',
                     )
  sess = session.Session(auth=auth)
  makeSecGroup(sess)
  return makeInstance(sess)

if __name__ == "__main__":
  ip = launchFor(os.environ["OS_USERNAME"], os.environ["OS_PASSWORD"])
  print(ip)
