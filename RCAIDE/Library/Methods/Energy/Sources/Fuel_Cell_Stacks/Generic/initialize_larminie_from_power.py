## @ingroup Methods-Power-Fuel_Cell-Sizing
# initialize_larminie_from_power.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Sep 2015, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from RCAIDE.Framework.Core import Units
from .find_power_larminie import find_power_larminie

import scipy as sp
import numpy as np

# ----------------------------------------------------------------------
#  Initialize Larminie from Power
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Sizing
def initialize_larminie_from_power(fuel_cell_stack,power): 
    '''
    Initializes extra paramters for the fuel cell when using the larminie method
    Determines the number of stacks
    
    Inputs:
    power                 [W]
    fuel_cell
    
    Outputs:
    
    fuel_cell.
        power_per_cell    [W]
        number_of_cells
        max_power         [W]
        volume            [m**3]
        specific_power    [W/kg]
        mass_properties.
            mass          [kg]
       
        
    ''' 
    fuel_cell                            = fuel_cell_stack.fuel_cell 
    lb                                   = .1*Units.mA/(Units.cm**2.)    #lower bound on fuel cell current density
    ub                                   = 1200.0*Units.mA/(Units.cm**2.)
    sign                                 = -1. #used to minimize -power
    current_density                      = sp.optimize.fminbound(find_power_larminie, lb, ub, args=(fuel_cell, sign))
    power_per_cell                       = find_power_larminie(current_density,fuel_cell)
    
    fuel_cell.number_of_cells            = np.ceil(power/power_per_cell)
    fuel_cell.max_power                  = fuel_cell.number_of_cells*power_per_cell
    fuel_cell.volume                     = fuel_cell.number_of_cells*fuel_cell.interface_area*fuel_cell.wall_thickness
    fuel_cell_stack.mass_properties.mass = fuel_cell.volume*fuel_cell.cell_density*fuel_cell.porosity_coefficient #fuel cell mass in kg
    fuel_cell.mass_density               = fuel_cell_stack.mass_properties.mass/  fuel_cell.volume                      
    fuel_cell.specific_power             = fuel_cell.max_power/fuel_cell_stack.mass_properties.mass #fuel cell specific power in W/kg
    
    return 