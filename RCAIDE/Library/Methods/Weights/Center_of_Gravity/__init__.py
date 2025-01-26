# RCAIDE/Library/Methods/Weights/Center_of_Gravity/__init__.py
# 


"""
This module provides methods for computing and analyzing center of gravity locations for aircraft components and systems. 
It includes functions for determining component CG positions based on empirical correlations and geometric relationships.

See Also
--------
RCAIDE.Library.Methods.Weights.Physics_Based_Buildups
RCAIDE.Library.Methods.Weights.Correlation_Buildups
RCAIDE.Library.Methods.Geometry.Planform
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_component_centers_of_gravity import compute_component_centers_of_gravity
from .compute_vehicle_center_of_gravity import compute_vehicle_center_of_gravity
