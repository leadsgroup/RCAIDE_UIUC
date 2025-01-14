## @ingroup Methods-Power-Fuel_Cell-Discharge
# compute_power_difference.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Sep 2015, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from .compute_power import compute_power

# ----------------------------------------------------------------------
#  Find Power Difference Larminie
# ----------------------------------------------------------------------
## @ingroup Methods-Power-Fuel_Cell-Discharge
def compute_power_difference(current_density, fuel_cell, power_desired):
    '''
    function that determines the power difference between the actual power
    and a desired input power, based on an input current density

    Assumptions:
    None
    
    Inputs:
    current_density                [Amps/m**2]
    power_desired                  [Watts]
    fuel_cell
      
    
    Outputs
    (power_desired-power_out)**2   [Watts**2]
    '''
    #obtain power output in W
    
    power_out     = compute_power(current_density, fuel_cell)              
    
    #want to minimize
    return (power_desired-power_out)**2.#abs(power_desired-power_out)