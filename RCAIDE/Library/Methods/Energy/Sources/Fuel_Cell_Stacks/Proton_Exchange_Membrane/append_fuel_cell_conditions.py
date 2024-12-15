# RCAIDE/Methods/Energy/Sources/Battery/Lithium_Ion_LFP/compute_lfp_cell_performance.py
# 
# 
# Created: Nov 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE 
from RCAIDE.Framework.Mission.Common     import   Conditions 

# ----------------------------------------------------------------------------------------------------------------------
# compute_lfp_cell_performance
# ----------------------------------------------------------------------------------------------------------------------  
def append_fuel_cell_conditions(fuel_cell_stack,segment,bus): 
 
    ones_row                                                                                    = segment.state.ones_row    
                                             
    bus_results                                                                                 = segment.state.conditions.energy[bus.tag]        
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag]                                           = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell                                 = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs                          = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.outputs                         = Conditions()

    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].power                                     = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].current                                   = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_to_air_ratio                         = fuel_cell_stack.fuel_cell.fuel_to_air_ratio* ones_row(1)    
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].voltage_open_circuit                      = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].voltage_under_load                        = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.voltage_open_circuit            = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.voltage_under_load              = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.power                           = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.current                         = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.current_density                 = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.stagnation_temperature          = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.stagnation_pressure             = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.p_drop_fc                       = fuel_cell_stack.fuel_cell.rated_p_drop_fc * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.p_drop_hum                      = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.air_excess_ratio                = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.stack_temperature               = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.hydrogen_pressure        = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.air_pressure             = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.fuel_mass_flow_rate      = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.oxidizer_mass_flow_rate  = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.oxygen_relative_humidity        = 1 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.degradation                     = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.p_air_out                       = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.mdot_air_in                     = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.outputs.oxidizer_mass_flow_rate = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.p_in_comp                       = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.pi_comp                         = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.mdot_in_comp                    = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.mdot_out_exp                    = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.p_in_exp                        = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.pi_exp                          = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.P_comp                          = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.P_motor_comp                    = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.P_exp                           = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.P_generator_exp                 = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.CEM_power                       = 0 * ones_row(1)
           
    # Conditions for recharging fuel_cell 
    if isinstance(segment,RCAIDE.Framework.Mission.Segments.Ground.Recharge):
        segment.state.conditions.energy.recharging  = True  
        segment.state.unknowns['recharge']          =  0* ones_row(1)  
        segment.state.residuals.network['recharge'] =  0* ones_row(1)
    elif type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Discharge:
        segment.state.conditions.energy.recharging   = False     
        segment.state.unknowns['recharge']          =  0* ones_row(1)  
        segment.state.residuals.network['recharge'] =  0* ones_row(1)
    else:
        segment.state.conditions.energy.recharging  = False            
    
    return

def append_fuel_cell_segment_conditions(fuel_cell_stack, bus, conditions, segment):
    
    
    return


def reuse_stored_fuel_cell_data():
    
    
    return 