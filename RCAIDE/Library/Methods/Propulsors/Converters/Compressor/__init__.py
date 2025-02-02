# RCAIDE/Library/Methods/Propulsors/Converters/Compressor/__init__.py

"""
Collection of methods for computing compressor performance and conditions in propulsion systems. 
This module provides functionality for calculating compressor performance metrics and appending 
relevant thermodynamic conditions to the analysis.

See Also
--------
RCAIDE.Library.Methods.Propulsors.Converters.Turbine
RCAIDE.Library.Methods.Propulsors.Converters.Nozzle
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
        
from .compute_compressor_performance import compute_compressor_performance
from .append_compressor_conditions   import append_compressor_conditions