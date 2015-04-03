#!/usr/bin python
import liblo, sys

class OSCserver:
	def __init__(self, port, dataType, *argv):
		self.server = None
		self.toReturn = None

		try:
		    self.server = liblo.Server(port)
		except liblo.ServerError, err:
		    print str(err)
		    sys.exit()

		def callback(path, args):
		    self.toReturn = [path, args]

		for arg in argv:
			self.server.add_method(arg, dataType, callback)

	def receive(self):
		self.server.recv(5)
		return self.toReturn

class OSCclient:
	def __init__(self, address, port):
		try:
			self.target = liblo.Address(address, port)
		except liblo.AddressError, err:
			print str(err)
			sys.exit()

	def sendMessage(self, tag, *args):
		liblo.send(self.target, tag, *args)