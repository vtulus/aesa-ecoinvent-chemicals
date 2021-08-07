# -*- coding: utf-8 -*-
"""
Adapted from https://stackoverflow.com/a/51028921/14485040

This script has to be included in the `notebooks` directory and
has to be imported (first line) in every notebook
which uses scripts from `src` directory
"""

import sys
import os

module_path = os.path.abspath(os.path.join(".."))
# `..` indicate a relative path to `src` directory
if module_path not in sys.path:
    sys.path.append(module_path)
