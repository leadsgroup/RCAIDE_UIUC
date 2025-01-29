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
    rho                         = conditions.freestream.density
    u0                          = conditions.freestream.velocity  
    g                           = conditions.freestream.gravity 
    gamma                       = conditions.freestream.isentropic_expansion_factor 
    M0                          = conditions.freestream.mach_number  
    p0                          = conditions.freestream.pressure       

    # Unpack low_fidelity_ducted_fan operating conditions and properties 
    Tref                        = low_fidelity_ducted_fan.reference_temperature
    Pref                        = low_fidelity_ducted_fan.reference_pressure
    mdhc                        = low_fidelity_ducted_fan.compressor_nondimensional_massflow
    A_R                         = low_fidelity_ducted_fan.rotor_disc_area
    epsilon_d                   = low_fidelity_ducted_fan.diffuser_expansion_ratio
    K_fan                       = low_fidelity_ducted_fan.fan_effectiveness
    eta_p                       = low_fidelity_ducted_fan.propeller_efficiency

    total_temperature_reference = low_fidelity_ducted_fan_conditions.total_temperature_reference
    total_pressure_reference    = low_fidelity_ducted_fan_conditions.total_pressure_reference 
    V_fan_nozzle                = low_fidelity_ducted_fan_conditions.fan_nozzle_exit_velocity
    fan_area_ratio              = low_fidelity_ducted_fan_conditions.fan_nozzle_area_ratio
    P_fan_nozzle                = low_fidelity_ducted_fan_conditions.fan_nozzle_static_pressure  

    total_temperature_reference = low_fidelity_ducted_fan_conditions.total_temperature_reference
    total_pressure_reference    = low_fidelity_ducted_fan_conditions.total_pressure_reference  
    V_3                         = low_fidelity_ducted_fan_conditions.fan_exit_velocity

    thrust_nondim       =  (gamma*M0*M0*(V_fan_nozzle/u0-1.) + fan_area_ratio*(P_fan_nozzle/p0-1.))

    # Computing Specifc Thrust
    Fsp   = 1./(gamma*M0)*thrust_nondim

    # Compute mass flow
    mdot                        = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)

    # Compute thrust
    T                           = rho*A_R*V_3*(V_3/epsilon_d - u0)

    # Computing Specifc Thrust
    T_sp                        = T/mdot

    # Compute specific impulse
    I_sp                        = T_sp/g

    # Compute power 
    P_req                       = (3/4)*T*u0 + (((T**2)*(u0**2)/16) + ((T**3)/(4*rho*A_R*epsilon_d)))**(0.5)   
    Power                       = K_fan*P_req/eta_p 

    # Pack turbofan outouts  
    low_fidelity_ducted_fan_conditions.thrust           = T
    low_fidelity_ducted_fan_conditions.specific_thrust  = T_sp  
    low_fidelity_ducted_fan_conditions.power            = Power  
    low_fidelity_ducted_fan_conditions.specific_impulse = I_sp
    low_fidelity_ducted_fan_conditions.mass_flow_rate   = mdot
    low_fidelity_ducted_fan_conditions.non_dimensional_thrust = Fsp  
    
    return  