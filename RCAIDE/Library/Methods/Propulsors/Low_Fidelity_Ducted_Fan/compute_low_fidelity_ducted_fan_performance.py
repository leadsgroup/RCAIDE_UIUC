# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/compute_low_fidelity_ducted_fan_performance.py
# 
# 
# Created:  Jan 2025, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Data   
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Fan                import compute_fan_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Low_Fidelity_Ducted_Fan       import compute_thrust

import  numpy as  np
from copy import  deepcopy

# ----------------------------------------------------------------------------------------------------------------------
# compute_performance
# ----------------------------------------------------------------------------------------------------------------------   
def compute_low_fidelity_ducted_fan_performance(low_fidelity_ducted_fan,state,center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' 
    ''' 
    conditions                = state.conditions   
    noise_conditions          = conditions.noise[low_fidelity_ducted_fan.tag] 
    low_fidelity_ducted_fan_conditions       = conditions.energy[low_fidelity_ducted_fan.tag] 
    rho                       = conditions.freestream.density
    U0                        = conditions.freestream.velocity
    
    ram                       = low_fidelity_ducted_fan.ram
    inlet_nozzle              = low_fidelity_ducted_fan.inlet_nozzle
    fan                       = low_fidelity_ducted_fan.fan
    exit_nozzle               = low_fidelity_ducted_fan.exit_nozzle
    
    # unpack component conditions 
    ram_conditions          = low_fidelity_ducted_fan_conditions[ram.tag]    
    inlet_nozzle_conditions = low_fidelity_ducted_fan_conditions[inlet_nozzle.tag]
    fan_conditions          = low_fidelity_ducted_fan_conditions[fan.tag]    
    exit_nozzle_conditions  = low_fidelity_ducted_fan_conditions[exit_nozzle.tag]

    # Set the working fluid to determine the fluid properties
    ram.working_fluid = low_fidelity_ducted_fan.working_fluid

    # Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions,conditions)

    # Link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature 
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure
    inlet_nozzle_conditions.inputs.static_temperature                 = ram_conditions.outputs.static_temperature
    inlet_nozzle_conditions.inputs.static_pressure                    = ram_conditions.outputs.static_pressure
    inlet_nozzle_conditions.inputs.mach_number                        = ram_conditions.outputs.mach_number
    inlet_nozzle.working_fluid                                        = ram.working_fluid

    # Flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions,conditions)
    
    # Link the fan to the inlet nozzle
    fan_conditions.inputs.stagnation_temperature                      = inlet_nozzle_conditions.outputs.stagnation_temperature
    fan_conditions.inputs.stagnation_pressure                         = inlet_nozzle_conditions.outputs.stagnation_pressure
    fan_conditions.inputs.static_temperature                          = inlet_nozzle_conditions.outputs.static_temperature
    fan_conditions.inputs.static_pressure                             = inlet_nozzle_conditions.outputs.static_pressure
    fan_conditions.inputs.mach_number                                 = inlet_nozzle_conditions.outputs.mach_number  
    fan.working_fluid                                                 = inlet_nozzle.working_fluid
    
    # Flow through the fan
    compute_fan_performance(fan,fan_conditions,conditions)    
          
    # Link the shaft power output to the fan
    try:
        shaft_power                                        = low_fidelity_ducted_fan.Shaft_Power_Off_Take       
        shaft_power.inputs.mdhc                            = low_fidelity_ducted_fan.compressor_nondimensional_massflow
        shaft_power.inputs.Tref                            = low_fidelity_ducted_fan.reference_temperature
        shaft_power.inputs.Pref                            = low_fidelity_ducted_fan.reference_pressure
        shaft_power.inputs.total_temperature_reference     = fan_conditions.outputs.stagnation_temperature
        shaft_power.inputs.total_pressure_reference        = fan_conditions.outputs.stagnation_pressure

        shaft_power(conditions)
    except:
        pass


    # Link the dan nozzle to the fan
    exit_nozzle_conditions.inputs.stagnation_temperature     = fan_conditions.outputs.stagnation_temperature
    exit_nozzle_conditions.inputs.stagnation_pressure        = fan_conditions.outputs.stagnation_pressure
    exit_nozzle_conditions.inputs.static_temperature         = fan_conditions.outputs.static_temperature
    exit_nozzle_conditions.inputs.static_pressure            = fan_conditions.outputs.static_pressure  
    exit_nozzle_conditions.inputs.mach_number                = fan_conditions.outputs.mach_number   
    exit_nozzle.working_fluid                                = fan.working_fluid
        
    # Flow through the fan nozzle
    compute_expansion_nozzle_performance(exit_nozzle,exit_nozzle_conditions,conditions)
 
    # Link the thrust component to the fan nozzle
    low_fidelity_ducted_fan_conditions.fan_nozzle_exit_velocity                        = exit_nozzle_conditions.outputs.velocity
    low_fidelity_ducted_fan_conditions.fan_nozzle_area_ratio                           = exit_nozzle_conditions.outputs.area_ratio  
    low_fidelity_ducted_fan_conditions.fan_nozzle_static_pressure                      = exit_nozzle_conditions.outputs.static_pressure

    # Link the thrust component to the low pressure compressor 
    low_fidelity_ducted_fan_conditions.total_temperature_reference              = low_fidelity_ducted_fan.reference_temperature
    low_fidelity_ducted_fan_conditions.total_pressure_reference                 = low_fidelity_ducted_fan.reference_pressure
    low_fidelity_ducted_fan_conditions.flow_through_fan                         = 1

    # Compute the thrust
    compute_thrust(low_fidelity_ducted_fan,low_fidelity_ducted_fan_conditions,conditions)

    # Compute forces and moments
    moment_vector              = 0*state.ones_row(3)
    thrust_vector              = 0*state.ones_row(3)
    thrust_vector[:,0]         =  low_fidelity_ducted_fan_conditions.thrust[:,0]
    moment_vector[:,0]         =  low_fidelity_ducted_fan.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1]         =  low_fidelity_ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]         =  low_fidelity_ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
    M                          =  np.cross(moment_vector, thrust_vector)   
    moment                     = M 
    power                      = low_fidelity_ducted_fan_conditions.power 
    low_fidelity_ducted_fan_conditions.moment = moment

    # store data

    fan_nozzle_res = Data(
                exit_static_temperature             = exit_nozzle_conditions.outputs.static_temperature,
                exit_static_pressure                = exit_nozzle_conditions.outputs.static_pressure,
                exit_stagnation_temperature         = exit_nozzle_conditions.outputs.stagnation_temperature,
                exit_stagnation_pressure            = exit_nozzle_conditions.outputs.static_pressure,
                exit_velocity                       = exit_nozzle_conditions.outputs.velocity
            )

    noise_conditions.turbofan.fan_nozzle    = fan_nozzle_res  
    noise_conditions.turbofan.fan           = None
    stored_results_flag                     = True
    stored_propulsor_tag                    = low_fidelity_ducted_fan.tag 
    
    return thrust_vector,moment,power,stored_results_flag,stored_propulsor_tag 
    
def reuse_stored_low_fidelity_ducted_fan_data(low_fidelity_ducted_fan,state,network,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one low fidelity ducted fan for identical low fidelity ducted fans
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    low_fidelity_ducted_fan             - low fidelity ducted fan data structure                [-]
    state                - operating conditions data structure   [-]  
    total_thrust         - thrust of low fidelity ducted fan group              [N]
    total_power          - power of low fidelity ducted fan group               [W] 

    Outputs:  
    total_thrust         - thrust of low fidelity ducted fan group              [N]
    total_power          - power of low fidelity ducted fan group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                                      = state.conditions  
    conditions.energy[low_fidelity_ducted_fan.tag]  = deepcopy(conditions.energy[stored_propulsor_tag])
    conditions.noise[low_fidelity_ducted_fan.tag]   = deepcopy(conditions.noise[stored_propulsor_tag])
    
    # compute moment  
    moment_vector      = 0*state.ones_row(3)
    thrust_vector      = 0*state.ones_row(3)
    thrust_vector[:,0] = conditions.energy[low_fidelity_ducted_fan.tag].thrust[:,0] 
    moment_vector[:,0] = low_fidelity_ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1] = low_fidelity_ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = low_fidelity_ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
    moment             = np.cross(moment_vector,thrust_vector)    
    
    power              = conditions.energy[low_fidelity_ducted_fan.tag].power 
    conditions.energy[low_fidelity_ducted_fan.tag].moment =  moment 
 
    return thrust_vector,moment,power    