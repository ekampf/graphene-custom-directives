import math

from graphql import GraphQLString, GraphQLFloat, GraphQLInt
from graphene_custom_directives.middleware import BaseCustomDirective

__author__ = 'ekampf'


class FloorDirective(BaseCustomDirective):
    """
    Floors value. Supports both String and Float fields.
    """
    @staticmethod
    def process(value, directive, root, args, context, info):
        new_value = math.floor(float(value))
        return str(new_value) if info.return_type == GraphQLString else new_value


