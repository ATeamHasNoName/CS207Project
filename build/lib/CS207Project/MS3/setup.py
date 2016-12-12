
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for Team 8 CS207Project project.
    This file was generated with PyScaffold 2.5.7, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup

packages = ['CS207Project','CS207Project.TimeSeries','cs207project.FileStorageManager',
'cs207project.DB','cs207project.SimSearch']

def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(setup_requires=['six', 'pyscaffold>=2.5a0,<2.6a0'] + sphinx,
          use_pyscaffold=True, packages=packages)

if __name__ == "__main__":
    setup_package()