# RCAIDE/Library/Components/Airfoils/__init__.py
# 

"""
Airfoils module providing classes and methods for defining and analyzing aircraft airfoil geometries

This module contains implementations of various airfoil types including general airfoils
and specific NACA series airfoils. It provides functionality for defining airfoil geometry.

Notes
-----
The airfoil classes in this module are designed to work with RCAIDE's aerodynamic analysis
tools and can be integrated into complete aircraft configurations. Airfoil data can be
imported from external sources or generated using geometric definitions.

See Also
--------
RCAIDE.Library.Components.Wings
    Wing components that utilize airfoil definitions
RCAIDE.Framework.Analyses.Aerodynamics
    Aerodynamic analysis tools that work with airfoil components
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Airfoil               import Airfoil
from .NACA_4_Series_Airfoil import NACA_4_Series_Airfoil
from .Biconvex_Airfoil      import Biconvex_Airfoil