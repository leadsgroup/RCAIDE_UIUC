# RCAIDE/Library/Methods/Propulsors/Converters/Expansion_Nozzlee/__init__.py

"""
Collection of methods for modeling expansion nozzle performance in propulsion systems. 
This module provides tools for computing nozzle conditions and performance metrics 
including thrust, mass flow rates, and efficiencies.

See Also
--------
RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle
RCAIDE.Library.Methods.Propulsors.Converters.Nozzle_Calculations
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .append_expansion_nozzle_conditions    import append_expansion_nozzle_conditions         
from .compute_expansion_nozzle_performance  import compute_expansion_nozzle_performance