# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/design_low_fidelity_ducted_fan.py
# 
# Created:  Jan 2025, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE
from RCAIDE.Framework.Mission.Common                                 import Conditions
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Fan                import compute_fan_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Low_Fidelity_Ducted_Fan       import size_core
from RCAIDE.Library.Methods.Propulsors.Common                        import compute_static_sea_level_performance


# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Design Turbofan
# ---------------------------------------------------------------------------------------------------------------------- 
def design_low_fidelity_ducted_fan(low_fidelity_ducted_fan):
    """Compute perfomance properties of a low fidelity ducted fan based on polytropic ration and combustor properties.
    Low fidelity ducted fan is created by manually linking the different components
    
    
    Assumtions:
       None 
    
    Source:
    
    Args:
        low_fidelity_ducted_fan (dict): low fidelity ducted fan data structure [-]
    
    Returns:
        None 

    """
    # check if mach number and temperature are passed
    if(low_fidelity_ducted_fan.design_mach_number==None) and (low_fidelity_ducted_fan.design_altitude==None): 
        raise NameError('The sizing conditions require an altitude and a Mach number') 
    else:
        #call the atmospheric model to get the conditions at the specified altitude
        atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
        atmo_data  = atmosphere.compute_values(low_fidelity_ducted_fan.design_altitude,low_fidelity_ducted_fan.design_isa_deviation)
        planet     = RCAIDE.Library.Attributes.Planets.Earth()
        
        p   = atmo_data.pressure          
        T   = atmo_data.temperature       
        rho = atmo_data.density          
        a   = atmo_data.speed_of_sound    
        mu  = atmo_data.dynamic_viscosity           
        U   = a*low_fidelity_ducted_fan.design_mach_number
        # setup conditions
        conditions = RCAIDE.Framework.Mission.Common.Results()
    
        # freestream conditions    
        conditions.freestream.altitude                    = np.atleast_1d(low_fidelity_ducted_fan.design_altitude)
        conditions.freestream.mach_number                 = np.atleast_1d(low_fidelity_ducted_fan.design_mach_number)
        conditions.freestream.pressure                    = np.atleast_1d(p)
        conditions.freestream.temperature                 = np.atleast_1d(T)
        conditions.freestream.density                     = np.atleast_1d(rho)
        conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
        conditions.freestream.gravity                     = np.atleast_1d(planet.compute_gravity(low_fidelity_ducted_fan.design_altitude))
        conditions.freestream.isentropic_expansion_factor = np.atleast_1d(low_fidelity_ducted_fan.working_fluid.compute_gamma(T,p))
        conditions.freestream.Cp                          = np.atleast_1d(low_fidelity_ducted_fan.working_fluid.compute_cp(T,p))
        conditions.freestream.R                           = np.atleast_1d(low_fidelity_ducted_fan.working_fluid.gas_specific_constant)
        conditions.freestream.speed_of_sound              = np.atleast_1d(a)
        conditions.freestream.velocity                    = np.atleast_1d(U) 
     
    segment                  = RCAIDE.Framework.Mission.Segments.Segment()  
    segment.state.conditions = conditions 
    low_fidelity_ducted_fan.append_operating_conditions(segment) 
    for tag, item in  low_fidelity_ducted_fan.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,low_fidelity_ducted_fan) 
    
    ram                       = low_fidelity_ducted_fan.ram
    inlet_nozzle              = low_fidelity_ducted_fan.inlet_nozzle
    fan                       = low_fidelity_ducted_fan.fan
    exit_nozzle               = low_fidelity_ducted_fan.exit_nozzle 
    # unpack component conditions
    low_fidelity_ducted_fan_conditions     = conditions.energy[low_fidelity_ducted_fan.tag]
    ram_conditions          = low_fidelity_ducted_fan_conditions[ram.tag]    
    inlet_nozzle_conditions = low_fidelity_ducted_fan_conditions[inlet_nozzle.tag]
    fan_conditions          = low_fidelity_ducted_fan_conditions[fan.tag]    
    exit_nozzle_conditions  = low_fidelity_ducted_fan_conditions[exit_nozzle.tag] 
     
    # Step 1: Set the working fluid to determine the fluid properties
    ram.working_fluid                             = low_fidelity_ducted_fan.working_fluid
    
    # Step 2: Compute flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions,conditions)
    
    # Step 3: link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure
    inlet_nozzle_conditions.inputs.static_temperature                 = ram_conditions.outputs.static_temperature
    inlet_nozzle_conditions.inputs.static_pressure                    = ram_conditions.outputs.static_pressure
    inlet_nozzle_conditions.inputs.mach_number                        = ram_conditions.outputs.mach_number
    inlet_nozzle.working_fluid                                        = ram.working_fluid
    
    # Step 4: Compute flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions,conditions)
    
    # Step 5: Link the fan to the inlet nozzle
    fan_conditions.inputs.stagnation_temperature                      = inlet_nozzle_conditions.outputs.stagnation_temperature
    fan_conditions.inputs.stagnation_pressure                         = inlet_nozzle_conditions.outputs.stagnation_pressure
    fan_conditions.inputs.static_temperature                          = inlet_nozzle_conditions.outputs.static_temperature
    fan_conditions.inputs.static_pressure                             = inlet_nozzle_conditions.outputs.static_pressure
    fan_conditions.inputs.mach_number                                 = inlet_nozzle_conditions.outputs.mach_number  
    fan.working_fluid                                                 = inlet_nozzle.working_fluid
     
    # Step 6: Compute flow through the fan
    compute_fan_performance(fan,fan_conditions,conditions)      
    # Step 19: Link the fan nozzle to the fan
    exit_nozzle_conditions.inputs.stagnation_temperature     = fan_conditions.outputs.stagnation_temperature
    exit_nozzle_conditions.inputs.stagnation_pressure        = fan_conditions.outputs.stagnation_pressure
    exit_nozzle_conditions.inputs.static_temperature         = fan_conditions.outputs.static_temperature
    exit_nozzle_conditions.inputs.static_pressure            = fan_conditions.outputs.static_pressure  
    exit_nozzle_conditions.inputs.mach_number                = fan_conditions.outputs.mach_number   
    exit_nozzle.working_fluid                                = fan.working_fluid
    
    # Step 20: Compute flow through the fan nozzle
    compute_expansion_nozzle_performance(exit_nozzle,exit_nozzle_conditions,conditions)
     
    # Step 21: Link the turbofan to outputs from various compoments    
    low_fidelity_ducted_fan_conditions.fan_nozzle_exit_velocity                 = exit_nozzle_conditions.outputs.velocity
    low_fidelity_ducted_fan_conditions.fan_nozzle_area_ratio                    = exit_nozzle_conditions.outputs.area_ratio  
    low_fidelity_ducted_fan_conditions.fan_nozzle_static_pressure               = exit_nozzle_conditions.outputs.static_pressure
    low_fidelity_ducted_fan_conditions.total_temperature_reference              = fan_conditions.outputs.stagnation_temperature
    low_fidelity_ducted_fan_conditions.total_pressure_reference                 = fan_conditions.outputs.stagnation_pressure
    low_fidelity_ducted_fan_conditions.flow_through_fan                         = 1

    # Step 22: Size the core of the turbofan  
    size_core(low_fidelity_ducted_fan,low_fidelity_ducted_fan_conditions,conditions) 
    mass_flow                     = low_fidelity_ducted_fan.mass_flow_rate_design
    low_fidelity_ducted_fan.design_core_massflow = mass_flow   
    
    # Step 23: Static Sea Level Thrust 
    compute_static_sea_level_performance(low_fidelity_ducted_fan)
     
    return 