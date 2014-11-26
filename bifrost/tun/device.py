#!/usr/bin/env python3

from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI

import logging
#logging.basicConfig(level=logging.DEBUG)

class TunDevice():
	"""
	Class responsible for create and maintain the tun ethernet device.
	"""
	def __init__(self, dev="tun0", addr="172.16.0.1", remote="172.16.0.2", mask="255.255.240.0", mtu="1400"):
		self.log = logging.getLogger(type(self))
		self.observers = list()
		self.tun = TunTapDevice(name=dev, flags=(IFF_TUN|IFF_NO_PI))
		self.tun.addr = addr
		self.tun.dstaddr = remote
		self.tun.netmask = mask
		self.tun.mtu = int(mtu)
		self.tun.up()
		self.log.debug("Tunnel device {0} created.".format(type(self))
	
	def fileno(self):
		return self.tun.fileno()
	
	def connectionLost(self, reason):
		self.log.warn("Tunnel device closed (reason: {0}).".format(reason))
	
	def registerObserver(self, observer):
		"""
		Observer Design Pattern.
		"""
		self.observers.append(observer)
		self.log.debug("Added {0} Observer.".format(observer)
	
	def doRead(self):
		data = self.tun.read(self.tun.mtu)
		self.log.debug("Data received (size: {0}).".format(size(data)))
		for o in observers:
			o.notify(data)
			self.log.debug("Data sent to {0} Observer.".format(o))
	
	def write(self, data):
		try:
			self.tun.write(data)
			self.log.info("Data sent to Tun device (size: {0}).".format(size(data)))
		except:
			self.log.error("Error writing to Tun device!", exc_info=True)
