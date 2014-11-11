
===========
txtorsocksx
===========


quick start
-----------

you can install txtorsocksx in your python virtual environment like this:

   $ pip install git+https://github.com/david415/txtorsocksx.git


overview
--------

txtorsocksx is a Tor client endpoint and parser for the python Twisted
asynchronous networking framework. To learn more about Twisted endpoints
and parsers see here:

https://twistedmatrix.com/documents/14.0.0/core/howto/endpoints.html

You can write Twisted program in an endpoint agnostic manner... for example
on the client side you can pass Twisted's `clientFromString` a client endpoint
descriptor string and receive from it an endpoint object. A txtorsocksx endpoint
descriptor string looks like this::

    tor:host=timaq4ygg2iegci7.onion:port=80

`clientFromString` uses a Twisted plugin system to load the correct parser
for each endpoint type. The above client endpoint descriptor string has a type
of "tor" and therefore loads the  `txtorsocksx` endpoint parser plugin which is
registered with Twisted's plugin system.

The `txtorsocksx` endpoint wraps the SOCKS 5 endpoint from `txsocksx`... and
unless further endpoint descriptor arguments are specified, will by default
attempt to connect to the local tor process at SOCKS host 127.0.0.1, ports
9050 and then 9150.

Here are two valid example endpoint descriptor strings::

    tor:host=timaq4ygg2iegci7.onion:port=80:socksPort=9050

and ::

    tor:host=timaq4ygg2iegci7.onion:port=80:socksHostname=127.0.0.1:socksPort=9050

``socksUsername`` and ``socksPassword`` arguments can be specified to effectively
tell the Tor process to create a new Tor circuit or to reuse an existing circuit.
Please do not abuse the Tor network and create large numbers of circuits.

::

    tor:host=timaq4ygg2iegci7.onion:port=80:socksUsername=hail:socksPassword=eris



contact
-------

Bugfixes, suggestions and feature requests welcome!

I'd also be interested to hear from developers using this Tor client endpoint
in their software.


  - email dstainton415@gmail.com
  - gpg key ID 0x836501BE9F27A723
  - gpg fingerprint F473 51BD 87AB 7FCF 6F88  80C9 8365 01BE 9F27 A723

