# RCAIDE/Framework/Energy/Networks/Fuel.py
# 
# Created:  Oct 2023, M. Clarke
#           Jan 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports
import  RCAIDE
from RCAIDE.Library.Methods.Powertrain.Systems.compute_avionics_power_draw import compute_avionics_power_draw
from RCAIDE.Library.Methods.Powertrain.Systems.compute_payload_power_draw  import compute_payload_power_draw

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Fuel
# ----------------------------------------------------------------------------------------------------------------------   
def evaluate_electric_based_propulsors(network,state,center_of_gravity,total_thrust,total_moment, total_power):
    conditions     = state.conditions 
    busses         = network.busses

    # Step 1: Compute Thrust 
    for bus in busses:    
        avionics  = bus.avionics
        payload   = bus.payload  

        # Avionics Power Consumtion
        avionics_conditions = state.conditions.energy[bus.tag][avionics.tag]
        compute_avionics_power_draw(avionics,avionics_conditions,conditions)

        # Payload Power
        payload_conditions = state.conditions.energy[bus.tag][payload.tag]
        compute_payload_power_draw(payload,payload_conditions,conditions)

        # Bus Voltage 
        bus_voltage = bus.voltage * state.ones_row(1)

        if conditions.energy.recharging:
            avionics_power         = (avionics_conditions.power*bus.power_split_ratio)* state.ones_row(1)
            payload_power          = (payload_conditions.power*bus.power_split_ratio)* state.ones_row(1)            
            total_esc_power        = 0 * state.ones_row(1)
            bus.charging_current   = bus.nominal_capacity * bus.charging_c_rate 
            charging_power         = (bus.charging_current*bus_voltage*bus.power_split_ratio)

            # append bus outputs to bus
            bus_conditions                    = state.conditions.energy[bus.tag]
            bus_conditions.power_draw         = ((avionics_power + payload_power + total_esc_power) - charging_power)/bus.efficiency
            bus_conditions.current_draw       = -bus_conditions.power_draw/bus.voltage 

        else:       
            # compute energy consumption of each electrochemical energy source on bus 
            stored_results_flag  = False
            stored_propulsor_tag = None 
            for propulsor_group in bus.assigned_propulsors:
                for propulsor_tag in propulsor_group:
                    propulsor =  network.propulsors[propulsor_tag]
                    if propulsor.active and bus.active:       
                        if network.identical_propulsors == False:
                            # run analysis  
                            T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,bus_voltage,center_of_gravity)
                        else:             
                            if stored_results_flag == False: 
                                # run propulsor analysis 
                                T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,bus_voltage,center_of_gravity)
                            else:
                                # use previous propulsor results 
                                T,M,P = propulsor.reuse_stored_data(state,network,stored_propulsor_tag,center_of_gravity)

                        total_thrust += T   
                        total_moment += M   
                        total_power  += P 

            # compute power from each componemnt 
            avionics_power  = (avionics_conditions.power*bus.power_split_ratio)* state.ones_row(1) 
            payload_power   = (payload_conditions.power*bus.power_split_ratio)* state.ones_row(1)   
            charging_power  = (state.conditions.energy[bus.tag].regenerative_power*bus_voltage*bus.power_split_ratio) 
            total_esc_power = total_power*bus.power_split_ratio  

            # append bus outputs to electrochemical energy source 
            bus_conditions                    = state.conditions.energy[bus.tag]
            bus_conditions.power_draw        += ((avionics_power + payload_power + total_esc_power) - charging_power)/bus.efficiency
            bus_conditions.current_draw       = bus_conditions.power_draw/bus_voltage 

    return total_thrust, total_moment, total_power


