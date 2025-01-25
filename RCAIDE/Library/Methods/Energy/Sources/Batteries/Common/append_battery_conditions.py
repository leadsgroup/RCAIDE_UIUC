# RCAIDE/Methods/Energy/Sources/Battery/Common/append_battery_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke
# Modified: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Append Battery Conditions
# ----------------------------------------------------------------------------------------------------------------------  
def append_battery_conditions(battery_module,segment,bus):
    """
    Appends the initial battery module conditions. 

    Parameters
    ----------
    battery_module : battery_module
        The battery_module object containing cell properties and configuration.
    segment : MissionSegment
        The current mission segment. 
    bus : bus
        The electrical bus object.

    Returns
    ------- 

    Notes
    -----
    The function appends various battery module conditions in the `state` object, including:
    - Current energy
    - Temperature
    - Heat energy generated
    - Load power
    - Current
    - Open-circuit voltage
    - Charge throughput
    - Internal resistance
    - State of charge
    - Depth of discharge
    - Voltage under load

    The model includes:
    - Internal resistance calculation
    - Thermal modeling (heat generation and temperature change)
    - Electrical performance (voltage and current calculations)
    - State of charge and depth of discharge updates

    Arrays accessed from objects:
    - From bus_conditions:
        - power_draw
        - current_draw
    - From battery_module_conditions:
        - energy
        - voltage_open_circuit
        - cell.voltage_open_circuit
        - power
        - cell.power
        - internal_resistance
        - cell.internal_resistance
        - heat_energy_generated
        - cell.heat_energy_generated
        - voltage_under_load
        - cell.voltage_under_load
        - current
        - cell.current
        - temperature
        - cell.temperature
        - cell.state_of_charge
        - cell.energy
        - cell.charge_throughput
        - cell.depth_of_discharge

    References
    ---------- 

    Assumptions
    -----------
    - Battery temperature is set to one degree hotter than ambient temperature for robust convergence.
    - Initial mission energy, maxed aged energy, and initial segment energy are the same
    - Cycle day is zero unless specified, resistance_growth_factor and capacity_fade_factor is one unless specified in the segment
    """ 
    ones_row                                               = segment.state.ones_row

    # compute ambient conditions
    atmosphere    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    alt           = -segment.conditions.frames.inertial.position_vector[:,2] 
    if segment.temperature_deviation != None:
        temp_dev = segment.temperature_deviation    
    atmo_data    = atmosphere.compute_values(altitude = alt,temperature_deviation=temp_dev)  
        
    bus_conditions                                              = segment.state.conditions.energy[bus.tag]        
    bus_conditions.battery_modules[battery_module.tag]          = Conditions() 
    bus_conditions.battery_modules[battery_module.tag].cell     = Conditions()


    bus_conditions.battery_modules[battery_module.tag].voltage_open_circuit      = 0 * ones_row(1)
    bus_conditions.battery_modules[battery_module.tag].cell.voltage_open_circuit = 0 * ones_row(1)
            
    bus_conditions.battery_modules[battery_module.tag].internal_resistance       = 0 * ones_row(1)
    bus_conditions.battery_modules[battery_module.tag].cell.internal_resistance  = 0 * ones_row(1)
         
    bus_conditions.battery_modules[battery_module.tag].voltage_under_load         = 0 * ones_row(1)
    bus_conditions.battery_modules[battery_module.tag].cell.voltage_under_load    = 0 * ones_row(1)
     
    bus_conditions.battery_modules[battery_module.tag].power                      = 0 * ones_row(1)
    bus_conditions.battery_modules[battery_module.tag].cell.power                 = 0 * ones_row(1)   
              
    bus_conditions.battery_modules[battery_module.tag].power_draw                 = 0 * ones_row(1)    
    bus_conditions.battery_modules[battery_module.tag].current_draw               = 0 * ones_row(1)
              
    bus_conditions.battery_modules[battery_module.tag].current                    = 0 * ones_row(1)
    bus_conditions.battery_modules[battery_module.tag].cell.current               = 0 * ones_row(1)  
               
    bus_conditions.battery_modules[battery_module.tag].heat_energy_generated      = 0 * ones_row(1)   
    bus_conditions.battery_modules[battery_module.tag].cell.heat_energy_generated = 0 * ones_row(1)    
              
    bus_conditions.battery_modules[battery_module.tag].cell.energy                = 0 * ones_row(1)
    bus_conditions.battery_modules[battery_module.tag].energy                     = 0 * ones_row(1)      
               
    bus_conditions.battery_modules[battery_module.tag].cell.cycle_in_day               = 0
    bus_conditions.battery_modules[battery_module.tag].cell.resistance_growth_factor   = 1.
    bus_conditions.battery_modules[battery_module.tag].cell.capacity_fade_factor       = 1. 
    
    # Conditions for recharging battery_module 
    if isinstance(segment,RCAIDE.Framework.Mission.Segments.Ground.Recharge):
        segment.state.conditions.energy.recharging  = True 
        segment.state.unknowns['recharge']          =  0* ones_row(1)  
        segment.state.residuals.network['recharge'] =  0* ones_row(1)
    elif type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Discharge:
        segment.state.conditions.energy.recharging   = False 
        segment.state.unknowns['discharge']          =  0* ones_row(1)  
        segment.state.residuals.network['discharge'] =  0* ones_row(1)     
    else:
        segment.state.conditions.energy.recharging  = False 
        
    # first segment 
    if 'initial_battery_state_of_charge' in segment:  
        initial_battery_energy                                            = segment.initial_battery_state_of_charge*battery_module.maximum_energy   
        bus_conditions.battery_modules[battery_module.tag].maximum_initial_energy   = initial_battery_energy
        bus_conditions.battery_modules[battery_module.tag].energy                   = initial_battery_energy* ones_row(1) 
        bus_conditions.battery_modules[battery_module.tag].state_of_charge          = segment.initial_battery_state_of_charge* ones_row(1) 
        bus_conditions.battery_modules[battery_module.tag].cell.state_of_charge     = segment.initial_battery_state_of_charge* ones_row(1) 
        bus_conditions.battery_modules[battery_module.tag].cell.depth_of_discharge  = 1 - segment.initial_battery_state_of_charge* ones_row(1)
    else:  
        bus_conditions.battery_modules[battery_module.tag].energy                    = 0 * ones_row(1)
        bus_conditions.battery_modules[battery_module.tag].state_of_charge           = 0 * ones_row(1)
        bus_conditions.battery_modules[battery_module.tag].cell.state_of_charge      = 0 * ones_row(1)       
        bus_conditions.battery_modules[battery_module.tag].cell.depth_of_discharge   = 0 * ones_row(1)   
        
    # temperature 
    if 'battery_cell_temperature' in segment:
        cell_temperature  = segment.battery_cell_temperature  
    else:
        cell_temperature                                      = atmo_data.temperature[0,0] 
    bus_conditions.battery_modules[battery_module.tag].temperature      = cell_temperature * ones_row(1)         
    bus_conditions.battery_modules[battery_module.tag].cell.temperature = cell_temperature * ones_row(1) 

    # charge thoughput 
    if 'charge_throughput' in segment: 
        bus_conditions.battery_modules[battery_module.tag].cell.charge_throughput          = segment.charge_throughput * ones_row(1)  
        bus_conditions.battery_modules[battery_module.tag].cell.resistance_growth_factor   = segment.resistance_growth
        bus_conditions.battery_modules[battery_module.tag].cell.capacity_fade_factor       = segment.capacity_fade
        bus_conditions.battery_modules[battery_module.tag].cell.cycle_in_day               = segment.cycle_day
    else:
        bus_conditions.battery_modules[battery_module.tag].cell.charge_throughput          = 0 * ones_row(1)
        bus_conditions.battery_modules[battery_module.tag].cell.resistance_growth_factor   = 1 
        bus_conditions.battery_modules[battery_module.tag].cell.capacity_fade_factor       = 1 
        bus_conditions.battery_modules[battery_module.tag].cell.cycle_in_day               = 0 
    # This is the only one besides energy and discharge flag that should be moduleed into the segment top level
    if 'increment_battery_age_by_one_day' not in segment:
        segment.increment_battery_age_by_one_day   = False    
     
    return 
    
