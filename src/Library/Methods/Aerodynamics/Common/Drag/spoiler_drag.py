# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/spoiler_drag.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# python imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Spolier Drag 
# ---------------------------------------------------------------------------------------------------------------------- 
def spoiler_drag(state,settings,geometry):
    """Adds a spoiler drag increment

    Assumptions:
        None

    Source:
        None

    Args:
        settings.spoiler_drag_increment (float): spoiler drag increment [Unitless]

    Returns:
        None 
    """    
    Mc =  state.conditions.freestream.mach_number
    state.conditions.aerodynamics.coefficients.drag.spoiler_drag = settings.spoiler_drag_increment * np.ones_like(Mc)
    
    return  
