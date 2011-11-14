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
from simplejson import dumps


class XHTTPError(Exception):
    """Base XHTTP error class"""
    code = 0
    message = ""

    def __init__(self, headers=None):
        self.headers = []
        if isinstance(headers, dict):
            self.headers.extend(headers.items())
        elif isinstance(headers, list):
            self.headers.extend(headers)
        else:
            #TODO: Check how to raise an error when headers are not used
            pass

    def __unicode__(self):
        return u"%s %s" % (self.code, self.message)

    def __str__(self):
        return self.header

    def __repr__(self):
        return unicode(self)

    def append_header(self, name, value):
        """Append an HTTP header that has to be returned
        
        Exceptions added here are returned after current exception is raised.

        """
        self.headers.append((name, value))

    @property
    def header(self):
        return unicode(self).encode("utf8")


class ServiceNotSpecifiedError(XHTTPError):
    code = 450
    message = "Service Not Specified"


class ActionNotSpecifiedError(XHTTPError):
    code = 451
    message = "Action Not Specified"


class ServiceNotFoundError(XHTTPError):
    code = 452
    message = "Service Not Found"


class ActionNotFoundError(XHTTPError):
    code = 453
    message = "Action Not Found"


class SchemaNotFoundError(XHTTPError):
    code = 454
    message = "Schema Not Found"


class InternalExceptionError(XHTTPError):
    code = 550
    message = "Exception"

    def __init__(self, message, headers=None):
        if not headers:
            headers = {}

        header_name = "X-Exception"
        header_value = dumps(message)

        if isinstance(headers, dict):
            headers[header_name] = header_value
        elif isinstance(headers, list):
            headers.append((header_name, header_value))

        super(InternalExceptionError, self).__init__(headers=headers)


class VersionNotSupportedError(XHTTPError):
    code = 551
    message = "XHTTP Version Not Supported"


class XHTTPProtocolError(XHTTPError):
    """Base exception class for XHTTP protocol errors"""


class Error101(XHTTPProtocolError):
    code = 101
    message = "Cannot process response if request not ready"


class Error102(XHTTPProtocolError):
    code = 102
    message = "Cannot return value of incomplete response"


class Error103(XHTTPProtocolError):
    code = 103
    message = "Redirection exception"


class Error104(XHTTPProtocolError):
    code = 104
    message = "Client exception"


class Error105(XHTTPProtocolError):
    code = 105
    message = "Server exception"


class Error106(XHTTPProtocolError):
    code = 106
    message = "Missing required arguments"


class Error107(XHTTPProtocolError):
    code = 107
    message = "Invalid argument passed"


class Error108(XHTTPProtocolError):
    code = 108
    message = "Unknown exception"


class Error109(XHTTPProtocolError):
    code = 109
    message = "Incompatible protocol version"

