# RCAIDE/Library/Methods/Propulsors/Turboshaft_Propulsor/__init__.py
# 
# Created:  Sep 2024, M. Clarke, M. Guidotti

"""
Collection of methods for analyzing turboshaft propulsion systems. These methods handle the design, 
sizing, and performance analysis of turboshaft engines, including power output calculations, core sizing, 
and operational performance evaluation.

The module provides functions for:
- Computing power output and fuel consumption
- Sizing engine core components
- Analyzing design point performance
- Computing off-design performance characteristics
- Managing stored engine performance data

See Also
--------
RCAIDE.Library.Methods.Propulsors.Turboshaft_Propulsor
RCAIDE.Library.Methods.Propulsors.Common
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_power                  import compute_power
from .size_core                      import size_core
from .design_turboshaft              import design_turboshaft
from .compute_turboshaft_performance import compute_turboshaft_performance , reuse_stored_turboshaft_data