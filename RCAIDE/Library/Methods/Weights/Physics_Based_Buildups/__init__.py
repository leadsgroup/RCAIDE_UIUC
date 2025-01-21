# RCAIDE/Library/Methods/Weights/Buildups/__init__.py
# 

"""
Collection of physics-based methods for aircraft weight estimation. Unlike correlation-based approaches, these methods 
calculate component weights using first principles, structural analysis, and material properties. The module includes 
specialized methods for both conventional and electric propulsion systems.

See Also
--------
RCAIDE.Library.Methods.Weights.Correlation_Buildups
RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport
RCAIDE.Library.Methods.Weights.Correlation_Buildups.UAV
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from . import Common
from . import Electric