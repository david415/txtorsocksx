from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import clientFromString


class GETSlash(Protocol):
    def connectionMade(self):
        self.transport.write("GET / HTTP/1.1\r\nHost: timaq4ygg2iegci7.onion\r\n\r\n")

    def buildProtocol(self):
        return self

    def dataReceived(self, data):
        print "Got this as a response"
        print data

class GETSlashFactory(Factory):
    def buildProtocol(self, addr):
        print "Building protocol towards"
        return GETSlash()


torEndpoint = clientFromString(reactor, "tor:host=timaq4ygg2iegci7.onion:port=80")
d = torEndpoint.connect(GETSlashFactory())
@d.addErrback
def _gotError(error):
    print error
    print "Error in connection"
    reactor.stop()

reactor.run()
