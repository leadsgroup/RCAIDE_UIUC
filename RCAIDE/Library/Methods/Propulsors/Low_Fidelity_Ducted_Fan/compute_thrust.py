# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/compute_thurst.py
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
    """Computes thrust and other properties of the low_fidelity_ducted_fan listed below: 
    low_fidelity_ducted_fan.  
      .outputs.thrust                                    (numpy.ndarray): thrust                               [N] 
      .outputs.non_dimensional_thrust                    (numpy.ndarray): non-dim thurst                       [unitless] 
      .outputs.core_mass_flow_rate                       (numpy.ndarray): core nozzle mass flow rate           [kg/s] 
      .outputs.power                                     (numpy.ndarray): power                                [W] 
      
    Assumptions:
        Perfect gas

    Source:
        Stanford AA 283 Course Notes: https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/


    Args: 
        conditions. 
           freestream.isentropic_expansion_factor                (float): isentropic expansion factor          [unitless]  
           freestream.specific_heat_at_constant_pressure         (float): speific heat                         [J/(kg K)] 
           freestream.velocity                           (numpy.ndarray): freestream velocity                  [m/s] 
           freestream.speed_of_sound                     (numpy.ndarray): freestream speed_of_sound            [m/s] 
           freestream.mach_number                        (numpy.ndarray): freestream mach_number               [unitless] 
           freestream.pressure                           (numpy.ndarray): freestream pressure                  [Pa] 
           freestream.gravity                            (numpy.ndarray): freestream gravity                   [m/s^2] 
           propulsion.throttle                           (numpy.ndarray): throttle                             [unitless] 
        low_fidelity_ducted_fan 
           .total_temperature_reference                          (float): total_temperature_reference          [K] 
           .total_pressure_reference                             (float): total_pressure_reference             [Pa]     
           .fan_nozzle.velocity                          (numpy.ndarray): low_fidelity_ducted_fan fan nozzle velocity         [m/s] 
           .fan_nozzle.static_pressure                   (numpy.ndarray): low_fidelity_ducted_fan fan nozzle static pressure  [Pa] 
           .fan_nozzle.area_ratio                                (float): low_fidelity_ducted_fan fan nozzle area ratio       [unitless]   
           .reference_temperature                                (float): reference_temperature                [K] 
           .reference_pressure                                   (float): reference_pressure                   [Pa] 
           .compressor_nondimensional_massflow                   (float): non-dim mass flow rate               [unitless]
      
    Returns:
        None
         
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
    fan_thrust_nondim   = flow_through_fan*(gamma*M0*M0*(V_fan_nozzle/u0-1.) + fan_area_ratio*(P_fan_nozzle/p0-1.))

    thrust_nondim       = fan_thrust_nondim

    # Computing Specifc Thrust
    Fsp   = 1./(gamma*M0)*thrust_nondim
    Fsp_f = 1./(gamma*M0)*fan_thrust_nondim
 
    # Compute core mass flow
    mdot_core  = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)

    # Compute dimensional thrust
    FD2   = Fsp*a0*(1)*mdot_core*low_fidelity_ducted_fan_conditions.throttle
    FD2_f = Fsp_f*a0*(1)*mdot_core*low_fidelity_ducted_fan_conditions.throttle

    # Compute power 
    power   = FD2*u0    

    # Pack low_fidelity_ducted_fan outouts  
    low_fidelity_ducted_fan_conditions.thrust                            = FD2 
    low_fidelity_ducted_fan_conditions.fan_thrust                        = FD2_f 
    low_fidelity_ducted_fan_conditions.non_dimensional_thrust            = Fsp  
    low_fidelity_ducted_fan_conditions.power                             = power  
    low_fidelity_ducted_fan_conditions.core_mass_flow_rate               = mdot_core  
    
    return  