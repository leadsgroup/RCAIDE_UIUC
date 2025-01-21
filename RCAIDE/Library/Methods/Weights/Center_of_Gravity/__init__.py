# RCAIDE/Library/Methods/Weights/Center_of_Gravity/__init__.py
# 


"""
Methods for computing the center of gravity (CG) locations for vehicle components and the overall vehicle. 
This module provides functions to calculate individual component CG positions and aggregate them into a total vehicle CG.

See Also
--------
RCAIDE.Methods.Weights.Correlation_Buildups
RCAIDE.Methods.Weights.Physics_Based_Buildups
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_component_centers_of_gravity import compute_component_centers_of_gravity
from .compute_vehicle_center_of_gravity import compute_vehicle_center_of_gravity
