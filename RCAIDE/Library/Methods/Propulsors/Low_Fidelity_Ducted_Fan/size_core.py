# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/size_core.py
# 
# 
# Created:  Jan 2025, M. Guidotti
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Propulsors.Low_Fidelity_Ducted_Fan.compute_thrust import compute_thrust

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ---------------------------------------------------------------------------------------------------------------------- 
def size_core(low_fidelity_ducted_fan,low_fidelity_ducted_fan_conditions,conditions):
    """
    """             
    # Unpack flight conditions 
    a0             = conditions.freestream.speed_of_sound

    # Unpack low fidelity ducted fan flight conditions 
    Tref           = low_fidelity_ducted_fan.reference_temperature
    Pref           = low_fidelity_ducted_fan.reference_pressure 
    Tt_ref         = low_fidelity_ducted_fan_conditions.total_temperature_reference  
    Pt_ref         = low_fidelity_ducted_fan_conditions.total_pressure_reference
    
    # Compute nondimensional thrust
    low_fidelity_ducted_fan_conditions.throttle = 1.0
    compute_thrust(low_fidelity_ducted_fan,low_fidelity_ducted_fan_conditions,conditions) 

    # Compute dimensional mass flow rates
    Fsp        = low_fidelity_ducted_fan_conditions.non_dimensional_thrust
    mdot_core  = low_fidelity_ducted_fan.design_thrust/(Fsp*a0*(1)*low_fidelity_ducted_fan_conditions.throttle)  
    mdhc       = mdot_core/ (np.sqrt(Tref/Tt_ref)*(Pt_ref/Pref))

    # Store results on turbofan data structure 
    low_fidelity_ducted_fan.mass_flow_rate_design               = mdot_core
    low_fidelity_ducted_fan.compressor_nondimensional_massflow  = mdhc

    return  
