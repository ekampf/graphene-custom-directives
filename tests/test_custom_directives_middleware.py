#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_graphene-custom-directives
----------------------------------

Tests for `graphene-custom-directives` module.
"""

import graphene
from graphene import ObjectType, Field, String, Int

import unittest

from graphene_custom_directives import CustomDirectivesMiddleware, CustomDirectiveMeta


class PersonType(ObjectType):
    name = String()
    age = Int()
    none = String()


class QueryRoot(ObjectType):
    person = Field(PersonType)

    def resolve_person(self, *_):
        return PersonType(name="Eran", age=15)



class TestGrapheneCustomDirectives(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        schema = graphene.Schema(query=QueryRoot, directives=CustomDirectiveMeta.get_all_directives())
        result = schema.execute('''
            {
                person {
                    name @lowercase
                    age
                    none @default(to: "YEAH")
                }
            }
        ''', middleware=[CustomDirectivesMiddleware()])

        if result.errors:
            print result.errors

        self.assertIsNotNone(result.errors)

        person = result.data['person']
        self.assertEqual(person['name'], 'eran')
        self.assertEqual(person['age'], 15)
        self.assertEqual(person['none'], 'YEAH')


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
