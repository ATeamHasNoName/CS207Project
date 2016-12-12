# -*- coding: utf-8 -*-
import MS1
import MS2
import MS3
import SimSearch

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
