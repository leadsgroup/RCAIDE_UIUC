# Regression/scripts/Tests/network_ducted_fan/electric_ducted_fan_netowrk.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  

import RCAIDE
from RCAIDE.Framework.Core                                    import Units, Data
from RCAIDE.Library.Plots                                     import *     
from RCAIDE.Framework.Mission.Common                          import Conditions, Results, Residuals  
from RCAIDE.Library.Methods.Propulsors.Converters.Motor       import design_DC_motor 
from RCAIDE.Library.Methods.Propulsors.Converters.Ducted_Fan  import design_ducted_fan 
# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  
import os

# ----------------------------------------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------------------------------------

def main(): 
    ducted_fan_type  = ['Blade_Element_Momentum_Theory', 'Rankine_Froude_Momentum_Theory']
    # omega_truth = [36.455819245889195,37.653244590335106]
    # torque_truth = [145.0992694988849,145.7740091588354]
    # current_truth = [73.5454727365098,73.0]
    # voltage_truth = [120,120.0]

    for i in range(len(ducted_fan_type)): 
        EDF = design_electric_ducted_fan(ducted_fan_type[i])  
  

        # run analysis 
        omega = motor_conditions.omega
        torque = motor_conditions.torque
        current = motor_conditions.current
        voltage = motor_conditions.voltage
 
        # Truth values 
        error = Data()
        error.omega_test     = np.max(np.abs(omega_truth[i]   - omega[0][0]  ))
        error.torque_test    = np.max(np.abs(torque_truth[i]  - torque[0][0] ))
        error.current_test   = np.max(np.abs(current_truth[i] - current[0][0])) 
        error.voltage_test   = np.max(np.abs(voltage_truth[i] - voltage[0][0])) 
        
        print('Errors:')
        print(error)
        
        for k,v in list(error.items()):
            assert(np.abs(v)<1e-6) 
               
    return
 
def design_electric_ducted_fan(regression_flag):
     #------------------------------------------------------------------------------------------------------------------------------------  
    #  Starboard Propulsor
    #------------------------------------------------------------------------------------------------------------------------------------   
    EDF                              = RCAIDE.Library.Components.Propulsors.Electric_Ducted_Fan()   
  
    # Electronic Speed Controller       
    esc                                          = RCAIDE.Library.Components.Energy.Modulators.Electronic_Speed_Controller()
    esc.tag                                      = 'esc_1'
    esc.efficiency                               = 0.95 
    EDF.electronic_speed_controller              = esc   
           
    # Ducted_fan                            
    ducted_fan                                   = RCAIDE.Library.Components.Propulsors.Converters.Ducted_Fan()
    ducted_fan.tag                               = 'ducted_fan'
    ducted_fan.number_of_rotor_blades            = 12 #22 
    ducted_fan.number_of_radial_stations         = 20
    ducted_fan.tip_radius                        = 6 * Units.inches  / 2
    ducted_fan.hub_radius                        = 6* 0.25  * Units.inches /2 
    ducted_fan.blade_clearance                   = 0.001
    ducted_fan.length                            = 10. * Units.inches
    ducted_fan.rotor_percent_x_location          = 0.4
    ducted_fan.stator_percent_x_location         = 0.7
    ducted_fan.cruise.design_thrust              = 60 *  Units.lbs
    ducted_fan.cruise.design_altitude            = 1000    
    ducted_fan.cruise.design_tip_mach            = 0.7
    ducted_fan.cruise.design_angular_velocity    = (ducted_fan.cruise.design_tip_mach *320) /ducted_fan.tip_radius  # 1352 RPM
    ducted_fan.cruise.design_freestream_velocity = 120 *  Units.mph
    ducted_fan.cruise.design_reference_velocity  = 120 *  Units.mph
    airfoil                                      = RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil() 
    airfoil.NACA_4_Series_code                   = '2208'
    ducted_fan.append_duct_airfoil(airfoil)  
    airfoil                                      = RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil()
    airfoil.NACA_4_Series_code                   = '0008'    
    ducted_fan.append_hub_airfoil(airfoil) 
    dfdc_bin_name = '/Users/matthewclarke/Documents/LEADS/CODES/DFDC/bin/dfdc'
    keep_files    =  True 
    design_ducted_fan(ducted_fan,dfdc_bin_name,regression_flag,keep_files) 
    EDF.ducted_fan                  = ducted_fan   
              
    # DC_Motor       
    motor                                         = RCAIDE.Library.Components.Propulsors.Converters.DC_Motor()
    motor.efficiency                              = 0.98
    motor.origin                                  = [[2.,  2.5, 0.95]]
    motor.nominal_voltage                         = 100
    motor.no_load_current                         = 0.01
    motor.rotor_radius                            = ducted_fan.tip_radius
    motor.design_torque                           = ducted_fan.cruise.design_torque
    motor.angular_velocity                        = ducted_fan.cruise.design_angular_velocity 
    design_DC_motor(motor)   
    motor.mass_properties.mass                    = compute_motor_weight(motor) 
    EDF.motor                        = motor 
    
    return EDF
 
if __name__ == '__main__': 
    main()    
    plt.show()
        
