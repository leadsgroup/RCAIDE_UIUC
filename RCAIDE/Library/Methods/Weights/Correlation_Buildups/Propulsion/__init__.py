# RCAIDE/Library/Methods/Weights/Correlations/Propulsion/__init__.py
# 

"""
Collection of methods for estimating propulsion system weights in aircraft. This module includes correlations 
for various propulsion system types including jet engines, piston engines, electric motors, and their 
integrated installations. The methods are primarily based on empirical correlations derived from historical 
aircraft data.

See Also
--------
RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric
RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from .compute_jet_engine_weight                             import compute_jet_engine_weight
from .compute_piston_engine_weight                          import compute_piston_engine_weight 
from .integrated_propulsion                                 import integrated_propulsion
from .integrated_propulsion_general_aviation                import integrated_propulsion_general_aviation
from .compute_motor_weight                                  import compute_motor_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric   import dynamo_supply_mass_estimation