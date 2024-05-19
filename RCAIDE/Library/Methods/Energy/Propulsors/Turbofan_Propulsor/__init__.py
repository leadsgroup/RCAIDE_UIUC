## @defgroup Methods-Energy-Propulsors-Converters-Turbofan
# RCAIDE/Methods/Energy/Propulsors/Converters/Turbofan/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_stream_thrust                                      import compute_stream_thrust
from .compute_thurst                                             import compute_thrust
from .size_core                                                  import size_core
from .size_stream_thrust                                         import size_stream_thrust
from .compute_turbofan_performance                               import compute_turbofan_performance
from .design_turbofan                                            import design_turbofan 
from .size_turbofan_nacelle                                      import size_turbofan_nacelle
from Legacy.trunk.S.Methods.Propulsion.turbofan_emission_index   import turbofan_emission_index 
