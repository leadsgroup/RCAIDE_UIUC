# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/size_core.py
# 
# Created:  Jan 2025, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Propulsors.Low_Fidelity_Ducted_Fan            import compute_thrust

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ---------------------------------------------------------------------------------------------------------------------- 
def size_core(low_fidelity_ducted_fan,low_fidelity_ducted_fan_conditions,conditions):
    """Sizes the core flow for the design condition by computing the
    non-dimensional thrust 

    Assumptions:
        Working fluid is a perfect gas

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.speed_of_sound  (numpy.ndarray): [m/s]  
        low_fidelity_ducted_fan
          .total_temperature_reference (float): total temperature reference [K]
          .total_pressure_reference    (float): total pressure reference    [Pa]  
          .reference_temperature              (float): reference temperature       [K]
          .reference_pressure                 (float): reference pressure          [Pa]
          .design_thrust                      (float): design thrust               [N]  

    Returns:
        None 
    """             
    # Unpack flight conditions 
    a0             = conditions.freestream.speed_of_sound

    # Unpack low_fidelity_ducted_fan flight conditions 
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

    # Store results on low_fidelity_ducted_fan data structure 
    low_fidelity_ducted_fan.mass_flow_rate_design               = mdot_core
    low_fidelity_ducted_fan.compressor_nondimensional_massflow  = mdhc

    return  
