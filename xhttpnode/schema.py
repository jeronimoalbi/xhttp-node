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
import os

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

LOG = logging.getLogger(__name__)


class SchemaParseError(Exception):
    """Base exception for XHTTP schema parse errors"""


def ns(tag_name):
    """Get a tag name inside xhttp namespace

    Return:  A string.

    """
    return "{http://www.xhttp.org/schema}%s" % tag_name


def parse_action_element(action_element):
    """Parse an xhttp:action Element
    
    Return: A dictionary.

    """
    exc_tag = ns('exception')
    arg_tag = ns('argument')
    return_tag = ns('return')
    action = {}
    action.update(action_element.attrib)

    #get return type
    return_iter = action_element.iter(return_tag)
    return_element = list(return_iter)[0]
    action['return'] = return_element.attrib['type']

    #get action exceptions
    action_exceptions = action['exceptions'] = {}
    for exc_element in action_element.iter(exc_tag):
        exception_code = exc_element.attrib['code']
        action_exceptions[exception_code] = exc_element.attrib.copy()

    #get action arguments
    action_args = action['args'] = {}
    for arg_element in action_element.iter(arg_tag):
        arg_name = arg_element.attrib['name']
        action_args[arg_name] = arg_element.attrib.copy()

    return action


def parse_schema_element(schema_element):
    """Parse an xhttp:schema Element
    
    Return: A dictionary.

    """
    info_tag = ns('info')
    action_tag = ns('action')
    schema = {}
    schema.update(schema_element.attrib)
    
    #get schema information
    schema_info = schema['info'] = {}
    for info_element in schema_element.iter(info_tag):
        info_name = info_element.attrib['name']
        info_value = info_element.attrib['value']
        schema_info[info_name] = info_value

    #get schema actions
    schema_actions = schema['actions'] = {}
    for action_element in schema_element.iter(action_tag):
        action_name = action_element.attrib['name']
        schema_actions[action_name] = parse_action_element(action_element)

    return schema


def parse_schema_tree(tree):
    """Parse an ElementTree of schema nodes

    Result dictionary have schema versions as key and schema info as values.
    
    Return: A dictionary.

    """
    schema_tag = ns('schema')
    schemas = {}

    for schema_element in tree.iter(schema_tag):
        version = schema_element.attrib['version']
        schemas[version] = parse_schema_element(schema_element)

    return schemas


def parse_schema_document(file_name):
    """Parse an XHTTP schema document
    
    Return: A dictionary.

    """
    file_name = os.path.abspath(file_name)
    try:
        tree = ET.parse(file_name)
        schemas = parse_schema_tree(tree)
        #save meta schema file information
        meta = schemas['__meta__'] = {}
        meta['mtime'] = os.path.getmtime(file_name)
        meta['file'] = file_name
    except Exception, exc:
        msg = ("Unable to parse XHTTP schema file %s\n[error] %s" 
               % (file_name, exc))

        raise SchemaParseError(msg)

    return schemas


if __name__ == "__main__":
    from pprint import pprint

    schemas = parse_schema_document('schema.xml')
    pprint(schemas)

