# RCAIDE/Library/Methods/Energy/Source/Fuel_Cells/Proton_Exchange_Membrane/pack_PEM_residuals.py 
# 
# Created:  Jun 2025, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  pack fuel cell residuals
# ----------------------------------------------------------------------------------------------------------------------  

def pack_PEM_residuals(fuel_cell_stack,bus,segment):
    '''
    Packs residuals for PEM fuel cell 
    '''
    bus_conditions  = segment.state.conditions.energy[bus.tag] 
    P_bus           = bus_conditions.power_draw 
    p_system        = P_bus/len(bus.fuel_cell_stacks) 
    p_fuel_cell     = segment.state.conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag].power
    segment.state.residuals[fuel_cell_stack.tag  + '_power'] = (p_system - p_fuel_cell) / 1E4
    return 
