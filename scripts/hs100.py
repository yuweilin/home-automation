#!/bin/bash python3
from pyHS100 import SmartPlug

from util import *

class HS100():
  def __init__(self, name, ip):
    self.name = name
    self.ip = ip
    print(name, ip, type(ip), len(ip))
    self.plug = SmartPlug(ip)
    self.logger = GetLogger('hs100')
    self.logger.info("Link to an HS100 at {0} with name {1}.".format(ip, name))

  def switch(self):
    if self.plug.state == SmartPlug.SWITCH_STATE_OFF:
      self.plug.turn_on()
    else:
      self.plug.turn_off()
    self.logger.info("Switch {0} (HS100) to {1}.".format(self.name, self.plug.state))

if __name__ == '__main__':
  with open('/home/yuweilin/home-automation/data/hs100.csv', 'r') as fin:
    devices = {}
    for line in fin:
      name, ip = line.strip().split(',')
      devices[name] = HS100(name, ip)
    while True:
      x = input("0 to switch bedroom, 1 to switch living room, others to exit: ")
      if x == "0":
        devices["BedRoomPlug"].switch()
      elif x == "1":
        devices["LivingRoomPlug"].switch()
      else:
        break

