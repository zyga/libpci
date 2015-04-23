#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright 2015 Canonical Ltd.
#
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""setup for python-libpci."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='libpci',
    version='0.1',
    description='Pure-Python, high-level bindings to libpci',
    long_description=readme + '\n\n' + history,
    author='Zygmunt Krynicki',
    author_email='zygmunt.krunicki@canonical.com',
    url='https://github.com/zyga/python-libpci',
    packages=['libpci'],
    package_dir={'libpci': 'libpci'},
    include_package_data=True,
    license="LGPLv3",
    zip_safe=True,
    keywords='libpci binding',
    install_requires=['guacamole'],
    scripts=['pci-lookup'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        ('License :: OSI Approved :: GNU Lesser General Public License v3'
         ' (LGPLv3)'),
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
