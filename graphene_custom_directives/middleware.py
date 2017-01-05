# -*- coding: utf-8 -*-
from graphql import DirectiveLocation, GraphQLDirective
from promise import Promise

__author__ = 'ekampf'

class CustomDirectivesMiddleware(object):
    def resolve(self, next, root, args, context, info):
        result = next(root, args, context, info)
        return result.then(
            lambda resolved: self.__process_value(resolved, root, args, context, info),
            lambda error: Promise.rejected(error)
        )

    def __process_value(self, value, root, args, context, info):
        field = info.field_asts[0]
        if not field.directives:
            return value

        for directive in field.directives:
            directive_class = CustomDirectiveMeta.REGISTRY[directive.name.value]
            return directive_class.process(value, directive, root, args, context, info)


class CustomDirectiveMeta(type):
    REGISTRY = {}  # Maps between ndb.Model to its GraphQL type

    def __new__(mcs, name, bases, attrs):
        newclass = super(CustomDirectiveMeta, mcs).__new__(mcs, name, bases, attrs)
        if name != 'BaseCustomDirective':
            mcs.register(newclass)
        return newclass

    @classmethod
    def register(mcs, target):
        mcs.REGISTRY[target.get_name()] = target

    @classmethod
    def get_all_directives(cls):
        return [d() for d in cls.REGISTRY.values()]


class BaseCustomDirective(GraphQLDirective):
    __metaclass__ = CustomDirectiveMeta

    def __init__(self):
        super(BaseCustomDirective, self).__init__(
            name=self.get_name(),
            description=self.__doc__,
            args=self.get_args(),
            locations=[
                DirectiveLocation.FIELD
            ]
        )

    @classmethod
    def get_name(cls):
        return cls.__name__.replace('Directive', '').lower()

    @staticmethod
    def get_args():
        return {}

