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

Number Formatting
-----------------

* Floor

.. code:: graphql

    query { 
        stringValue(value: "3.14") @floor
        floatValue(value: 3.14) @floor
    } 
    
    // => { stringValue: "3.0", floatValue: 3.0 } 
    
* Ceil

.. code:: graphql

    query { 
        stringValue(value: "3.14") @ceil
        floatValue(value: 3.14) @ceil
    } 
    
    // => { stringValue: "4.0", floatValue: 4.0 } 

String formatting directives
----------------------------
* Default value:

.. code:: graphql

    query { 
        input @default(to: "YEAH")
    } 
    
    // => { input: "YEAH" } 
    
* Base64 encode

.. code:: graphql

    query {
        stringValue(value: "YES") @base64 
    }

    // => { input: "Tm9uZQ==" }

    
* Uppercase:

.. code:: graphql

    query { 
        input(value: "FOO BAR") @lowercase
    } 
    
    // => { input: "foo bar" } 

* Lowercase:

.. code:: graphql

    query { 
        input(value: "foo BAR") @uppercase
    } 
    
    // => { input: "FOO BAR" } 

* Capitalize:

.. code:: graphql

    query { 
        input(value: "foo BAR") @capitalize
    } 
    
    // => { input: "Foo Bar" } 
    
* Number formatting

.. code:: graphql

    query { 
        stringValue(value: "3.14") @number(as: "0.4f") 
    }
    
    // => { stringValue: "3.1400" } 

* Currency formatting

.. code:: graphql

    query { 
        stringValue(value: "150000") @currency
    }
    
    // => { stringValue: "$150,000" } 

List Directives
---------------

* Sample

.. code:: graphql

    query { 
        listValue(value: [1, 2, 3]) @sample(k: 1)
    }
    
    // => { listValue: [2] } 
    
* Shuffle

.. code:: graphql

    query { 
        listValue(value: [1, 2, 3]) @shuffle
    }
    
    // => { listValue: [2, 1, 3] } 


Misc.
-----

You can also use multiple directives, executed from left to right:

.. code:: graphql

    query { 
        stringValue(value: "3.14") @ceil @number(as: "0.4f") 
    }
    
    // => { stringValue: "4.0000" } 
