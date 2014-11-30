#!/usr/bin/env python3
#
# Byfrost WebSocket powered VPN Tunnel
#
###############################################################################
##
## Copyright 2014 Eduardo Rolim
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
###############################################################################

#from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol
from autobahn.asyncio.websocket import WebSocketClientFactory, WebSocketClientProtocol

import logging
#logging.basicConfig(level=logging.DEBUG)

class TunClientFactory(WebSocketClientFactory):
	"""
	Class responsible for create and initialize the protocol instances.
	"""
	
	def __init__(*args, **kwargs):
		# Add here parameters that can be used by all protocol instances
		if 'dev' in kwargs and kwargs['dev']:
			self.device = kwargs['dev']
		else:
			raise TypeError("'dev' must be specified!")
		self.crypto = kwargs['crypto'] if 'crypto' in kwargs and kwargs['crypto'] else None
		
		WebSocketClientFactory.__init__(self, *args, **kwargs)
		self.log = logging.getLogger(type(self))
		self.log.debug("Factory {0} created.".format(type(self))


class TunClientProtocol(WebSocketClientProtocol):
	"""
	Class that implements the websocket protocol used for communication.
	"""
	
	def __init__(self):
		super.__init__(self)
		self.log = logging.getLogger(type(self))
		self.log.debug("Protocol instance {0} created.".format(type(self))
	
	def onConnect(self, response):
		self.log.info("Websocket connected.")
	
	def onOpen(self):
		self.log.info("Websocket oppened.")
	
	def onClose(self, wasClean, code, reason):
		self.log.warn("WebSocket closed (reason: {0}; wasClean: {1}).".format(reason, wasClean))
	
	def onMessage(self, payload, isBinary):
		data = payload if self.factory.crypto == None else self.factory.crypto.decode(payload)
		self.factory.device.write(data)
		self.log.debug("Data sent to tun device.")
	
	def notify(self, payload):
		"""
		Observer Design Pattern.
		"""
		data = payload if self.factory.crypto == None else self.factory.crypto.encode(payload)
		self.sendMessage(data, isBinary=True)
		self.log.debug("Data sent to WebSocket (size: {0}).".format(size(data)))
