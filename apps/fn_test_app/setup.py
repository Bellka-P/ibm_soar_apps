#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generated with resilient-sdk v51.0.7.2.16540

from setuptools import setup, find_packages
import glob
import ntpath


def get_module_name(module_path):
    """
    Return the module name of the module path
    """
    return ntpath.split(module_path)[1].split(".")[0]


def snake_to_camel(word):
    """
    Convert a word from snake_case to CamelCase
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


setup(
    name="fn_test_app",
    display_name="Test App",
    version="1.0.2",
    license="MIT",
    author="fn_test_app developers",
    author_email="",
    url="https://www.ibm.com/products/qradar-soar",
    description="Minimal echo function for IBM QRadar SOAR App Host testing",
    long_description="""A minimal IBM QRadar SOAR App Host application containing
one test_echo function with framework-independent echo business logic.""",
    install_requires=[
        "resilient-circuits>=51.0.7.2.0"
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Programming Language :: Python",
    ],
    entry_points={
        "resilient.circuits.components": [
            # When setup.py is executed, loop through the .py files in the components directory and create the entry points.
            "{}FunctionComponent = fn_test_app.components.{}:FunctionComponent".format(snake_to_camel(get_module_name(filename)), get_module_name(filename)) for filename in glob.glob("./fn_test_app/components/[a-zA-Z]*.py")
        ]
        ,
        "resilient.circuits.configsection": ["gen_config = fn_test_app.util.config:config_section_data"],
        "resilient.circuits.customize": ["customize = fn_test_app.util.customize:customization_data"],
        "resilient.circuits.selftest": ["selftest = fn_test_app.util.selftest:selftest_function"]
    }
)
