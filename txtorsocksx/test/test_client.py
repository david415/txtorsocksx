

from twisted.internet import defer
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.python import failure
from twisted.internet.error import ConnectionRefusedError

from txsocksx import client
from txtorsocksx.endpoints import TorClientEndpoint


connectionRefusedFailure = failure.Failure(ConnectionRefusedError())


class FakeTorSocksEndpoint(object):
    def __init__(self, *args, **kw):
        self.host     = args[1]
        self.port     = args[2]
        self.transport = None

        if kw.has_key('failure'):
            self.failure = kw['failure']
        else:
            self.failure = None
        if kw.has_key('acceptPort'):
            self.acceptPort = kw['acceptPort']
        else:
            self.acceptPort = None

    def connect(self, fac):
        self.factory = fac
        if self.acceptPort:
            if self.port != self.acceptPort:
                return defer.fail(self.failure)
        else:
            if self.failure:
                return defer.fail(self.failure)
        self.proto = fac.buildProtocol(None)
        transport = proto_helpers.StringTransport()
        self.proto.makeConnection(transport)
        self.transport = transport
        return defer.succeed(self.proto)


class TestTorClientEndpoint(unittest.TestCase):

    def test_clientConnectionFailed(self):
        """
        This test is equivalent to txsocksx's TestSOCKS4ClientEndpoint.test_clientConnectionFailed
        """
        def FailTorSocksEndpointGenerator(*args, **kw):
            kw['failure'] = connectionRefusedFailure
            return FakeTorSocksEndpoint(*args, **kw)
        endpoint = TorClientEndpoint('', 0, proxyEndpointGenerator=FailTorSocksEndpointGenerator)
        d = endpoint.connect(None)
        return self.assertFailure(d, ConnectionRefusedError)

    def test_defaultFactory(self):
        """
        This test is equivalent to txsocksx's TestSOCKS5ClientEndpoint.test_defaultFactory
        """
        def TorSocksEndpointGenerator(*args, **kw):
            return FakeTorSocksEndpoint(*args, **kw)
        endpoint = TorClientEndpoint('', 0, proxyEndpointGenerator=TorSocksEndpointGenerator)
        endpoint.connect(None)
        self.assertEqual(endpoint.torSocksEndpoint.transport.value(), '\x05\x01\x00')

    def test_goodPortRetry(self):
        """
        This tests that our Tor client endpoint retry logic works correctly.
        We create a proxy endpoint that fires a connectionRefusedFailure
        unless the connecting port matches. We attempt to connect with the
        proxy endpoint for each port that the Tor client endpoint will try.
        """
        success_ports = TorClientEndpoint.socks_ports_to_try
        for port in success_ports:
            def TorSocksEndpointGenerator(*args, **kw):
                kw['acceptPort'] = port
                kw['failure']    = connectionRefusedFailure
                return FakeTorSocksEndpoint(*args, **kw)
            endpoint = TorClientEndpoint('', 0, proxyEndpointGenerator=TorSocksEndpointGenerator)
            endpoint.connect(None)
            self.assertEqual(endpoint.torSocksEndpoint.transport.value(), '\x05\x01\x00')

    def test_badPortRetry(self):
        """
        This tests failure to connect to the ports on the "try" list.
        """
        fail_ports    = [1984, 666]
        for port in fail_ports:
            def TorSocksEndpointGenerator(*args, **kw):
                kw['acceptPort'] = port
                kw['failure']    = connectionRefusedFailure
                return FakeTorSocksEndpoint(*args, **kw)
            endpoint = TorClientEndpoint('', 0, proxyEndpointGenerator=TorSocksEndpointGenerator)
            d = endpoint.connect(None)
            return self.assertFailure(d, ConnectionRefusedError)

    def test_goodNoGuessSocksPort(self):
        """
        This tests that if a SOCKS port is specified,
        we *only* attempt to connect to that SOCKS port.
        """
        def TorSocksEndpointGenerator(*args, **kw):
            kw['acceptPort'] = 6669
            kw['failure']    = connectionRefusedFailure
            return FakeTorSocksEndpoint(*args, **kw)
        endpoint = TorClientEndpoint('', 0, proxyEndpointGenerator=TorSocksEndpointGenerator, socksPort=6669)
        endpoint.connect(None)
        self.assertEqual(endpoint.torSocksEndpoint.transport.value(), '\x05\x01\x00')

    def test_badNoGuessSocksPort(self):
        """
        This tests that are connection fails if we try to connect to an unavailable
        specified SOCKS port... even if there is a valid SOCKS port listening on
        the socks_ports_to_try list.
        """
        def TorSocksEndpointGenerator(*args, **kw):
            kw['acceptPort'] = 9050
            kw['failure']    = connectionRefusedFailure
            return FakeTorSocksEndpoint(*args, **kw)
        endpoint = TorClientEndpoint('', 0, proxyEndpointGenerator=TorSocksEndpointGenerator, socksPort=6669)
        d = endpoint.connect(None)
        self.assertFailure(d, ConnectionRefusedError)
