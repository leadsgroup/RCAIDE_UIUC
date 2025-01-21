# RCAIDE/Library/Methods/Weights/Correlations/__init__.py
# 

"""
Methods for computing component and total vehicle weights using correlation-based buildup methods. 
This module provides weight estimation techniques for different aircraft categories and configurations.

See Also
--------
RCAIDE.Library.Methods.Weights.Moment_of_Inertia
    Moment of inertia calculations using estimated weights
RCAIDE.Library.Methods.Weights.Center_of_Gravity
    Center of gravity calculations using component weights
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from . import BWB
from . import Common
from . import FLOPS
from . import General_Aviation
from . import Human_Powered
from . import Propulsion
from . import Raymer
from . import Transport
from . import UAV