import random
from graphql import GraphQLArgument, GraphQLNonNull, GraphQLInt
from graphene_custom_directives.middleware import BaseCustomDirective


__author__ = 'ekampf'


class ShuffleDirective(BaseCustomDirective):
    @staticmethod
    def process(value, directive, root, args, context, info):
        if value:
            random.shuffle(value)

        return value


class SampleDirective(BaseCustomDirective):
    @staticmethod
    def get_args():
        return {
            'k': GraphQLArgument(
                type=GraphQLNonNull(GraphQLInt),
                description='Value to default to',
            ),
        }

    @staticmethod
    def process(value, directive, root, args, context, info):
        k_argument = [arg for arg in directive.arguments if arg.name.value == 'k'][0]
        k = int(k_argument.value.value)
        return random.sample(value, k) if value else value
