# dc_motor_test.py
# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

#----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core                              import Units, Data
from RCAIDE.Library.Plots                               import *     
from RCAIDE.Library.Methods.Performance                 import propeller_aerodynamic_analysis
from RCAIDE.Framework.Analyses.Atmospheric              import US_Standard_1976
from RCAIDE.Framework.Mission.Common import Conditions, Results, Residuals
from RCAIDE.Library.Methods.Propulsors.Converters import Motor
from RCAIDE.Library.Methods.Propulsors.Converters.Motor.design_DC_motor import design_DC_motor

import os
import numpy as np 
import matplotlib.pyplot as plt

# python imports 
import numpy as np
import pylab as plt 
import sys
import os

# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles' + os.path.sep + 'Rotors'))
from Test_Propeller    import Test_Propeller   
 
def main(): 
    motor_type  = ['DC_Motor', 'PMSM_Motor']
    omega_truth = [36.455819245889195,82.33509483753275]
    torque_truth = [145.0992694988849,14.577400915883537]
    current_truth = [73.5454727365098,73.0]
    voltage_truth = [120,120.0]

    for i in range(len(motor_type)):
        prop = Test_Propeller() 
        motor = design_test_motor(prop, motor_type[i])

        bus                                            = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus()
        bus.voltage                                   = 120                         
        electric_rotor                                = RCAIDE.Library.Components.Propulsors.Electric_Rotor()  
        electric_rotor.motor                          = motor 
        electric_rotor.rotor                          = prop
 
        # set up conditions  
        ctrl_pts = 1
        altitude = 0
        mach_number = 0.3
        atmosphere                                             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976() 
        atmo_data                                              = atmosphere.compute_values(altitude = altitude) 
        segment                                                = RCAIDE.Framework.Mission.Segments.Segment()  
        conditions                                             = Results()  
        conditions.freestream.density                          = atmo_data.density  
        conditions.freestream.dynamic_viscosity                = atmo_data.dynamic_viscosity
        conditions.freestream.speed_of_sound                   = atmo_data.speed_of_sound
        conditions.freestream.temperature                      = atmo_data.temperature
        conditions.freestream.altitude                         = np.ones((ctrl_pts,1)) *altitude
        conditions.frames.inertial.velocity_vector             = np.array([[mach_number *atmo_data.speed_of_sound[0,0] , 0. ,0.]])     
        segment.state.conditions                               = conditions  
        segment.state.conditions.energy[bus.tag]               = Conditions() 
        

        segment.state.residuals.network = Residuals()
            
        electric_rotor.append_operating_conditions(segment) 

        for tag, propulsor_item in  electric_rotor.items():  
            if issubclass(type(propulsor_item), RCAIDE.Library.Components.Component):
                propulsor_item.append_operating_conditions(segment,electric_rotor)            
        
    
        # ------------------------------------------------------------------------------------------------------            
        # Create bus results data structure  
        # ------------------------------------------------------------------------------------------------------
        segment.state.conditions.energy[bus.tag] = RCAIDE.Framework.Mission.Common.Conditions() 
        segment.state.conditions.noise[bus.tag]  = RCAIDE.Framework.Mission.Common.Conditions()   

        # ------------------------------------------------------------------------------------------------------
        # Assign network-specific  residuals, unknowns and results data structures
        # ------------------------------------------------------------------------------------------------------  
        electric_rotor.append_propulsor_unknowns_and_residuals(segment)

        # for tag, bus_item in  bus.items():  
        #     if issubclass(type(bus_item), RCAIDE.Library.Components.Component):
        #         bus_item.append_operating_conditions(segment,bus)
 

        motor_conditions = segment.state.conditions.energy[electric_rotor.tag][motor.tag]
                # Assign conditions to the rotor
        motor_conditions.voltage                   = np.ones((ctrl_pts,1)) * bus.voltage 

        if (type(motor) == RCAIDE.Library.Components.Propulsors.Converters.PMSM_Motor):
            motor_conditions.current = np.ones((ctrl_pts,1)) * 73
            Motor.compute_PMSM_motor_performance.compute_RPM_and_torque(motor,motor_conditions,conditions)
        else:
            motor_conditions.rotor_power_coefficient   = np.ones((ctrl_pts,1)) * 0.5
            Motor.compute_DC_motor_performance.compute_RPM_and_torque(motor,motor_conditions,conditions)
            Motor.compute_DC_motor_performance.compute_current_from_RPM_and_voltage(motor,motor_conditions,conditions) 

        # run analysis 
        omega = motor_conditions.omega
        torque = motor_conditions.torque
        current = motor_conditions.current
        voltage = motor_conditions.voltage

 
        # Truth values 
        error = Data()
        error.omega_test     = np.max(np.abs(omega_truth[i]   - omega[0][0]  ))
        error.torque_test_1  = np.max(np.abs(torque_truth[i]  - torque[0][0] ))
        error.current_test_1 = np.max(np.abs(current_truth[i] - current[0][0])) 
        error.voltage_test   = np.max(np.abs(voltage_truth[i] - voltage[0][0])) 
        
        print('Errors:')
        print(error)
        
        for k,v in list(error.items()):
            assert(np.abs(v)<1e-6) 
                    
               
    return

def design_test_motor(prop, motor_type):
    if motor_type == 'DC_Motor':
        motor = RCAIDE.Library.Components.Propulsors.Converters.DC_Motor()

        motor.mass_properties.mass = 9. * Units.kg 
        motor.efficiency           = 0.935
        motor.gear_ratio           = 1. 
        motor.gearbox_efficiency   = 1. # Gear box efficiency     
        motor.no_load_current      = 2.0 
        motor.propeller_radius     = prop.tip_radius
        motor.nominal_voltage      = 400
        motor.rotor_radius         = prop.tip_radius
        motor.design_torque        = prop.cruise.design_torque 
        motor.angular_velocity     = prop.cruise.design_angular_velocity # Horse power of gas engine variant  750 * Units['hp']
        design_DC_motor(motor) 
    elif motor_type == 'PMSM_Motor':
        motor = RCAIDE.Library.Components.Propulsors.Converters.PMSM_Motor()
    else:
        raise ValueError('Invalid motor type')
    return motor

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()