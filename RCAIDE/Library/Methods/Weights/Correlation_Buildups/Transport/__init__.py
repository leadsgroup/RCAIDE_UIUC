# RCAIDE/Library/Methods/Weights/Correlations/Transport/__init__.py
# 

"""
Collection of aircraft weight estimation methods for transport category aircraft. 
This module provides component weight estimation functions based on empirical 
correlations derived from historical transport aircraft data. The methods include 
weight estimations for fuselage, wings, tails, operating items, and empty weight 
calculations.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Raymer
RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_fuselage_weight          import compute_fuselage_weight
from .compute_horizontal_tail_weight   import compute_horizontal_tail_weight
from .compute_operating_items_weight   import compute_operating_items_weight
from .compute_vertical_tail_weight     import compute_vertical_tail_weight
from .compute_operating_empty_weight   import compute_operating_empty_weight