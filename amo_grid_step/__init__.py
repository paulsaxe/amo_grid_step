# -*- coding: utf-8 -*-

"""Top-level package for AMO Grid Step."""

__author__ = """Paul Saxe"""
__email__ = 'psaxe@vt.edu'
__version__ = '0.1.0'

# Bring up the classes so that they appear to be directly in
# the amo_grid_step package.

from amo_grid_step.amo_grid import AMOGrid  # noqa F401
from amo_grid_step.amo_grid_parameters import AMOGridParameters  # noqa F401
from amo_grid_step.amo_grid_step import AMOGridStep  # noqa F401
from amo_grid_step.tk_amo_grid import TkAMOGrid  # noqa F401

properties = {
    "Central grid size": {
        "description": "Number of points in the central grid",
        "dimensionality": "scalar",
        "type": "integer"
    },
    "Atomic grid size": {
        "description": "Number of points in the central grid",
        "dimensionality": "scalar",
        "type": "integer"
    },
    "Sphere test": {
        "description": "Percent error for integral over sphere",
        "dimensionality": "scalar",
        "type": "float"
    },
    "Yukawa test": {
        "description": "Percent error for integral of Yukawa function",
        "dimensionality": "scalar",
        "type": "float"
    },
    "Gaussian test": {
        "description": "Percent error for integral over Gaussian",
        "dimensionality": "scalar",
        "type": "float"
    }
}
