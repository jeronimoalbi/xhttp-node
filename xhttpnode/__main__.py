# -*- coding: utf8 -*-
#
# Copyright (c) 2011, Jeronimo Jose Albi <jeronimo.albi@gmail.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of copyright holders nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import logging
import sys

from wsgiref.simple_server import make_server

from xhttpnode import app
from xhttpnode.middleware import XHTTPNodeMiddleware


def start_node(service_dir, host='localhost', port=8888):
    """Start serving XHTTP requests
    
    By default server listens on localhost:8888.

    """
    #create the WSGI application that will handle requests
    application = app.Application()
    application = XHTTPNodeMiddleware(service_dir, app=application)
    #create and start a WSGI server
    server = make_server(host, port, application)
    try:
        print "Listening for XHTTP request on %s:%s" % (host, port)
        print "Use Control-C to exit."
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
        #start a new line
        print


if __name__ == "__main__":
    #TODO: Parse arguments to support other params like port or host
    if len(sys.argv) != 2:
        print "Usage: python -m xhttpnode SERVICE_DIR"
        sys.exit(1)

    #TODO: use debugging when debug argument is available
    logging.basicConfig(level=logging.DEBUG)

    service_dir = sys.argv[1]
    start_node(service_dir)

