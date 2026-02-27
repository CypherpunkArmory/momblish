# -*- coding: utf-8 -*-
from importlib.metadata import PackageNotFoundError, version
from momblish.momblish import Momblish

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:
    __version__ = 'unknown'
finally:
    del version, PackageNotFoundError
