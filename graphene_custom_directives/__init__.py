# -*- coding: utf-8 -*-
from graphql import DirectiveLocation
from graphql import GraphQLDirective, GraphQLArgument, GraphQLNonNull, GraphQLBoolean, GraphQLString
from promise import Promise

__author__ = 'Eran Kampf'
__email__ = 'eran@ekampf.com'
__version__ = '0.1.0'


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
            return directive_class().process(value, root, args, context, info)


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


class BaseCustomDirective(GraphQLDirective):
    __metaclass__ = CustomDirectiveMeta

    @classmethod
    def get_name(cls):
        return cls.__name__.replace('Directive', '').lower()


class LowercaseDirective(BaseCustomDirective):
    """
    Lowercases result.
    """

    def __init__(self):
        super(self.__class__, self).__init__(
            name=self.get_name(),
            description=self.__doc__,
            args={},
            locations=[
                DirectiveLocation.FIELD
            ]
        )

    def process(self, value, root, args, context, info):
        if isinstance(value, basestring):
            return value.lower()

        return value
