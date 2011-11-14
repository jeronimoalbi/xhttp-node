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
import glob
import logging
import os
import simplejson

from xhttpnode import error
from xhttpnode import schema
from xhttpnode.request import MODE_INFO
from xhttpnode.request import MODE_SCHEMA
from xhttpnode.request import MODE_VERSION
from xhttpnode.response import Response

LOG = logging.getLogger(__name__)


class Node(object):
    """Nose server that handles XHTTP requests"""
    #XHTTP schema version supported by current node
    schema_version = "1.0"

    def __init__(self, service_dir):
        #TODO: implement dynamic XML file update
        self.service_dir = service_dir
        self.services = {}

        #parse each schema file to get available services
        file_pattern = os.path.join(service_dir, "*.xml")
        service_schema_file_list = glob.glob(file_pattern)
        for schema_file in service_schema_file_list:
            file_name = os.path.basename(schema_file)
            name = os.path.splitext(file_name)[0]
            LOG.debug(u"Parsing schema for service '%s'", name)
            #TODO: Implement checking of schema versions in each file
            self.services[name] = schema.parse_schema_document(schema_file)

    def _get_x_version(self, request):
        version = request.x_version
        if not version:
            raise error.InternalExceptionError("Missing X-Version header")

        LOG.debug(u"Validating X-Version %s", version)
        if version != self.schema_version:
            headers = {}
            headers['X-Version'] = self.schema_version

            raise error.VersionNotSupportedError(headers=headers)

        return version

    def _get_x_services(self, request):
        service_info = request.x_service
        if not service_info:
            raise error.ServiceNotSpecifiedError()
        
        #TODO: See how to use the version given here
        (service_name, version) = service_info
        LOG.debug(u"Validating X-Service %s", service_name)
        if service_name not in self.services:
            raise error.ServiceNotFoundError()

        return self.services[service_name]

    def get_schema(self, request):
        """Get schema for current XHTTP request

        XHTTP request headers are validated before getting schema.        
        Raise error.XHTTPError type exceptions when invalid request is found.

        """
        service = self._get_x_service(request)
        version = self._get_x_version(request)
        if version not in service:
            headers = {}
            headers['X-Version'] = self.schema_version

            raise error.VersionNotSupportedError(headers=headers)

        return service[version]

    def get_request_controller(self, request):
        """Get the controller that will handle the XHTTP request contents"""

        controller = None
        #schema = self.get_schema(request)

        return controller

    def process_mode_version(self, request):
        services = self._get_x_services(request)
        version = self._get_x_version(request)
        service_name = services[version]['info']['service']
        LOG.debug(u"X-Mode: version, for service %s[%s]", service_name, version)
        version_list = [version for version in services.keys()
                                if not version.startswith("_")]
        version_list.sort()
        
        return version_list

    def process_mode_info(self, request):
        services = self._get_x_services(request)
        version = self._get_x_version(request)
        service_name = services[version]['info']['service']
        LOG.debug(u"X-Mode: info, for service %s[%s]", service_name, version)
        #get service schema info for current version
        info = services[version]['info']
        #sort info list by field name
        info_list = info.items()
        info_list.sort(lambda info, info2: cmp(info[0], info2[0]))
        
        return info_list

    def process_mode_schema(self, request):
        pass
    
    def process_request(self, request):
        content = None
        mode = request.x_mode
        if mode == MODE_VERSION:
            content = self.process_mode_version(request)
        elif mode == MODE_INFO:
            content = self.process_mode_info(request)
        elif mode == MODE_SCHEMA:
            content = self.process_mode_schema(request)

        if not content:
            if not mode:
                message = u"Request has not X-Mode"
            else:
                message = u"Invalid X-Mode %s" % mode

            raise error.InternalExceptionError(message)

        body = simplejson.dumps(content, separators=(",", ":"))
        response = Response(body=body)
        response.content_type = "application/json; charset=utf-8"
        
        return response

