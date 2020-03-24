# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_namespace_packages

with open(os.path.join('README.md'), 'r') as file:
    long_description = file.read()

with open(os.path.join('.', 'qudi', 'core', 'VERSION.txt'), 'r') as file:
    version = file.read().strip()

# packages = ['qudi', 'qudi.gui', 'qudi.logic', 'qudi.hardware', 'qudi.interface']

setup(name='qudi-module-lib',
      version=version,
      packages=find_namespace_packages(),
      description='Qudi module library for various experiments',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Ulm-IQO/qudi',
      keywords=['diamond',
                'quantum',
                'confocal',
                'experiment',
                'lab',
                'laboratory',
                'instrumentation',
                'instrument',
                'modular'
                ],
      license='GPLv3',
      install_requires=['qudi @ git+https://github.com/Neverhorst/qudi-core.git@master#egg=qudi'],
      python_requires='~=3.7',
      zip_safe=False
      )