def evaluate_fuel_based_propulsors(network,state,center_of_gravity,total_thrust,total_moment, total_power):

    conditions     = state.conditions 
    fuel_lines     = network.fuel_lines
    total_mdot     = 0. * state.ones_row(1)   

    # Step 2: loop through compoments of network and determine performance
    for fuel_line in fuel_lines:
        fuel_line_mdot       = 0. * state.ones_row(1)  
        stored_results_flag  = False
        stored_propulsor_tag = None
        # Step 2.1: Compute thrust,moment and power of propulsors
        for propulsor_group in fuel_line.assigned_propulsors:
            for propulsor_tag in propulsor_group:
                propulsor =  network.propulsors[propulsor_tag]
                if propulsor.active and fuel_line.active:   
                    if network.identical_propulsors == False:
                        # run analysis  
                        T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,center_of_gravity)
                    else:             
                        if stored_results_flag == False: 
                            # run propulsor analysis 
                            T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,center_of_gravity)
                        else:
                            # use previous propulsor results 
                            T,M,P = propulsor.reuse_stored_data(state,network,stored_propulsor_tag,center_of_gravity)

                    total_thrust += T   
                    total_moment += M   
                    total_power  += P

                    # compute fuel line mass flow rate 
                    fuel_line_mdot += conditions.energy[propulsor.tag].fuel_flow_rate

                    # compute total mass flow rate 
                    total_mdot     += conditions.energy[propulsor.tag].fuel_flow_rate 

        # Step 2.2: Determine cumulative fuel flow from each fuel tank  
        for fuel_tank in fuel_line.fuel_tanks:  
            conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank.fuel_selector_ratio*fuel_line_mdot + fuel_tank.secondary_fuel_flow         
 
    return  total_thrust, total_moment, total_power, total_mdot

def evaluate_electric_energy_storage(state,network,total_mdot): 
    busses          = network.busses     
    conditions      = state.conditions  
    coolant_lines   = network.coolant_lines
    cryogen_mdot    = 0. * state.ones_row(1)   
    
    # NEED TO FIGURE OUT A WAY TO CONNECT POWER SUPPLED BY CONVENTIONAL SOURCE 
    
    # Step 2.1: Compute performance of electro-chemical energy (battery) compoments   
    time               = state.conditions.frames.inertial.time[:,0] 
    delta_t            = np.diff(time)
    for bus in  busses:    
        for t_idx in range(state.numerics.number_of_control_points):            
            stored_results_flag       = False
            stored_battery_cell_tag   = None
            
            stored_fuel_cell_tag      = None  
            # Step 2.1.a : Battery Module Performance          
            for battery_module in  bus.battery_modules:                   
                if bus.identical_battery_modules == False:
                    # run analysis  
                    stored_results_flag, stored_battery_cell_tag =  battery_module.energy_calc(state,bus,coolant_lines, t_idx, delta_t)
                else:             
                    if stored_results_flag == False: 
                        # run battery analysis 
                        stored_results_flag, stored_battery_cell_tag  =  battery_module.energy_calc(state,bus,coolant_lines, t_idx, delta_t)
                    else:
                        # use previous battery results 
                        battery_module.reuse_stored_data(state,bus,stored_results_flag, stored_battery_cell_tag)
             
            # Step 2.1.b : Fuel Cell Stack Performance           
            for fuel_cell_stack in  bus.fuel_cell_stacks:                   
                if bus.identical_fuel_cell_stacks == False:
                    # run analysis  
                    stored_results_flag, stored_fuel_cell_tag =  fuel_cell_stack.energy_calc(state,bus,coolant_lines, t_idx, delta_t)
                else:             
                    if stored_results_flag == False: 
                        # run battery analysis 
                        stored_results_flag, stored_fuel_cell_tag  =  fuel_cell_stack.energy_calc(state,bus,coolant_lines, t_idx, delta_t)
                    else:
                        # use previous battery results 
                        fuel_cell_stack.reuse_stored_data(state,bus,stored_results_flag, stored_fuel_cell_tag)
                     
                # compute cryogen mass flow rate 
                fuel_cell_stack_conditions  = state.conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag]                        
                cryogen_mdot[t_idx]        += fuel_cell_stack_conditions.H2_mass_flow_rate[t_idx]
                
                # compute total mass flow rate 
                total_mdot[t_idx]     += fuel_cell_stack_conditions.H2_mass_flow_rate[t_idx]    
               
            # Step 3: Compute bus properties          
            bus.compute_distributor_conditions(state,t_idx, delta_t)
            
            # Step 4 : Battery Thermal Management Calculations                    
            for coolant_line in coolant_lines:
                if t_idx != state.numerics.number_of_control_points-1: 
                    for heat_exchanger in coolant_line.heat_exchangers: 
                        heat_exchanger.compute_heat_exchanger_performance(state,bus,coolant_line,delta_t[t_idx],t_idx) 
                    for reservoir in coolant_line.reservoirs:   
                        reservoir.compute_reservior_coolant_temperature(state,coolant_line,delta_t[t_idx],t_idx) 
   
        # Step 5: Determine mass flow from cryogenic tanks 
        for cryogenic_tank in bus.cryogenic_tanks:
            # Step 5.1: Determine the cumulative flow from each cryogen tank
            fuel_tank_mdot = cryogenic_tank.croygen_selector_ratio*cryogen_mdot + cryogenic_tank.secondary_cryogenic_flow 
            
            # Step 5.2: DStore mass flow results 
            conditions.energy[bus.tag][cryogenic_tank.tag].mass_flow_rate  = fuel_tank_mdot
            
    return total_mdot


