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
    number = String()


class QueryRoot(ObjectType):
    person = Field(PersonType)

    def resolve_person(self, *_):
        return PersonType(name="Eran", age=15, number="1314.15")


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
                    number @number(as: "0,.1f")
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
        self.assertEqual(person['number'], '1,314.2')


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