def append_battery_segment_conditions(battery_module, bus, conditions, segment): 
    """
    Sets the initial battery module energy at the start of each segment as the last point from the previous segment
    
    Parameters
    ----------
    battery_module : battery_module
        The battery_module object containing cell properties and configuration.
    bus : bus
        The electrical bus object.
    conditions : MissionConditions
        The current conditions of the mission segment segment
    segment : MissionSegment
        The current mission segment. 

    Returns
    ------- 
        
    """

    battery_conditions = conditions[bus.tag].battery_modules[battery_module.tag]
    if segment.state.initials:  
        battery_initials                                        = segment.state.initials.conditions.energy[bus.tag].battery_modules[battery_module.tag]  
        if type(segment) ==  RCAIDE.Framework.Mission.Segments.Ground.Recharge:             
            battery_conditions.battery_discharge_flag           = False 
        else:                   
            battery_conditions.battery_discharge_flag           = True      
            
        battery_conditions.energy[:,0]                     = battery_initials.energy[-1,0]
        battery_conditions.temperature[:,0]                = battery_initials.temperature[-1,0]
        battery_conditions.cell.temperature[:,0]           = battery_initials.cell.temperature[-1,0]
        battery_conditions.cell.cycle_in_day               = battery_initials.cell.cycle_in_day      
        battery_conditions.cell.charge_throughput[:,0]     = battery_initials.cell.charge_throughput[-1,0]
        battery_conditions.cell.resistance_growth_factor   = battery_initials.cell.resistance_growth_factor 
        battery_conditions.cell.capacity_fade_factor       = battery_initials.cell.capacity_fade_factor 
        battery_conditions.cell.state_of_charge[:,0]       = battery_initials.cell.state_of_charge[-1,0]

    if 'battery_cell_temperature' in segment:       
        battery_conditions.temperature[:,0]          = segment.battery_cell_temperature 
        battery_conditions.cell.temperature[:,0]     = segment.battery_cell_temperature     

    return    