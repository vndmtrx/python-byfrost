#!/usr/bin/env python3

#from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol
from autobahn.asyncio.websocket import WebSocketClientFactory, WebSocketClientProtocol

import logging
#logging.basicConfig(level=logging.DEBUG)

class SimpleTunClientFactory(WebSocketClientFactory):
	"""
	Class responsible for create and initialize the protocol instances.
	"""
	
	def __init__(self, url, device):
		# Add here parameters that can be used by all protocol instances
		super.__init__(self, url)
		self.device = device
		self.log = logging.getLogger(type(self))
		self.log.debug("Factory {0} created.".format(type(self))
	
	def buildProtocol(self, addr):
		# Here is the place when the protocol instance is created
		protocol = SimpleTunClientProtocol(device)
		return protocol


class SimpleTunClientProtocol(WebSocketClientProtocol):
	"""
	Class that implements the websocket protocol used for communication.
	"""
	
	def __init__(self, device):
		super.__init__(self)
		self.device = device
		self.log = logging.getLogger(type(self))
		self.log.debug("Protocol instance {0} created.".format(type(self))
	
	def onConnect(self, response):
		self.log.info("Websocket connected.")
	
	def onOpen(self):
		self.log.info("Websocket oppened.")
	
	def onClose(self, wasClean, code, reason):
		self.log.warn("WebSocket closed (reason: {0}; wasClean: {1}).".format(reason, wasClean))
	
	def onMessage(self, data, isBinary):
		self.device.write(data)
		self.log.debug("Data sent.")
	
	def notify(self, data):
		"""
		Observer Design Pattern.
		"""
		self.sendMessage(data, isBinary=True)
		self.log.debug("Data sent to WebSocket (size: {0}).".format(size(data)))
