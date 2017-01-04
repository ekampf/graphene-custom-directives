===============================
Graphene Custom Directives
===============================

.. image:: https://travis-ci.org/ekampf/graphene-custom-directives.svg
        :target: https://travis-ci.org/ekampf/graphene-custom-directives

.. image:: https://coveralls.io/repos/ekampf/graphene-custom-directives/badge.svg?branch=master&service=github 
        :target: https://coveralls.io/github/ekampf/graphene-custom-directives?branch=master

.. image:: https://img.shields.io/pypi/v/graphene-custom-directives.svg
        :target: https://pypi.python.org/pypi/graphene-custom-directives


A collection of custom GraphQL directives for (Graphene)[https://github.com/graphql-python/graphene]

* Free software: BSD license
* Documentation: https://graphene-custom-directives.readthedocs.org.

Examples
--------

```

query { 
    input(value: "FOO BAR") @lowerCase
} 
// => { input: "foo bar" } 

```


