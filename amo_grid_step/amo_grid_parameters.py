# -*- coding: utf-8 -*-
"""Control parameters for the AMO Grid step in a MolSSI flowchart"""

import logging
import molssi_workflow
import pprint

logger = logging.getLogger(__name__)


class AMOGridParameters(molssi_workflow.Parameters):
    """The control parameters for AMO Grid

    This is a dictionary of Parameters objects, which themselves are
    dictionaries.  You need to replace the 'time' example below with one or
    more definitions of the control parameters for your plugin and application.

    The fields of each Parameter are:

        default: the default value of the parameter, used to reset it
        kind: one of 'integer', 'float', 'string', 'boolean' or 'enum'
        default_units: the default units, used for reseting the value
        enumeration: a tuple of enumerated values. See below for more.
        format_string: a format string for 'pretty' output
        description: a short string used as a prompt in the GUI
        help_text: a longer string to display as help for the user

    While the 'kind' of a variable might be a numeric value, it may still have
    enumerated values, such as 'normal', 'precise', etc. In addition, any
    parameter can be set to a variable of expression, indicated by having '$'
    as the first character in the field.
    """

    parameters = {
        "central grid lmax": {
            "default": 40,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default", ),
            "format_string": "%d",
            "description": "L-max for grid:",
            "help_text": ("The maximum L values for the angular grid.")
        },
        "central grid angular quadrature": {
            "default": "mixed",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("Lebedev", "Gauss", "mixed"),
            "format_string": "s",
            "description": "Angular quadrature:",
            "help_text": ("The quadrature method for the angular grid.")
        },
        "central grid Lebedev rule": {
            "default": 35,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default",),
            "format_string": "d",
            "description": "Lebedev rule to use:",
            "help_text": ("The number of the Lebedev rule to use in the "
                          "angular grid.")
        },
        "central grid phi quadrature": {
            "default": "trapezoidal",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("trapezoidal",),
            "format_string": "s",
            "description": "Quadrature method in phi:",
            "help_text": ("The quadrature method for the phi part of the "
                          "angular grid.")
        },
        "central grid phi n-points": {
            "default": 3,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default",),
            "format_string": "d",
            "description": "Number of points in phi:",
            "help_text": ("The number of points to use in the phi part of the "
                          "angular grid.")
        },
        "central grid theta quadrature": {
            "default": "Legendre",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("Legendre",),
            "format_string": "s",
            "description": "Quadrature method in theta:",
            "help_text": ("The quadrature method for the theta part of the "
                          "angular grid.")
        },
        "central grid theta n-points": {
            "default": 50,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default",),
            "format_string": "d",
            "description": "Number of points in theta:",
            "help_text": ("The number of points to use in the theta part of "
                          "the angular grid.")
        },
        "central grid radial quadrature": {
            "default": "Legendre",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("Legendre", "Gauss"),
            "format_string": "s",
            "description": "Radial quadrature:",
            "help_text": ("The quadrature method for the radial grid.")
        },
        "central grid region n-points": {
            "default": [100, 50],
            "kind": "list",
            "default_units": "",
            "enumeration": ("default", ),
            "format_string": "",
            "description": "Number of points",
            "help_text": ("The number of points in this region of the radial "
                          "grid.")
        },
        "central grid region outer limit": {
            "default": [20.0, 30.0],
            "kind": "list",
            "default_units": "Å",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Outer edge",
            "help_text": ("The outer edge of this region of the radial "
                          "grid.")
        },
        "atomic grid lmax": {
            "default": 3,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default", ),
            "format_string": "%d",
            "description": "L-max for grid:",
            "help_text": ("The maximum L values for the angular grid.")
        },
        "atomic grid angular quadrature": {
            "default": "mixed",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("Lebedev", "Gauss", "mixed"),
            "format_string": "s",
            "description": "Angular quadrature:",
            "help_text": ("The quadrature method for the angular grid.")
        },
        "atomic grid Lebedev rule": {
            "default": 17,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default",),
            "format_string": "d",
            "description": "Lebedev rule to use:",
            "help_text": ("The number of the Lebedev rule to use in the "
                          "angular grid.")
        },
        "atomic grid phi quadrature": {
            "default": "trapezoidal",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("trapezoidal",),
            "format_string": "s",
            "description": "Quadrature method in phi:",
            "help_text": ("The quadrature method for the phi part of the "
                          "angular grid.")
        },
        "atomic grid phi n-points": {
            "default": 3,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default",),
            "format_string": "d",
            "description": "Number of points in phi:",
            "help_text": ("The number of points to use in the phi part of the "
                          "angular grid.")
        },
        "atomic grid theta quadrature": {
            "default": "Legendre",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("Legendre",),
            "format_string": "s",
            "description": "Quadrature method in theta:",
            "help_text": ("The quadrature method for the theta part of the "
                          "angular grid.")
        },
        "atomic grid theta n-points": {
            "default": 10,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("default",),
            "format_string": "d",
            "description": "Number of points in theta:",
            "help_text": ("The number of points to use in the theta part of "
                          "the angular grid.")
        },
        "atomic grid radial quadrature": {
            "default": "Legendre",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": ("Legendre", "Gauss"),
            "format_string": "s",
            "description": "Radial quadrature:",
            "help_text": ("The quadrature method for the radial grid.")
        },
        "atomic grid region n-points": {
            "default": [20],
            "kind": "list",
            "default_units": "",
            "enumeration": ("default", ),
            "format_string": "",
            "description": "Number of points",
            "help_text": ("The number of points in this region of the radial "
                          "grid.")
        },
        "atomic grid region outer limit": {
            "default": [5.0],
            "kind": "list",
            "default_units": "Å",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Outer edge",
            "help_text": ("The outer edge of this region of the radial "
                          "grid.")
        },
        "results": {
            "default": {},
            "kind": "dictionary",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "results",
            "help_text": ("The results to save to variables or in "
                          "tables. ")
        },
        "create tables": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ('yes', 'no'),
            "format_string": "",
            "description": "Create tables as needed:",
            "help_text": ("Whether to create tables as needed for "
                          "results being saved into tables.")
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**AMOGridParameters.parameters, **defaults},
            data=data
        )
