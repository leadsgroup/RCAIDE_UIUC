# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/compute_thrust.py
# 
# 
# Created:  Jan 2025, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Framework.Core      import Units 

# Python package imports
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_thrust
# ----------------------------------------------------------------------------------------------------------------------
def compute_thrust(low_fidelity_ducted_fan,low_fidelity_ducted_fan_conditions,conditions):
    """
    """      
    # Unpack flight conditions 
    gamma                       = conditions.freestream.isentropic_expansion_factor 
    u0                          = conditions.freestream.velocity
    a0                          = conditions.freestream.speed_of_sound
    M0                          = conditions.freestream.mach_number
    p0                          = conditions.freestream.pressure  
    g                           = conditions.freestream.gravity        

    # Unpack low_fidelity_ducted_fan operating conditions and properties 
    Tref                        = low_fidelity_ducted_fan.reference_temperature
    Pref                        = low_fidelity_ducted_fan.reference_pressure
    mdhc                        = low_fidelity_ducted_fan.compressor_nondimensional_massflow
    total_temperature_reference = low_fidelity_ducted_fan_conditions.total_temperature_reference
    total_pressure_reference    = low_fidelity_ducted_fan_conditions.total_pressure_reference 
    flow_through_fan            = low_fidelity_ducted_fan_conditions.flow_through_fan  
    V_fan_nozzle                = low_fidelity_ducted_fan_conditions.fan_nozzle_exit_velocity
    fan_area_ratio              = low_fidelity_ducted_fan_conditions.fan_nozzle_area_ratio
    P_fan_nozzle                = low_fidelity_ducted_fan_conditions.fan_nozzle_static_pressure      

    # Compute  non dimensional thrust
    thrust_nondim   = flow_through_fan*(gamma*M0*M0*(V_fan_nozzle/u0-1.) + fan_area_ratio*(P_fan_nozzle/p0-1.))

    # Computing Specifc Thrust
    Fsp             = 1./(gamma*M0)*thrust_nondim
 
    # Compute core mass flow
    mdot_core       = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)

    # Compute dimensional thrust
    FD2             = Fsp*a0*mdot_core*low_fidelity_ducted_fan_conditions.throttle

    # Compute specific impulse
    Isp             = FD2/(mdot_core*g)

    # Compute power 
    power   = FD2*u0    

    # Pack turbofan outouts  
    low_fidelity_ducted_fan_conditions.thrust                            = FD2 
    low_fidelity_ducted_fan_conditions.non_dimensional_thrust            = Fsp  
    low_fidelity_ducted_fan_conditions.power                             = power  
    low_fidelity_ducted_fan_conditions.specific_impulse                  = Isp
    low_fidelity_ducted_fan_conditions.core_mass_flow_rate               = mdot_core 
    
    return  