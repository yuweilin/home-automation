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

  def state(self):
    return self.plug.state

  def turn_on(self):
    self.plug.turn_on()
    self.logger.info("Turn on {0} (HS100).".format(self.name))

  def turn_off(self):
    self.plug.turn_off()
    self.logger.info("Turn off {0} (HS100).".format(self.name))

  def switch(self):
    if self.state() == SmartPlug.SWITCH_STATE_OFF:
      self.plug.turn_on()
    else:
      self.plug.turn_off()
    self.logger.info("Switch {0} (HS100) to {1}.".format(self.name, self.state()))
  
class HS100Group():
  def __init__(self, name, plugs):
    self.name = name
    self.plugs = plugs
    self.logger = GetLogger('hs100')
    self.logger.info(
        "Create a plug group ({0}) with plugs {1}.".format(
          self.name, [plug.name for plug in self.plugs]))

  def switch(self):
    if any(plug.state()!=SmartPlug.SWITCH_STATE_OFF for plug in self.plugs):
      [plug.turn_off() for plug in self.plugs]
      self.logger.info(
          "Not all plugs in group {0} is off, turn off all the plugs.".format(
            self.name))
    else:
      [plug.turn_on() for plug in self.plugs]
      self.logger.info(                
          "All plugs in group {0} are off, turn on all the plugs.".format(
            self.name)) 

if __name__ == '__main__':
  devices = {}
  with open('../data/hs100.csv', 'r') as fin:
    for line in fin:
      name, ip = line.strip().split(',')
      devices[name] = HS100(name, ip)
  with open('../data/hs100_groups.csv', 'r') as f:
    for line in f:
      line = line.strip().split(',')
      name = line[0]
      plugs = [devices[plug] for plug in line[1:] if plug in devices]
      devices[name] = HS100Group(name, plugs)
  
  print(devices.keys())
  while True:
    x = input("0 to switch living room group, 1 to switch desk lamp, others to exit: ")
    if x == "0":
      devices["LivingRoomGroup"].switch()
    elif x == "1":
      devices["DeskLamp"].switch()
    else:
      break
