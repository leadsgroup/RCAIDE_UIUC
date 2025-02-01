# Regression/scripts/Tests/network_ducted_fan/electric_ducted_fan_netowrk.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  

import RCAIDE
from RCAIDE.Framework.Core                              import Units, Data
from RCAIDE.Library.Plots                               import *     
from RCAIDE.Framework.Mission.Common import Conditions, Results, Residuals  
from RCAIDE.Library.Methods.Propulsors.Converters import Motor
# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  
import os
# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from NASA_X48    import vehicle_setup as vehicle_setup
from NASA_X48    import configs_setup as configs_setup 
from RCAIDE.Library.Methods.Propulsors.Converters.Motor          import design_DC_motor 
# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles' + os.path.sep + 'Rotors'))
from Test_Propeller    import Test_Propeller  
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
        prop = Test_Propeller() 
        motor = design_test_motor(prop)

        bus                                            = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus()
        bus.voltage                                   = 120                         
        electric_rotor                                = RCAIDE.Library.Components.Propulsors.Electric_Rotor()  
        electric_rotor.motor                          = motor 
        electric_rotor.rotor                          = prop
 
        # set up conditions  
        ctrl_pts = 1
        altitude = 0
        mach_number = 0.3
        PMSM_current = 73

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

        motor_conditions = segment.state.conditions.energy[electric_rotor.tag][motor.tag]
                # Assign conditions to the rotor
        motor_conditions.voltage                   = np.ones((ctrl_pts,1)) * bus.voltage 
        motor_conditions.rotor_power_coefficient   = np.ones((ctrl_pts,1)) * 0.5
        Motor.compute_motor_performance(motor,motor_conditions,conditions)

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



def design_test_motor(prop):
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
    return motor

def define_ducted_fan():
    
    ducted_fan                                   = RCAIDE.Library.Components.Propulsors.Converters.Ducted_Fan()
    ducted_fan.tag                               = 'test_ducted_fan'
    ducted_fan.eta_p                             = 0.9
    ducted_fan.K_fan                             = 0.9
    ducted_fan.epsilon_d                         = 0.9
    ducted_fan.A_R                               = 0.9

    ducted_fan.number_of_rotor_blades            = 12 #22 
    ducted_fan.number_of_radial_stations         = 20
    ducted_fan.tip_radius                        = 3.124 / 2
    ducted_fan.hub_radius                        = 3.124 /2 * 0.25
    ducted_fan.blade_clearance                   = 0.01
    ducted_fan.length                            = 2
    ducted_fan.rotor_percent_x_location          = 0.4
    ducted_fan.stator_percent_x_location         = 0.7
    ducted_fan.cruise.design_thrust              = 10000  
    ducted_fan.cruise.design_altitude            = 20000 *Units.ft  
    ducted_fan.cruise.design_tip_mach            = 0.7
    ducted_fan.cruise.design_torque            = 400
    speed_of_sound                               =  316.032
    ducted_fan.cruise.design_angular_velocity    = (ducted_fan.cruise.design_tip_mach *speed_of_sound) /ducted_fan.tip_radius  # 1352 RPM
    ducted_fan.cruise.design_freestream_velocity = 0.45* speed_of_sound
    ducted_fan.cruise.design_reference_velocity  = 0.45*  speed_of_sound  
    
    return ducted_fan 


def define_electronic_speed_controller():

    # Electronic Speed Controller       
    esc                                              = RCAIDE.Library.Components.Energy.Modulators.Electronic_Speed_Controller()
    esc.tag                                          = 'esc'
    esc.efficiency                                   = 0.95        
    return esc


if __name__ == '__main__': 
    main()    
    plt.show()
        
