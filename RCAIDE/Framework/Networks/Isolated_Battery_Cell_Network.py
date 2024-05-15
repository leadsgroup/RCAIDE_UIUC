## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Battery_Cell_Isolated_Network.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Mission.Common                                                 import Residuals
from RCAIDE.Framework.Core                                                                    import Data
from RCAIDE.Library.Components.Component                                                    import Container    
from RCAIDE.Library.Methods.Energy.Sources.Battery.Common.append_initial_battery_conditions import append_initial_battery_conditions
from .Network import Network 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Isolated_Battery_Cell
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Isolated_Battery_Cell_Network(Network):
    """ This is a test bench to analyze the discharge and charge profile 
        of a battery cell.
    
        Assumptions:
        None
        
        Source:
        None
    """  
    def __defaults__(self):
        """ This sets the default values for the network to function.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """      
        self.tag                     = 'isolated_battery_cell' 
        self.avionics                = RCAIDE.Library.Components.Systems.Avionics()
        self.payload                 = RCAIDE.Library.Components.Payloads.Payload()
        self.busses                  = Container()
        self.system_voltage          = None          
        
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Evaluate the state variables of a cycled cell
    
            Assumptions: 
            None
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs: 
            conditions.energy: 
                current                            [amps]
                battery.power                      [watts]
                initial.battery_state_of_charge    [joules]
                battery.voltage_open_circuit       [volts]
                battery.voltage_under_load         [volts]  
    
            Properties Used:
            Defaulted values
        """        
        
        # unpack   
        conditions      = state.conditions
        numerics        = state.numerics
        busses          = self.busses  
        recharging_flag = conditions.energy.recharging 
    
        for bus in busses: 
            avionics        = bus.avionics
            payload         = bus.payload  
            batteries       = bus.batteries
    
            # Avionics Power Consumtion 
            avionics.power() 
    
            # Payload Power 
            payload.power() 
    
            # Bus Voltage 
            bus_voltage = bus.voltage * state.ones_row(1)
            if recharging_flag:
                for battery in batteries:   
                    # append compoment power to bus 
                    avionics_power         = (avionics.inputs.power*battery.bus_power_split_ratio)/len(batteries)* state.ones_row(1)
                    payload_power          = (payload.inputs.power*battery.bus_power_split_ratio)/len(batteries)* state.ones_row(1)            
                    total_esc_power        = 0 * state.ones_row(1)     
                    charging_power         = (state.conditions.energy[bus.tag][battery.tag].pack.current*bus_voltage*battery.bus_power_split_ratio)/len(batteries)
                   
                    # append bus outputs to battery 
                    battery.outputs.power       = ((avionics_power + payload_power + total_esc_power) - charging_power)/bus.efficiency
                    battery.outputs.current     = -battery.outputs.power/bus_voltage
                    battery.energy_calc(state,bus,recharging_flag)    
            
            else:
                # compute energy calculation for each battery on bus  
                for battery in batteries:  
                    # compute power from each componemnt 
                    avionics_power  = (avionics.inputs.power*battery.bus_power_split_ratio)/len(batteries)* state.ones_row(1) 
                    payload_power   = (payload.inputs.power*battery.bus_power_split_ratio)/len(batteries) * state.ones_row(1)  
                    charging_power  = bus.charging_power*battery.bus_power_split_ratio/len(batteries)
                    total_esc_power = state.conditions.energy[bus.tag][battery.tag].pack.current*bus_voltage*battery.bus_power_split_ratio
                       
                    # append bus outputs to battery 
                    battery.outputs.power       = ((avionics_power + payload_power + total_esc_power) - charging_power)/bus.efficiency
                    battery.outputs.current     = battery.outputs.power/bus_voltage
                    battery.energy_calc(state,bus,recharging_flag)   
    
        conditions.energy.thrust_force_vector  =  0. * state.ones_row(3)     
        conditions.energy.power                = state.ones_row(1)*0.0        
        conditions.energy.vehicle_mass_rate    = state.ones_row(1)*0.0  
    
        # --------------------------------------------------        
        # A PATCH TO BE DELETED IN RCAIDE
        results                           = Data()
        results.thrust_force_vector       = state.ones_row(3)*0.0 
        results.vehicle_mass_rate         = state.ones_row(1)*0.0         
        # --------------------------------------------------     
        
        return results  
      
    def add_unknowns_and_residuals_to_segment(self, 
                                              segment,  
                                              estimated_battery_voltages          = [[400]] ):
        """ This function sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
            self                                [None]
            segment                             [None]
            estimated_battery_voltages          [volts]
            estimated_battery_cell_temperature  [Kelvin]
            estimated_battery_state_of_charges  [unitless]
            estimated_battery_cell_currents     [Amperes]
            
            Outputs
            None
            
            Properties Used:
            N/A
        """          
        busses   = segment.analyses.energy.networks.isolated_battery_cell.busses
        ones_row = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  
         
        for bus_i, bus in enumerate(busses):   
            batteries                 = bus.batteries 

            # ------------------------------------------------------------------------------------------------------            
            # Create bus results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[bus.tag] = RCAIDE.Framework.Mission.Common.Conditions()            

            # ------------------------------------------------------------------------------------------------------            
            # Determine number of propulsor groups in bus
            # ------------------------------------------------------------------------------------------------------ 
            bus_results                             = segment.state.conditions.energy[bus.tag] 
             
            # ------------------------------------------------------------------------------------------------------
            # Assign battery residuals, unknowns and results data structures 
            # ------------------------------------------------------------------------------------------------------   
                
            for b_i , battery in enumerate(batteries):         
                bus_results[battery.tag]                               = RCAIDE.Framework.Mission.Common.Conditions() 
                bus_results[battery.tag].pack                          = RCAIDE.Framework.Mission.Common.Conditions() 
                bus_results[battery.tag].cell                          = RCAIDE.Framework.Mission.Common.Conditions() 
                bus_results[battery.tag].pack.energy                   = 0 * ones_row(1)    
                bus_results[battery.tag].pack.current                  = segment.current * ones_row(1)   
                bus_results[battery.tag].pack.voltage_open_circuit     = 0 * ones_row(1)  
                bus_results[battery.tag].pack.voltage_under_load       = 0 * ones_row(1)  
                bus_results[battery.tag].pack.power                    = 0 * ones_row(1)   
                bus_results[battery.tag].pack.temperature              = 0 * ones_row(1)   
                bus_results[battery.tag].pack.heat_energy_generated    = 0 * ones_row(1)   
                bus_results[battery.tag].pack.internal_resistance      = 0 * ones_row(1)   
                bus_results[battery.tag].cell.heat_energy_generated    = 0 * ones_row(1)    
                bus_results[battery.tag].cell.state_of_charge          = 0 * ones_row(1)   
                bus_results[battery.tag].cell.power                    = 0 * ones_row(1)         
                bus_results[battery.tag].cell.energy                   = 0 * ones_row(1)         
                bus_results[battery.tag].cell.voltage_under_load       = 0 * ones_row(1)         
                bus_results[battery.tag].cell.voltage_open_circuit     = 0 * ones_row(1)        
                bus_results[battery.tag].cell.current                  = 0 * ones_row(1)         
                bus_results[battery.tag].cell.temperature              = 0 * ones_row(1)         
                bus_results[battery.tag].cell.charge_throughput        = 0 * ones_row(1)         
                bus_results[battery.tag].cell.depth_of_discharge       = 0 * ones_row(1)
                bus_results[battery.tag].cell.cycle_in_day             = 0
                bus_results[battery.tag].cell.resistance_growth_factor = 1.
                bus_results[battery.tag].cell.capacity_fade_factor     = 1.
                bus_results[battery.tag].thermal_management_system.heat_generated                 = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.power                          = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HAS.inlet_coolant_pressure     = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HAS.heat_removed               = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HAS.inlet_coolant_temperature  = 0 * ones_row(1)   
                bus_results[battery.tag].thermal_management_system.HAS.outlet_coolant_temperature = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HAS.coolant_mass_flow_rate     = 0 * ones_row(1)  
                bus_results[battery.tag].thermal_management_system.HAS.effectiveness              = 0 * ones_row(1)
                bus_results[battery.tag].thermal_management_system.HAS.power                      = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HEX.coolant_mass_flow_rate     = 0 * ones_row(1)  
                bus_results[battery.tag].thermal_management_system.HEX.power                      = 0 * ones_row(1)  
                bus_results[battery.tag].thermal_management_system.HEX.inlet_air_temperature      = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HEX.outlet_coolant_temperature = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HEX.air_mass_flow_rate         = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HEX.coolant_mass_flow_rate     = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HEX.air_inlet_pressure         = 0 * ones_row(1) 
                bus_results[battery.tag].thermal_management_system.HEX.coolant_inlet_pressure     = 0 * ones_row(1)   
                bus_results[battery.tag].thermal_management_system.HEX.effectiveness_HEX          = 0 * ones_row(1)
                bus_results[battery.tag].thermal_management_system.HEX.pressure_diff_air          = 0 * ones_row(1)
                bus_results[battery.tag].thermal_management_system.RES.coolant_temperature        = 0 * ones_row(1)
               
                
                append_initial_battery_conditions(segment,bus,battery)      
                
                # appennd residuals and unknowns for recharge segment                     
                segment.state.unknowns['fv_' + battery.tag]          =  0* ones_row(1)  
                segment.state.residuals.network['fv_' + battery.tag] =  0* ones_row(1)       

        return segment
    
    __call__ = evaluate_thrust


