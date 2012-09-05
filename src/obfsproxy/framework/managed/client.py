#!/usr/bin/python
# -*- coding: utf-8 -*-

import monocle
from monocle import _o, Return
monocle.init('tornado')

from monocle.stack import eventloop
from monocle.stack.network import add_service, Service

from obfsproxy.framework.socks import SocksHandler

from obfsproxy.transports.dummy import DummyClient
from obfsproxy.transports.rot13 import Rot13Client
from obfsproxy.transports.dust_transport import DustClient
from obfsproxy.transports.obfs3 import Obfs3Client

from pyptlib.easy.client import init, reportSuccess, reportFailure, \
    reportEnd

import obfsproxy.common.log as log

class TransportLaunchException(Exception):

    pass


class ManagedClient:

    def __init__(self):
        self.handler = SocksHandler()

        self.supportedTransports = {
            'dummy': DummyClient,
            'rot13': Rot13Client,
            'dust': DustClient,
            'obfs3': Obfs3Client,
            }

        managed_info = init(self.supportedTransports.keys())
        if managed_info is None: # XXX what should we return?
            return

        for transport in managed_info['transports']:
            try:
                log.error('Launching %s' % transport)
                self.launchClient(transport, 8182) # XXX hardcoded
                reportSuccess(transport, 5, ('127.0.0.1', 8182), None,
                              None)
            except TransportLaunchException:
                reportFailure(transport, 'Failed to launch')
        reportEnd()

        eventloop.run()

    def launchClient(self, name, port):
        if not name in self.supportedTransports.keys():
            raise TransportLaunchException('Tried to launch unsupported transport %s'
                     % name)

        clientClass = self.supportedTransports[name]
        self.handler.setTransport(clientClass)
        add_service(Service(self.handler.handle, port=port))


