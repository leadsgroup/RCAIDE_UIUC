# RCAIDE/Library/Methods/Weights/Correlations/Human_Powered/__init__.py
# 

"""
This module provides weight estimation methods for human-powered aircraft components 
using empirical correlations. These methods are specifically calibrated for 
ultra-lightweight aircraft designs where minimizing structural weight while maintaining 
adequate strength is critical.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS
    Weight estimation methods for conventional aircraft
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Raymer
    Weight estimation methods using Raymer correlations
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_operating_empty_weight    import compute_operating_empty_weight
from .compute_fuselage_weight           import compute_fuselage_weight
from .compute_tail_weight               import compute_tail_weight
from .compute_wing_weight               import compute_wing_weight