#!/bin/bash python3
import sys
sys.path.append('../lib/fliclib-linux-hci/clientlib/python/')

import asyncio
from aioflic import *
from util import *

class FlicScanner():
  def __init__(self, log="flic_scanner", localhost=5551):
    self.actions = {}
    self.logger = GetLogger(log)
    self.logger.info("Creating a Flic scanner...")
    # Initialize the scanner
    self.loop = asyncio.get_event_loop()
    coro = self.loop.create_connection(lambda: FlicClient(self.loop), 
        'localhost', localhost)
    _, self.client = self.loop.run_until_complete(coro)
    self.client.on_get_info = self._GotInfo

  def AddAction(self, address, action, click_type=None):
    self.actions[address] = self.actions.get(address, []) + [(None, action)]

  def _GetActions(self, channel, click_type, was_queued, time_diff):
    for action_click_type, action in self.actions.get(channel.bd_addr, []):
      if action_click_type is None or action_click_type == click_type:
        action()

  def _GotButton(self, address):
    cc = ButtonConnectionChannel(address)
    cc.on_button_single_or_double_click_or_hold = self._GetActions
    self.client.add_connection_channel(cc)
    self.logger.info("Connect to button with mac address: {0}".format(address))

  def _GotInfo(self, items):
    print(self.actions)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
      self._GotButton(bd_addr)
    flic_wizard = ScanWizard()
    flic_wizard.on_button_connected = \
        lambda scan_wizard, bd_addr, name: self._GotButton(bd_addr)
    self.client.add_scan_wizard(flic_wizard)

  def Run(self):
    self.client.get_info()
    self.loop.run_forever()
    self.client.close()
    self.loop.close()

  def Stop(self):
    self.loop.stop()

if __name__ == '__main__':
  scanner = FlicScanner(log="testflic")
  with open('../data/flic.csv', 'r') as fin:
    def PrintFunc(name, address):
      return lambda : \
        print("Click on {0} with address {1}".format(name, address))
    for line in fin:
      name, address = line.strip().split(',')  
      scanner.AddAction(address, PrintFunc(name, address))
  try:
    scanner.Run()
  except:
    print("Exit!")
  finally:
    scanner.Stop()
