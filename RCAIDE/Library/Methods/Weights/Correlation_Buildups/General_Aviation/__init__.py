# RCAIDE/Library/Methods/Weights/Correlations/General_Aviation/__init__.py
# 

"""
This module provides weight estimation methods for general aviation aircraft components 
using empirical correlations. The methods are calibrated for light aircraft ranging 
from single-engine piston to light business jets.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS
    Weight estimation methods for transport aircraft
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered
    Weight estimation methods for ultra-lightweight aircraft
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_operating_empty_weight import compute_operating_empty_weight
from .compute_landing_gear_weight    import compute_landing_gear_weight    
from .compute_payload_weight         import compute_payload_weight         
from .compute_systems_weight         import compute_systems_weight         
from .compute_horizontal_tail_weight import compute_horizontal_tail_weight 
from .compute_vertical_tail_weight   import compute_vertical_tail_weight   
from .compute_fuselage_weight        import compute_fuselage_weight        
from .compute_main_wing_weight       import compute_main_wing_weight       
