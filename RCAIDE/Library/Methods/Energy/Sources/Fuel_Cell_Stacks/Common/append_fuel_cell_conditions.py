# RCAIDE/Methods/Energy/Sources/fuel_cell/Lithium_Ion_LFP/compute_lfp_cell_performance.py
# 
# 
# Created: Nov 2024, M. Clarke
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
# compute_lfp_cell_performance
# ----------------------------------------------------------------------------------------------------------------------  
def append_fuel_cell_conditions(fuel_cell_stack,segment,bus):
    ones_row                                               = segment.state.ones_row  
                                             
    bus_results                                                                                 = segment.state.conditions.energy[bus.tag]        
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag]                                           = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell                                 = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs                          = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.outputs                         = Conditions()

    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].power                                     = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].voltage_under_load                        = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].current                                   = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].voltage_open_circuit                      = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.voltage_open_circuit            = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.current_density                 = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.current                         = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.fuel_mass_flow_rate      = 0 * ones_row(1)
    
    
    # Conditions for recharging fuel_cell 
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
    
    
    return
 
def append_fuel_cell_segment_conditions(fuel_cell, bus, conditions, segment):
    
    
    return


def reuse_stored_fuel_cell_data():
    
    
    return 