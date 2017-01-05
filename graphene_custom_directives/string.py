from graphql import GraphQLArgument, GraphQLNonNull, GraphQLString
from graphene_custom_directives.middleware import BaseCustomDirective

__author__ = 'ekampf'


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


class NumberDirective(BaseCustomDirective):
    """
    Number formatting
    """
    @staticmethod
    def get_args():
        return {
            'as': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString),
                description='Value to default to',
            ),
        }

    @staticmethod
    def process(value, directive, root, args, context, info):
        as_argument = [arg for arg in directive.arguments if arg.name.value == 'as'][0]
        return format(float(value or 0), as_argument.value.value)


class LowercaseDirective(BaseCustomDirective):
    """
    Lowercases result.
    """
    @staticmethod
    def process(value, directive, root, args, context, info):
        value = value if isinstance(value, basestring) else str(value)
        return value.lower()


class UppercaseDirective(BaseCustomDirective):
    """
    Uppercases result.
    """

    @staticmethod
    def process(value, directive, root, args, context, info):
        value = value if isinstance(value, basestring) else str(value)
        return value.upper()


class CapitalizeDirective(BaseCustomDirective):
    """
    Capitalize result.
    """

    @staticmethod
    def process(value, directive, root, args, context, info):
        value = value if isinstance(value, basestring) else str(value)
        return value.capitalize()



