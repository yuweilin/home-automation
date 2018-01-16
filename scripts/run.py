#!/bin/bash python3
import csv
from collections import defaultdict

from util import GetLogger
from hs100 import HS100,HS100Group
from flic import FlicScanner,ClickType

def main():
  hs100s = {}
  with open('../data/hs100.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for name, ip in reader:
      hs100s[name] = HS100(name, ip)
  
  with open('../data/hs100_groups.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for line in reader:
      name = line[0]
      plugs = [hs100s[plug] for plug in line[1:] if plug in hs100s]
      hs100s[name] = HS100Group(name, plugs)

  pairing = defaultdict(list)
  with open('../data/pairing.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for flic_name, click_type, hs100 in reader:
      try:
        click_type = ClickType[click_type]
      except:
        click_type = None
      pairing[flic_name].append((click_type, hs100s[hs100].switch))

  scanner = FlicScanner()
  with open('../data/flic.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for name, address in reader:
      for click_type, action in pairing[name]:
        scanner.AddAction(address, click_type, action)
  
  scanner.Run()

if __name__ == '__main__':
  main()
