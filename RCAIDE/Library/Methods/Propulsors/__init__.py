# RCAIDE/Library/Methods/Propulsors/__init__.py

"""
Collection of propulsion system analysis methods for various aircraft propulsion types. This module 
provides a comprehensive set of tools for analyzing and designing different propulsion systems, from 
conventional to advanced configurations.

The module includes methods for:
- Constant Speed Internal Combustion Engine (ICE) propulsors
- Electric propulsion systems (rotors and ducted fans)
- Gas turbine engines (turbofan, turbojet, turboprop, turboshaft)
- Power conversion and modulation systems
- Common propulsion utilities and analysis tools

The methods handle both design and off-design performance calculations, component sizing, and 
system integration analysis for various propulsion architectures.
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from . import Common
from . import Constant_Speed_ICE_Propulsor
from . import Converters 
from . import ICE_Propulsor
from . import Electric_Rotor_Propulsor
from . import Electric_Ducted_Fan_Propulsor
from . import Modulators
from . import Turbofan_Propulsor
from . import Turbojet_Propulsor
from . import Turboprop_Propulsor
from . import Turboshaft_Propulsor

