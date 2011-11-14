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

from xhttpnode import error
from xhttpnode.node import Node
from xhttpnode.request import MODE_PERFORM
from xhttpnode.request import Request
from xhttpnode.response import Response

LOG = logging.getLogger(__name__)


class XHTTPNodeMiddleware(object):
    """Middleware class to add support for XHTTP request processing
    
    Middleware will call the application to get the Response instance when
    an application is assigned, or if there is none then middleware will
    handle the call to controller.
    Request instance and controller function are assigned to environment
    in 'xhttp.request' and 'xhttp.controller' before calling application.
    Also the Node instance is saved inside environment in 'xhttp.node'.

    """

    def __init__(self, service_dir, app=None):
        self.application = app
        #create a node to parse XHTTP requests
        self.node = Node(service_dir)

    def __call__(self, environ, start_response):
        request = Request(self.node, environ)

        try:
            if 'X-Mode' not in request.headers:
                raise error.InternalExceptionError("Missing X-Mode header")

            if request.headers['X-Mode'] == MODE_PERFORM:
                #get controller in charge of performing request action
                controller = self.node.get_request_controller(request)
                if self.application:
                    environ['xhttp.controller'] = controller
                    environ['xhttp.request'] = request
                    environ['xhttp.node'] = controller
                    #call application to get the Response instance
                    response = self.application(environ, start_response)
                else:
                    #when no application is assigned to middleware
                    #call controller here to get Response
                    response = controller(request, self.node)
            else:
                #when X-Mode is not perform get contents from server node
                response = self.node.process_request(request)
        except error.XHTTPError, err:
            response = Response.create_from_error(err)
        except Exception, exc:
            LOG.exception("Error processing XHTTP request")
            #for non XHTTP errors return XHTTP Exception response
            message = u"%s: %s" % (exc.__class__.__name__, unicode(exc))
            err = error.InternalExceptionError(message)
            response = Response.create_from_error(err)

        return response(environ, start_response)

