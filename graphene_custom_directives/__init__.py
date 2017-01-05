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


class DefaultDirective(BaseCustomDirective):
    """
    Default to given value if None
    """
    @staticmethod
    def get_args():
        return {
            'to': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString),
                description='Value to default to',
            ),
        }


    @staticmethod
    def process(value, directive, root, args, context, info):
        if value is None:
            to_argument = [arg for arg in directive.arguments if arg.name.value == 'to'][0]
            return to_argument.value.value

        return value


class LowercaseDirective(BaseCustomDirective):
    """
    Lowercases result.
    """
    @staticmethod
    def process(value, directive, root, args, context, info):
        if isinstance(value, basestring):
            return value.lower()

        return value


class UppercaseDirective(BaseCustomDirective):
    """
    Uppercases result.
    """

    @staticmethod
    def process(value, directive, root, args, context, info):
        if isinstance(value, basestring):
            return value.upper()

        return value


class CapitalizeDirective(BaseCustomDirective):
    """
    Capitalize result.
    """

    @staticmethod
    def process(value, directive, root, args, context, info):
        if isinstance(value, basestring):
            return value.capitalize()

        return value
