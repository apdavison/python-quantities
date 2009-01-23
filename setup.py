#!/usr/bin/env python

#+
#
# This file is part of quantities, a python package for handling physical
# quantities based on numpy.
#
# Copyright (C) 2009 Darren Dale
# http://packages.python.org/quantities
# License: BSD  (See doc/users/license.rst for full license)
#
# $Date$
#
#-

"""
    setup script for the quantities package

    options:

    * Unicode

      Units are presented using unicode by default, but this can be problematic
      on some platforms like windows. Unicode can be disabled, and units
      presented as simple ASCII text by passing the "--no-unicode" flag to the
      setup script::

        python setup.py build --no-unicode
"""

from __future__ import with_statement

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from numpy.distutils.core import setup

if os.path.exists('MANIFEST'): os.remove('MANIFEST')

MIN_NUMPY = '1.2'

with file('quantities-data/NIST_codata.txt') as f:
    data = f.read()
data = data.split('\n')[10:-1]

with file('quantities/constants/_codata.py', 'w') as f:
    f.write('# THIS FILE IS AUTOMATICALLY GENERATED\n')
    f.write('# ANY CHANGES MADE HERE WILL BE LOST\n\n')
    f.write('physical_constants = {}\n\n')
    for line in data:
        name = line[:55].rstrip().replace('mag.','magnetic')
        name = name.replace('mom.', 'moment')
        val = line[55:77].replace(' ','').replace('...','')
        prec = line[77:99].replace(' ','').replace('(exact)', '0')
        unit = line[99:].rstrip().replace(' ', '*').replace('^', '**')
        d = "{'value': %s, 'precision': %s, 'units': '%s'}"%(val, prec, unit)
        f.write("physical_constants['%s'] = %s\n"%(name, d))

USE_UNICODE = True
for arg in sys.argv[:]:
    if arg.find('--no-unicode') == 0:
        USE_UNICODE = False
        sys.argv.remove(arg)
with file('quantities/config.py', 'w') as f:

    f.write('# THIS FILE IS AUTOMATICALLY GENERATED AT BUILD TIME\n')
    f.write('# ANY CHANGES MADE HERE WILL BE LOST\n')
    f.write('# PASS --no-unicode FLAG TO setup.py TO DISABLE UNICODE\n\n')
    f.write('USE_UNICODE = %s'% USE_UNICODE)

desc = 'Support for physical quantities based on the popular numpy library'
long_desc = "Quantities is designed to handle arithmetic and conversions of \
physical quantities, which have a magnitude, dimensionality specified by \
various units, and possibly an uncertainty. Quantities is based on the popular \
numpy library. It is undergoing active development, and while the current \
features and API are fairly stable, test coverage is far from complete and the \
package is not ready for production use."
classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Education',
    'Topic :: Scientific/Engineering',
]

for line in file('quantities/__init__.py').readlines():
    if line[:11] == '__version__':
        exec(line)
        break

setup(
    name = "quantities",
    version = __version__,
    author = 'Darren Dale',
    author_email = 'dsdale24@gmail.com',
    description = desc,
    keywords = ['quantities', 'physical quantities', 'units'],
    license = 'BSD',
    long_description = long_desc,
    classifiers = classifiers,
    platforms = 'Any',
    requires = ['numpy'],
    url = "http://packages.python.org/quantities",
    packages = [
        'quantities',
        'quantities.units',
        'quantities.constants',
        'quantities.tests'
    ],
    requires = ['numpy (>=%s)' % MIN_NUMPY],
)
