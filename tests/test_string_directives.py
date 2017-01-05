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


class TestStringDirectives(unittest.TestCase):

    def testDefault_returnsDefaultIfNone(self):
        result = self.__execute('{ stringValue @default(to: "YES") }')
        self.assertEqual(result.data['stringValue'], 'YES')

        result = self.__execute('{ stringValue(value: "NO") @default(to: "YES") }')
        self.assertEqual(result.data['stringValue'], 'NO')

    def testNumber_formatsANumberString(self):
        result = self.__execute('{ stringValue(value: "1345.16") @number(as: "0,.1f")}')
        self.assertEqual(result.data['stringValue'], '1,345.2')

    def testLowercase_formatsANumberString(self):
        result = self.__execute('{ stringValue(value: "FOO BAR") @lowercase }')
        self.assertEqual(result.data['stringValue'], 'foo bar')

    def testUppercase_formatsANumberString(self):
        result = self.__execute('{ stringValue(value: "Foo Bar") @uppercase }')
        self.assertEqual(result.data['stringValue'], 'FOO BAR')

    def testCapitalize_formatsANumberString(self):
        result = self.__execute('{ stringValue(value: "FOO BaR") @capitalize }')
        self.assertEqual(result.data['stringValue'], 'Foo bar')

    def __execute(self, query):
        result = schema.execute(query, middleware=[CustomDirectivesMiddleware()])

        if result.errors:
            print result.errors

        self.assertFalse(bool(result.errors))
        return result
