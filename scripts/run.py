#!/bin/bash python3
import csv

from util import GetLogger
from hs100 import HS100
from flic import FlicScanner

def main():
  hs100s = {}
  with open('../data/hs100.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for name, ip in reader:
      hs100s[name] = HS100(name, ip)
  
  pairing = {
    'black': hs100s['LivingRoomPlug'].switch,
    'white': hs100s['BedRoomPlug'].switch
  }

  scanner = FlicScanner()
  with open('../data/flic.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for name, address in reader:
      scanner.AddAction(address, pairing[name])
  
  scanner.Run()

if __name__ == '__main__':
  main()
