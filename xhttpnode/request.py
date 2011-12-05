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
from webob import request

#XHTTP request modes
MODE_VERSION = "version"
MODE_INFO = "info"
MODE_SCHEMA = "schema"
MODE_PERFORM = "perform"


class RequestException(Exception):
    """Base exception for Request errors"""


class Request(request.Request):
    """Base class for XHTTP requests"""

    #default X-Encoding value
    default_x_encoding = "x-user-defined"

    def __init__(self, node, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        self.node = node

    @property
    def x_mode(self):
        """Get XHTTP request X-Mode
        
        Return: A string or MODE_PERFORM when no mode header exists.

        """
        return self.headers.get("X-Mode", MODE_PERFORM)

    @property
    def x_version(self):
        """Get XHTTP request X-Version
        
        Return: A string or None when no version header exists.

        """
        return self.headers.get("X-Version", None)

    @property
    def x_service(self):
        """Get XHTTP request X-Service values
        
        Result tuple has None for version when X-Service specify
        only the service name.

        Return: A tuple with service name and version, or None
        when no service header exists.

        """
        if "X-Service" in self.headers:
            x_service = self.headers['X-Service']
            if ";" in x_service:
                return tuple(x_service.split(";"))
            
            #when no version is available return None instead
            return (x_service, None)
    
    @property
    def x_action(self):
        """Get XHTTP request X-Action
        
        Return: A string or None when no action header exists.

        """
        return self.headers.get("X-Action", None)

    @property
    def x_arguments(self):
        """Get a dictionary with XHTTP request X-Arguments
        
        Returned dictionary has argument name as key
        and argument type as value.

        Return: A dictionary, or None when no arguments header exists.

        """
        if "X-Arguments" not in self.headers:
            return

        arguments = self.headers['X-Arguments']
        arguments = arguments.split(",")
        arguments = [arg.split(";") for arg in arguments]
        #convert argument types to integer and add them to dictionary
        x_args = {}
        for (name, value_type) in arguments:
            try:
                x_args[name] = int(value_type)
            except TypeError:
                msg = u"Invalid XHTTP data type %s for argument %s" \
                    % (name, value_type)

                raise RequestException(msg)

        return x_args
    @property
    def x_arguments_values(self):
        """Get a dictionary with XHTTP request X-Arguments values."""
        x_args_values = {}
        for (name, value_type) in self.x_arguments.items():
            #TODO: get values from request
            pass

        return x_args_values

    @property
    def x_encoding(self):
        """Get XHTTP request X-Encoding
        
        Return: A string.

        """
        return self.headers.get("X-Encoding", self.default_x_encoding)
