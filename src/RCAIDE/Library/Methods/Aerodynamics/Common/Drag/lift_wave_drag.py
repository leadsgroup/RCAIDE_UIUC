# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/lift_wave_drag.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports    
from .wave_drag  import wave_drag  

# package imports
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compressibility Drag Total
# ---------------------------------------------------------------------------------------------------------------------- 
def lift_wave_drag(conditions,wing,Sref):
    """Determine lift wave drag for supersonic speeds.

    Assumptions: 

    Source:
        Stanford AA241 A/B Course Notes

    Args:
        conditions.freestream.mach_number (numpy.array): mach number              [unitless] 
        wing.areas.reference                    (float): wing reference area      [m^2]
        Sref                                    (float): main wing reference area [m^2]

    Returns:
        cd_c_l                            (numpy.array): Wave drag CD due to lift [unitless]
        """
    
    cd_lift_wave         = wave_drag(conditions,wing) 
    mach                 = conditions.freestream.mach_number 
    cd_c_l               = np.zeros_like(mach)  
    cd_c_l[mach >= 1.01] = cd_lift_wave[0:len(mach[mach >= 1.01]),0] 
    cd_c_l               = cd_c_l*wing.areas.reference/Sref

    return cd_c_l