#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_graphene-custom-directives
----------------------------------

Tests for `graphene-custom-directives` module.
"""

import graphene
from graphene import ObjectType, Field, String

import unittest

from graphene_custom_directives import CustomDirectivesMiddleware, LowercaseDirective


class PersonType(ObjectType):
    name = String()


class QueryRoot(ObjectType):
    person = Field(PersonType)

    def resolve_person(self, *_):
        return PersonType(name="ErAn")



class TestGrapheneCustomDirectives(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        schema = graphene.Schema(query=QueryRoot, directives=[LowercaseDirective()])
        result = schema.execute('''
            {
                person {
                    name @lowercase
                }
            }
        ''', middleware=[CustomDirectivesMiddleware()])

        if result.errors:
            print result.errors

        self.assertIsNotNone(result.errors)

        person = result.data['person']
        self.assertEqual(person['name'], 'eran')


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
