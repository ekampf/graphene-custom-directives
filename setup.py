#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import os
import re
from setuptools import setup
from setuptools.command.test import test as TestCommand

root_dir = os.path.abspath(os.path.dirname(__file__))

def get_build_number():
    fname = 'build.info'
    if os.path.isfile(fname):
        with open(fname) as f:
            build_number = f.read()
            build_number = re.sub("[^a-z0-9]+","", build_number, flags=re.IGNORECASE)
            return '.' + build_number

    return ''

def get_version(package_name):
    build_number = get_build_number()

    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]+build_number

    return '0.1.0' + build_number

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

requirements = [
    'graphene'
]

test_requirements = [
    'pytest'
]

setup(
    name='graphene-custom-directives',
    version=get_version('graphene_custom_directives'),
    description="Graphene Custom Directives",
    long_description=readme + '\n\n' + history,
    author="Eran Kampf",
    author_email='eran@ekampf.com',
    url='https://github.com/ekampf/graphene-custom-directives',
    packages=[
        'graphene_custom_directives',
    ],
    package_dir={'graphene-custom-directives': 'graphene-custom-directives'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='graphene-custom-directives',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
