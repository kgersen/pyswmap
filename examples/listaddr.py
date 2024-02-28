#!/usr/bin/env python
import sys
import argparse

sys.path.append("..")

from pyswmap import MapCalc


parser=argparse.ArgumentParser(description="MapCalc")
parser.add_argument("-rulev6")
parser.add_argument("-rulev4")
parser.add_argument("-ratio",type=int,default=argparse.SUPPRESS)
parser.add_argument("-ealen",type=int,default=argparse.SUPPRESS)
parser.add_argument("-psidoffset",type=int,default=0)
parser.add_argument("-pd")
args=parser.parse_args()


# This prints out a list of all possible MAP end-user IPv6 prefixes,
# applicable MAP IPv6 addresses, and PSIDs for a particular domain.
# PSID will always equal 0 for a sharing ratio of 1:1.  This script is
# allows the entering in of the mapping rule via the command line but is
# otherwise the same as listmapaddresses.py.

# Syntax is as follows:
#  ./listaddr.py -rulev6 [Rule IPv6] -rulev4 [Rule IPv4] -ratio [ratio] -ealen [ealen] -psidoffset [psidoffset]
# an optionnal -pd [pd] is also passed

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.

m = MapCalc(**vars(args))

# print contiguous ranges in a list of ordered integers
def print_ranges(l):
  if not l:
    print("no range!")
    return

  first = l[0]
  curr = first

  for n in l[1:]:
    if n != curr + 1:
      print("{}-{}, ".format(first,curr),end="")
      first = n
    curr = n
  print("{}-{}".format(first,curr))



# The attribute rulev4object is the object returned for a particular
# instance of the ip_address class from module Python ipaddress.
for y in range(m.rulev4object.num_addresses):
    for w in range(2**m.psidbits):
        mapce = m.get_mapce_addr(m.rulev4object[y], w)
        pd = m.get_mapce_prefix(m.rulev4object[y], w)
        if args.pd is None:
            print(
                "User prefix: {}  MAP address: {}  PSID: {} IPv4: {}".format(
                    pd,
                    mapce,
                    w,
                    m.get_map_ipv4(mapce),
                )
            )
        if args.pd == pd:
            print(
                "User prefix: {}\nMAP address: {}\nPSID: {}\nIPv4: {}".format(
                    pd,
                    mapce,
                    w,
                    m.get_map_ipv4(mapce),
                )
            )
            print("reversed ports: {}\nAvailable ports ({} range): ".format(
                    "todo",
                    m.port_ranges(),
                ),end=""
            )
            print_ranges(m.port_list(w))
