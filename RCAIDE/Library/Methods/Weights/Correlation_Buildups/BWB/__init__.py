# RCAIDE/Library/Methods/Weights/Correlations/BWB/__init__.py
# 


"""
Methods for computing component weights specific to Blended Wing Body (BWB) aircraft configurations. 
This module provides specialized weight estimation techniques that account for the unique structural 
and geometric characteristics of BWB designs.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common
    Shared component weight methods
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport
    Transport aircraft weight methods
"""


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_operating_empty_weight   import compute_operating_empty_weight
from .compute_aft_centerbody_weight    import compute_aft_centerbody_weight
from .compute_cabin_weight             import compute_cabin_weight