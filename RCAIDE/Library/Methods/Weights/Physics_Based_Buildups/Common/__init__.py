# RCAIDE/Library/Methods/Weights/Buildups/Common/__init__.py
# 

"""
Collection of fundamental physics-based weight estimation methods that can be applied across different aircraft types. 
These methods calculate component weights using first principles, structural mechanics, and material properties rather 
than empirical correlations. The module includes methods for primary structural components (wings, booms, fuselages, 
rotors) and systems (wiring).

See Also
--------
RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common
RCAIDE.Library.Attributes.Materials
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_boom_weight        import compute_boom_weight
from .compute_fuselage_weight    import compute_fuselage_weight
from .compute_rotor_weight       import compute_rotor_weight
from .compute_wing_weight        import compute_wing_weight
from .compute_wiring_weight      import compute_wiring_weight