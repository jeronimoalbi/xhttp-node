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
from webob import response


class Response(response.Response):
    """Base class for XHTTP responses"""
    
    #default Content-Type for XHTTP responses
    default_content_type = "text/plain"

    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)
        if 'Server' not in self.headers:
            self.headers['Server'] = "XHTTP Python node"

    @classmethod
    def create_from_error(cls, error):
        """Create a new Request from an XHTTP error
        
        This method creates a response initialized with XHTTP error info.

        """
        content_type = "%s; charset=utf-8" % cls.default_content_type

        headers = dict(error.headers)
        headers['Content-Type'] = content_type 
        headers = headers.items()
        status = str(error)

        return cls(headers=headers, status=status, body=status)
 
