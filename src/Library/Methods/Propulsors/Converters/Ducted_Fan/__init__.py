# RCAIDE/Library/Methods/Propulsors/Converters/Ducted_Fan/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .purge_files                        import purge_files
from .read_results                       import read_results
from .run_dfdc_analysis                  import run_dfdc_analysis
from .translate_conditions_to_dfdc_cases import translate_conditions_to_dfdc_cases
from .compute_ducted_fan_performance     import compute_ducted_fan_performance
from .append_ducted_fan_conditions       import append_ducted_fan_conditions
from .write_geometry                     import write_geometry
from .write_input_deck                   import write_input_deck
from .design_ducted_fan                  import design_ducted_fan