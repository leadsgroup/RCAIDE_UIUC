# RCAIDE/Library/Methods/Weights/Buildups/eVTOL/__init__.py
# 

"""
This module provides functions for physics-based weight estimation of electric aircraft. It includes methods for computing 
operating empty weight and iteratively converging weight buildups based on physical principles and constraints.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_operating_empty_weight          import compute_operating_empty_weight
from .converge_physics_based_weight_buildup   import converge_physics_based_weight_buildup