# Copyright (c) David Stainton <dstainton415@gmail.com>
# See LICENSE for details.

from twisted.internet import reactor, interfaces
from twisted.internet.endpoints import TCP4ClientEndpoint
from zope.interface import implementer
from twisted.plugin import IPlugin
from twisted.internet.interfaces import IStreamClientEndpointStringParser
from twisted.internet import error

from txsocksx.client import SOCKS5ClientEndpoint

__module__ = 'txtorsocksx.endpoints'


@implementer(IPlugin, IStreamClientEndpointStringParser)
class TorClientEndpointStringParser(object):
    prefix = "tor"

    def _parseClient(self, host=None, port=None, socksPort=None):
        if port is not None:
            port = int(port)
        if socksPort is not None:
            socksPort = int(socksPort)

        return TorClientEndpoint(host, port, socksPort=socksPort)

    def parseStreamClient(self, *args, **kwargs):
        return self._parseClient(*args, **kwargs)

def DefaultTCP4EndpointGenerator(*args, **kw):
    """
    Default generator used to create client-side TCP4ClientEndpoint instances.
    We do this to make the unit tests work...
    """
    return TCP4ClientEndpoint(*args, **kw)

@implementer(interfaces.IStreamClientEndpoint)
class TorClientEndpoint(object):
    """An endpoint which attempts to establish a SOCKS5 connection
    with the system tor process by iterating over a list of ports
    that tor might be listening to.

    :param host: The hostname to connect to.
    This of course can be a Tor Hidden Service onion address.

    :param port: The tcp port or Tor Hidden Service port.

    """

    socks_ports_to_try = [9050, 9150]

    def __init__(self, host, port, proxyEndpointGenerator=DefaultTCP4EndpointGenerator, socksPort=None):
        if host is None or port is None:
            raise ValueError('host and port must be specified')

        self.host = host
        self.port = port
        self.proxyEndpointGenerator = proxyEndpointGenerator
        self.socksPort = socksPort

        if self.socksPort is None:
            self.socksPortIter = iter(self.socks_ports_to_try)
            self.socksGuessingEnabled = True
        else:
            self.socksGuessingEnabled = False

    def connect(self, protocolfactory):
        self.protocolfactory = protocolfactory

        if self.socksGuessingEnabled:
            self.socksPort = self.socksPortIter.next()

        d = self._try_connect()
        return d

    def _try_connect(self):
        self.torSocksEndpoint = self.proxyEndpointGenerator(reactor, '127.0.0.1', self.socksPort)
        socks5ClientEndpoint = SOCKS5ClientEndpoint(self.host, self.port, self.torSocksEndpoint)
        d = socks5ClientEndpoint.connect(self.protocolfactory)
        if self.socksGuessingEnabled:
            d.addErrback(self._retry_socks_port)
        return d

    def _retry_socks_port(self, failure):
        failure.trap(error.ConnectError)
        try:
            self.socksPort = self.socksPortIter.next()
        except StopIteration:
            return failure
        d = self._try_connect()
        d.addErrback(self._retry_socks_port)
        return d
