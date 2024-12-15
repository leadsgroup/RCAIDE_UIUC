# RCAIDE/Methods/Energy/Sources/Battery/Common/compute_module_properties.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Framework.Core import Units 
import  numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ----------------------------------------------------------------------------------------------------------------------  
def compute_stack_properties(fuel_cell_stack):  
    """Calculate fuel_cell_stack level properties of battery module using cell 
    properties and module configuraton
    
    Assumptions: 
    Inputs:
    mass              
    fuel_cell_stack.cell
      nominal_capacity        [amp-hours]            
      nominal_voltage         [volts]
      pack_config             [unitless]
      mass                    [kilograms]
                          
    Outputs:              
     fuel_cell_stack.             
       maximum_energy         [watt-hours]
       maximum_power              [watts]
       initial_maximum_energy [watt-hours]
       specific_energy        [watt-hours/kilogram]
       charging_voltage       [volts]
       mass_properties.    
        mass                  [kilograms] 
    """
     
    
    series_e           = fuel_cell_stack.electrical_configuration.series
    parallel_e         = fuel_cell_stack.electrical_configuration.parallel 
    normal_count       = fuel_cell_stack.geometrtic_configuration.normal_count  
    parallel_count     = fuel_cell_stack.geometrtic_configuration.parallel_count
    stacking_rows      = fuel_cell_stack.geometrtic_configuration.stacking_rows

    if int(parallel_e*series_e) != int(normal_count*parallel_count):
        pass #raise Exception('Number of cells in gemetric layout not equal to number of cells in electric circuit configuration ')
         
    normal_spacing     = fuel_cell_stack.geometrtic_configuration.normal_spacing   
    parallel_spacing   = fuel_cell_stack.geometrtic_configuration.parallel_spacing
    volume_factor      = fuel_cell_stack.volume_packaging_factor 
    euler_angles       = fuel_cell_stack.orientation_euler_angles
    fuel_cell_length   = fuel_cell_stack.fuel_cell.length 
    fuel_cell_width    = fuel_cell_stack.fuel_cell.width   
    fuel_cell_height   = fuel_cell_stack.fuel_cell.height   
    weight_factor      = fuel_cell_stack.additional_weight_factor
    
    x1 =  normal_count * (fuel_cell_length +  normal_spacing) * volume_factor # distance in the module-level normal direction
    x2 =  parallel_count *  (fuel_cell_width +parallel_spacing) * volume_factor # distance in the module-level parallel direction
    x3 =  fuel_cell_height * volume_factor # distance in the module-level height direction 

    length = x1 / stacking_rows
    width  = x2
    height = x3 *stacking_rows     
    
    if  euler_angles[0] == (np.pi / 2):
        x1prime      = x2
        x2prime      = -x1
        x3prime      = x3 
    if euler_angles[1] == (np.pi / 2):
        x1primeprime = -x3prime
        x2primeprime = x2prime
        x3primeprime = x1prime
    if euler_angles[2] == (np.pi / 2):
        length       = x1primeprime
        width        = x3primeprime
        height       = -x2primeprime

    # store length, width and height
    fuel_cell_stack.length = length
    fuel_cell_stack.width  = width
    fuel_cell_stack.height = height 
    
    
    P_fc    =  fuel_cell_stack.fuel_cell.rated_power_density *  fuel_cell_stack.fuel_cell.interface_area
    I_fc    =  fuel_cell_stack.fuel_cell.rated_current_density *  fuel_cell_stack.fuel_cell.interface_area
    I_stack = I_fc * parallel_e
    V_fc    = P_fc / I_fc
    V_stack = V_fc  * series_e
    P_stack = V_stack * I_stack
    
    fuel_cell_stack.voltage         = V_stack
    fuel_cell_stack.maximum_voltage = V_stack  
    fuel_cell_stack.maximum_current = I_stack 
    fuel_cell_stack.maximum_power   = P_stack   
     