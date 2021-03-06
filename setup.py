#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

import versioneer
versioneer.versionfile_source = 'obfsproxy/_version.py'
versioneer.versionfile_build = 'obfsproxy/_version.py'
versioneer.tag_prefix = 'pyobfsproxy-' # tags are like 1.2.0
versioneer.parentdir_prefix = 'pyobfsproxy-' # dirname like 'myproject-1.2.0'


setup(
    name = "pyobfsproxy",
    author = "asn",
    author_email = "asn@torproject.org",
    description = ("A pluggable transport proxy written in Python"),
    license = "BSD",
    keywords = ['tor', 'obfuscation', 'twisted'],

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'pyobfsproxy = obfsproxy.pyobfsproxy:run'
            ]
        }
)
