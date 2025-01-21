# RCAIDE/Library/Methods/Weights/Correlations/FLOPS/__init__.py
# 

"""
Methods for computing component weights using NASA's Flight Optimization System (FLOPS) 
correlations. This module provides weight estimation techniques derived from NASA's 
extensive aircraft database and analysis tools.

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

from .compute_fuselage_weight            import compute_fuselage_weight          
from .compute_horizontal_tail_weight     import compute_horizontal_tail_weight  
from .compute_operating_items_weight     import compute_operating_items_weight   
from .compute_landing_gear_weight        import compute_landing_gear_weight      
from .compute_payload_weight             import compute_payload_weight           
from .compute_propulsion_system_weight   import compute_propulsion_system_weight 
from .compute_systems_weight             import compute_systems_weight           
from .compute_vertical_tail_weight       import compute_vertical_tail_weight     
from .compute_wing_weight                import compute_wing_weight              