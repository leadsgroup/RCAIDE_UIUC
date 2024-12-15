## @ingroup Methods-Power-Fuel_Cell-Sizing

# initialize_from_power.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Feb 2016, E. Botero
           
# ----------------------------------------------------------------------
#  Initialize from Power
# ---------------------------------------------------------------------- 
def initialize_from_power(fuel_cell_stack,power):
    '''
    assigns the mass of the fuel cell based on the power and specific power
    Assumptions:
    None
    
    Inputs:
    power            [J]
    fuel_cell.
      specific_power [W/kg]
    
    
    Outputs:
    fuel_cell.
      mass_properties.
        mass         [kg]
    '''
    fuel_cell =  fuel_cell_stack.fuel_cell
    fuel_cell_stack.mass_properties.mass = power/fuel_cell.specific_power
