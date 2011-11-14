# -*- coding: utf8 -*-
import unittest

from xhttpnode import schema
from xhttpnode.schema import ET


class SchemaTestCase(unittest.TestCase):
    """Test case for the schema module"""

    def test_parse_schema_tree(self):
        #create a simple tree with a single schema node
        element = ET.XML("""
            <xhttp xmlns:xhttp="http://www.xhttp.org/schema" version="1.0">
                <xhttp:schema version="1.0"></xhttp:schema>
                <xhttp:schema version="2.0"></xhttp:schema>
            </xhttp>
        """)
        tree = ET.ElementTree(element=element)
        #get schemas dictionary from the tree
        schemas = schema.parse_schema_tree(tree)

        #there should be only two schemas
        self.assertEqual(len(schemas), 2)
        #schema version 2.0 must be available
        self.assertIn("2.0", schemas)

    def test_parse_schema_element(self):
        #create a schema node with some info
        element = ET.XML("""
            <xhttp xmlns:xhttp="http://www.xhttp.org/schema" version="1.0">
                <xhttp:schema version="1.0">
                    <xhttp:info name="link" value="http://www.xhttp.org"/>
                    <xhttp:info name="service" value="example"/>
                    <xhttp:action name="test2" function="test2">
                        <xhttp:exception code="1" message="Empty"/>
                        <xhttp:argument name="dummy" type="4"/>
                        <xhttp:return type="4"/>
                    </xhttp:action>
                </xhttp:schema>
            </xhttp>
        """)
        schema_tag = schema.ns('schema')
        schema_element_list = list(element.iter(schema_tag))
        #get schema dictionary
        schema_dict = schema.parse_schema_element(schema_element_list[0])

        #check some properties that should be available
        schema_dict_expected = {}
        schema_dict_expected['version'] = "1.0"
        schema_dict_expected['link'] = "http://www.xhttp.org"
        schema_dict_expected['service'] = "example"
        self.assertDictContainsSubset(schema_dict_expected, schema_dict)

        #schema should contain 1 actions
        self.assertEqual(len(schema_dict['actions']), 1)

    def test_parse_action_element(self):
        #create an action node with some info
        element = ET.XML("""
            <xhttp xmlns:xhttp="http://www.xhttp.org/schema" version="1.0">
                <xhttp:action name="test" function="test_fn">
                    <xhttp:exception code="1" message="Empty"/>
                    <xhttp:exception code="99" message="Dummy"/>
                    <xhttp:argument name="dummy" type="4"/>
                    <xhttp:return type="4"/>
                </xhttp:action>
            </xhttp>
        """)
        action_tag = schema.ns('action')
        action_element_list = list(element.iter(action_tag))

        #get action dictionary
        action = schema.parse_action_element(action_element_list[0])

        #check some properties that should be available
        action_expected = {}
        action_expected['name'] = "test"
        action_expected['function'] = "test_fn"
        action_expected['return'] = "4"
        self.assertDictContainsSubset(action_expected, action)

        #there should be 2 exceptions
        self.assertEqual(len(action['exceptions']), 2)
        #dummy exception code must be available
        self.assertIn('99', action['exceptions'])
        #check mandatory exception properties
        first_exception = action['exceptions']['99']
        self.assertIn('code', first_exception)
        self.assertIn('message', first_exception)

        #there should be 1 argument
        self.assertEqual(len(action['args']), 1)
        #dummy argument name must be available
        self.assertIn('dummy', action['args'])
        #check mandatory argument properties
        first_argument = action['args']['dummy']
        self.assertIn('name', first_argument)
        self.assertIn('type', first_argument)