def evaluate_fuel_energy_storage(state,network,total_mdot):
    conditions     = state.conditions  
    fuel_lines     = network.fuel_lines  
     

    # NEED TO FIGURE OUT A WAY TO CONNECT POWER SUPPLED BY ElECTRIC SOURCE      
    alpha        = 0.000005
    throttle     = 0.5*state.ones_row(1) # NEED TO REMOVE FROM HERE 
    target_power = (1-state.conditions.energy.hybrid_power_split_ratio)*electric_power # NEED TO CONNECT ELECTRICAL POWER 
    
    # Step 2: loop through compoments of network and determine performance
    for fuel_line in fuel_lines:
        fuel_line_mdot       = 0. * state.ones_row(1)  
        stored_results_flag  = False
        stored_propulsor_tag = None
        # Step 2.1: Compute thrust,moment and power of propulsors
    
        diff_target_power = 100
        while np.any(np.abs(diff_target_power) > 1E-6):
            
            fuel_network_total_power  = 0. * state.ones_row(1)  
            # update guess of mdot
            for tag, item in fuel_line.items():
                if type(item) == RCAIDE.Library.Components.Powertrain.Converters.Turboshaft: 
                    if item.active and fuel_line.active: 
                        state.conditions.energy[item.tag].throttle = throttle
                        if network.identical_propulsors == False:
                            # run analysis  
                            T,M,P,stored_results_flag,stored_propulsor_tag = item.compute_performance(state)
                        else:             
                            if stored_results_flag == False: 
                                # run propulsor analysis 
                                T,M,P,stored_results_flag,stored_propulsor_tag = item.compute_performance(state)
                            else:
                                # use previous propulsor results 
                                T,M,P = item.reuse_stored_data(state,network,stored_propulsor_tag)
                         
                        fuel_network_total_power  += P
                        
                        # compute fuel line mass flow rate 
                        fuel_line_mdot += conditions.energy[item.tag].fuel_flow_rate
                        
                        # compute total mass flow rate 
                        total_mdot     += conditions.energy[item.tag].fuel_flow_rate 
    
            diff_target_power = target_power - fuel_network_total_power 
            stored_results_flag = False 
            throttle  += alpha*(diff_target_power) 
                
        # Step 2.2: Determine cumulative fuel flow from each fuel tank  
        for fuel_tank in fuel_line.fuel_tanks:  
            conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  += fuel_tank.fuel_selector_ratio*fuel_line_mdot + fuel_tank.secondary_fuel_flow         
                            
        
    return total_mdot                            