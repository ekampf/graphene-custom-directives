import math
from graphene_custom_directives.middleware import BaseCustomDirective

__author__ = 'ekampf'


class FloorDirective(BaseCustomDirective):
    """
    Capitalize result.
    """

    @staticmethod
    def process(value, directive, root, args, context, info):
        return math.floor(value)


