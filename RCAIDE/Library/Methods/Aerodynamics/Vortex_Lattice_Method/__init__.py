## @defgroup Methods-Aerodynamics-Fidelity_Zero Fidelity_Zero
# @ingroup Methods-Aerodynamics
# RCAIDE/Methods/Aerodynamics/Fidelity_Zero/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift                           import generate_vortex_distribution, compute_unit_normal 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_VD_helpers       import postprocess_VD, compute_panel_area, compute_unit_normal
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.make_VLM_wings            import make_VLM_wings  
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.deflect_control_surface   import deflect_control_surface
from .compute_RHS_matrix                      import compute_RHS_matrix 
from .compute_wing_induced_velocity           import compute_wing_induced_velocity 
from .generate_vortex_distribution            import generate_vortex_distribution
from .VLM                                     import VLM
from .VLM_Aerodynamics import *  

