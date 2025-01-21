# RCAIDE/Library/Methods/Weights/Correlations/Common/__init__.py
# 

"""
Methods for computing component weights that are common across different aircraft configurations. 
This module provides weight estimation techniques for standard aircraft components and systems 
that share similar design principles regardless of aircraft type.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport
    Transport-specific weight methods
RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation
    General aviation weight methods
RCAIDE.Library.Methods.Weights.Correlation_Buildups.BWB
    BWB-specific weight methods
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_landing_gear_weight        import compute_landing_gear_weight    
from .compute_payload_weight             import compute_payload_weight         
from .compute_main_wing_weight           import compute_main_wing_weight       
from .compute_operating_empty_weight     import compute_operating_empty_weight
from .compute_systems_weight             import compute_systems_weight