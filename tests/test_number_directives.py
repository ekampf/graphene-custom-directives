import unittest

import graphene
from graphene import ObjectType, Argument, String, Int, Float

from graphene_custom_directives import CustomDirectiveMeta, CustomDirectivesMiddleware

__author__ = 'ekampf'


class QueryRoot(ObjectType):
    string_value = String(value=Argument(String))
    int_value = Int(value=Argument(Int))
    float_value = Float(value=Argument(Float))

    @graphene.resolve_only_args
    def resolve_string_value(self, value=None):
        return value

    @graphene.resolve_only_args
    def resolve_int_value(self, value=None):
        return value

    @graphene.resolve_only_args
    def resolve_float_value(self, value=None):
        return value

schema = graphene.Schema(query=QueryRoot, directives=CustomDirectiveMeta.get_all_directives())


class TestNumberDirectives(unittest.TestCase):

    def testFloor_floatField_floorsValue(self):
        result = self.__execute('{ floatValue(value: 3.14) @floor }')
        self.assertEqual(result.data['floatValue'], 3.0)

    def testFloor_stringField_floorsValue(self):
        result = self.__execute('{ stringValue(value: "3.14") @floor @number(as: "0.0f") }')
        self.assertEqual(result.data['stringValue'], '3')

    def testCeil_floatField_floorsValue(self):
        result = self.__execute('{ floatValue(value: 3.14) @ceil }')
        self.assertEqual(result.data['floatValue'], 4.0)

    def testCeil_stringField_floorsValue(self):
        result = self.__execute('{ stringValue(value: "3.14") @ceil @number(as: "0.4f") }')
        self.assertEqual(result.data['stringValue'], '4.0000')

    def __execute(self, query):
        result = schema.execute(query, middleware=[CustomDirectivesMiddleware()])

        if result.errors:
            print result.errors

        self.assertFalse(bool(result.errors))
        return result
