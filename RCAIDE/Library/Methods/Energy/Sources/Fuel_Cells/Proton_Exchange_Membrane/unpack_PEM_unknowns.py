# RCAIDE/Library/Methods/Energy/Source/Fuel_Cells/Proton_Exchange_Membrane/unpack_PEM_unknowns.py 
# Created:  Jun 2025, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  unpack electric ducted_fan network unknowns 
# ----------------------------------------------------------------------------------------------------------------------  

def unpack_PEM_unknowns(fuel_cell_stack,bus,segment):
    '''
    Unpacks unknowns for PEM fuel cell 
    '''
    fuel_cell_stack_conditions  = segment.state.conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag]
    fuel_cell_stack_conditions.fuel_cell.current_density  = segment.state.unknowns[fuel_cell_stack.tag  + '_current_density']  