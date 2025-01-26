# RCAIDE/Methods/Energy/Propulsors/ICE_Propulsor/__init__.py
# 

"""
Collection of methods for analyzing Internal Combustion Engine (ICE) propulsion systems. 
These methods provide functionality for performance computation and state management of 
propeller-driven ICE propulsors, including torque matching between engine and propeller, 
condition tracking, and residual handling for solver integration.

See Also
--------
RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor
RCAIDE.Library.Methods.Propulsors.Electric_Ducted_Fan_Propulsor
RCAIDE.Library.Components.Propulsors.ICE_Propeller
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_ice_performance         import compute_ice_performance
from .append_ice_propeller_conditions import append_ice_propeller_conditions
from .unpack_ice_propeller_unknowns   import unpack_ice_propeller_unknowns
from .pack_ice_propeller_residuals    import pack_ice_propeller_residuals
