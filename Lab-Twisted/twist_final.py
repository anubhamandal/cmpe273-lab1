from __future__ import print_function

from pprint import pformat

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

import operator

urls = ["http://localhost:5000","http://localhost:6000"]

global count, my_dict
count = len(urls)
my_dict = {}
d = [None] * len(urls)
agent = [None] * len(urls)
idx = 0

class ServerLatency(Protocol):
	def __init__(self, finished, url):
		self.finished = finished
		self.remaining = 1024 * 10
		self.url = url

	def dataReceived(self, bytes):
		global my_dict
		if self.remaining:
			display = bytes[:self.remaining]
			print('Some data received:')
			print(display)
			my_dict[self.url] = display
			self.remaining -= len(display)

	def connectionLost(self, reason):
		print('Finished receiving body:', reason.getErrorMessage())
		self.finished.callback(None)

def cbRequest(response, url):
	finished = Deferred()
	response.deliverBody(ServerLatency(finished, url))
	return finished

def cbShutdown(ignored):
	global count
	count = count - 1
	if count == 0:
		reactor.stop()
	
for url in urls:

	agent[idx] = Agent(reactor)
	d[idx] = agent[idx].request(
		'GET',
		url,
		Headers({'User-Agent': ['Twisted Web Client Example']}),
		None)

	d[idx].addCallback(cbRequest, (url))
	d[idx].addBoth(cbShutdown)
	idx = idx + 1

reactor.run()


#result = dict((k, int(v)) for k, v in my_dict.iteritems())
print (min(my_dict.iteritems(), key=operator.itemgetter(1))[0])

#print (my_dict)