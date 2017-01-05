import unittest

import graphene
from graphene import ObjectType, Argument, List, String, Int

from graphene_custom_directives import CustomDirectiveMeta, CustomDirectivesMiddleware

__author__ = 'ekampf'


class QueryRoot(ObjectType):
    list_value = List(Int, value=Argument(List(Int)))

    @graphene.resolve_only_args
    def resolve_list_value(self, value=None):
        return value

schema = graphene.Schema(query=QueryRoot, directives=CustomDirectiveMeta.get_all_directives())


class TestListDirectives(unittest.TestCase):

    def testShuffle(self):
        result = self.__execute('{ listValue(value: [1, 2, 3]) @shuffle }')
        self.assertEqual(set(result.data['listValue']), {1, 2, 3})
        self.assertNotEqual(result.data['listValue'], [1, 2, 3])

        result = self.__execute('{ listValue(value: []) @shuffle }')
        self.assertFalse(bool(result.data['listValue']))

    def testSample(self):
        result = self.__execute('{ listValue(value: [1, 2, 3]) @sample(k: 1) }')
        self.assertEqual(len(result.data['listValue']), 1)
        self.assertIn(result.data['listValue'][0], [1, 2, 3])

    def __execute(self, query):
        result = schema.execute(query, middleware=[CustomDirectivesMiddleware()])
        self.assertFalse(bool(result.errors))
        return result
