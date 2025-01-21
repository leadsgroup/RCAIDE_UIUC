# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/__init__.py 

"""
Methods for computing moments of inertia for various vehicle components and the complete vehicle. This module provides 
functions for calculating mass distribution properties using geometric approximations and analytical methods.

See Also
--------
RCAIDE.Library.Methods.Weights.Center_of_Gravity
RCAIDE.Library.Methods.Weights.Correlations
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_wing_moment_of_inertia     import compute_wing_moment_of_inertia
from .compute_cuboid_moment_of_inertia   import compute_cuboid_moment_of_inertia
from .compute_fuselage_moment_of_inertia import compute_fuselage_moment_of_inertia
from .compute_cylinder_moment_of_inertia import compute_cylinder_moment_of_inertia
from .compute_aircraft_moment_of_inertia import compute_aircraft_moment_of_inertia