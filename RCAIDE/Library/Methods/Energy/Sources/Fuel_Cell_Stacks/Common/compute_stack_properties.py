# RCAIDE/Methods/Energy/Sources/Battery/Common/compute_module_properties.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Cell_Stacks.Larminie_Model import  compute_power, compute_voltage
import  scipy as  sp
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
        raise Exception('Number of cells in gemetric layout not equal to number of cells in electric circuit configuration ')
         
    normal_spacing     = fuel_cell_stack.geometrtic_configuration.normal_spacing   
    parallel_spacing   = fuel_cell_stack.geometrtic_configuration.parallel_spacing
    volume_factor      = fuel_cell_stack.volume_packaging_factor 
    euler_angles       = fuel_cell_stack.orientation_euler_angles
    fuel_cell_length   = fuel_cell_stack.fuel_cell.length 
    fuel_cell_width    = fuel_cell_stack.fuel_cell.width   
    fuel_cell_height   = fuel_cell_stack.fuel_cell.height    
    
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
     
    if isinstance(fuel_cell_stack, RCAIDE.Library.Components.Energy.Sources.Fuel_Cell_Stacks.Generic_Fuel_Cell_Stack):
        fuel_cell                            = fuel_cell_stack.fuel_cell 
        lb                                   = 0.0001/(Units.cm**2.)    #lower bound on fuel cell current density
        ub                                   = 1.2/(Units.cm**2.)
        sign                                 = -1. #used to minimize -power
        current_density                      = sp.optimize.fminbound(compute_power, lb, ub, args=(fuel_cell, sign))
        power_per_cell                       = compute_power(current_density,fuel_cell) 
        V_fc                                 = compute_voltage(fuel_cell,current_density)  #useful voltage vector 
        
        fuel_cell.volume                     = parallel_e *series_e *fuel_cell.interface_area*fuel_cell.wall_thickness
        fuel_cell_stack.mass_properties.mass = fuel_cell.volume*fuel_cell.cell_density*fuel_cell.porosity_coefficient #fuel cell mass in kg
        fuel_cell.mass_density               = fuel_cell_stack.mass_properties.mass/  fuel_cell.volume                      
        fuel_cell.specific_power             = fuel_cell.max_power/fuel_cell_stack.mass_properties.mass #fuel cell specific power in W/kg


        fuel_cell_stack.voltage         = V_fc  * series_e
        fuel_cell_stack.maximum_voltage = V_fc  * series_e
        #fuel_cell_stack.maximum_power   = power_per_cell * series_e 
        #fuel_cell_stack.maximum_current =  fuel_cell_stack.maximum_power / fuel_cell_stack.maximum_voltage
 
 
  