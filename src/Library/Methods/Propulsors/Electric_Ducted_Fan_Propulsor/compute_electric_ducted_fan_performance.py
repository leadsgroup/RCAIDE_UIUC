# RCAIDE/Methods/Energy/Propulsors/Electric_Ducted_Fan_Propulsor/compute_ducted_fan_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   
from RCAIDE.Library.Methods.Propulsors.Modulators.Electronic_Speed_Controller.compute_esc_performance  import * 
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor.compute_motor_performance                   import *
from RCAIDE.Library.Methods.Propulsors.Converters.Ducted_Fan.compute_ducted_fan_performance            import * 

# pacakge imports  
import numpy as np 
from copy import deepcopy

# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_ducted_fan_performance
# ----------------------------------------------------------------------------------------------------------------------  
def compute_electric_ducted_fan_performance(propulsor,state,voltage,center_of_gravity= [[0.0, 0.0,0.0]]):   
    ''' Computes the perfomrance of one propulsor
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-] 
    voltage              - system voltage                         [V]
    bus                  - bus                                    [-] 
    propulsor            - propulsor data structure               [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A]

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A]
    stored_results_flag  - boolean for stored results             [-]     
    stored_propulsor_tag - name of propulsor with stored results  [-]
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                 = state.conditions    
    ducted_fan_conditions      = conditions.energy[propulsor.tag] 
    motor                      = propulsor.motor 
    ducted_fan                 = propulsor.ducted_fan 
    esc                        = propulsor.electronic_speed_controller  
    esc_conditions             = ducted_fan_conditions[esc.tag]
    motor_conditions           = ducted_fan_conditions[motor.tag]
    ducted_fan_conditions      = ducted_fan_conditions[ducted_fan.tag]
    eta                        = conditions.energy[propulsor.tag].throttle
    
    esc_conditions.inputs.voltage   = voltage
    esc_conditions.throttle         = eta 
    compute_voltage_out_from_throttle(esc,esc_conditions,conditions)

    # Assign conditions to the ducted_fan
    motor_conditions.voltage              = esc_conditions.outputs.voltage 
    compute_RPM_and_torque_from_power_coefficent_and_voltage(motor,motor_conditions,conditions)
    
    # Spin the ducted_fan 
    ducted_fan_conditions.omega              = motor_conditions.omega
    ducted_fan_conditions.tip_mach           = (motor_conditions.omega * ducted_fan.tip_radius) / conditions.freestream.speed_of_sound
    ducted_fan_conditions.throttle           = esc_conditions.throttle
    ducted_fan_conditions.operating_altitude = conditions.freestream.altitude
    ducted_fan_conditions.inflow_velocity    = conditions.freestream.velocity
    compute_ducted_fan_performance(propulsor,state,center_of_gravity)  

    # Run the motor for current
    compute_current_from_RPM_and_voltage(motor,motor_conditions,conditions)
    
    # Detemine esc current 
    esc_conditions.outputs.current = motor_conditions.current
    compute_current_in_from_throttle(esc,esc_conditions,conditions)  
    esc_conditions.current         = esc_conditions.inputs.current  
    esc_conditions.power           = esc_conditions.inputs.power
    
    stored_results_flag            = True
    stored_propulsor_tag           = propulsor.tag 
    
    # compute total forces and moments from propulsor (future work would be to add moments from motors)
    ducted_fan_conditions.thrust      = conditions.energy[propulsor.tag][ducted_fan.tag].thrust 
    ducted_fan_conditions.moment      = conditions.energy[propulsor.tag][ducted_fan.tag].moment 
    
    T  = conditions.energy[propulsor.tag][ducted_fan.tag].thrust 
    M  = conditions.energy[propulsor.tag][ducted_fan.tag].moment 
    P  = conditions.energy[propulsor.tag][esc.tag].power 
    
    return T,M,P, stored_results_flag,stored_propulsor_tag 
                
def reuse_stored_electric_ducted_fan_data(propulsor,state,network,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one propulsor for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-] 
    voltage              - system voltage                         [V]
    bus                  - bus                                    [-] 
    propulsors           - propulsor data structure               [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A]

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                 = state.conditions 
    motor                      = propulsor.motor 
    ducted_fan                 = propulsor.ducted_fan 
    esc                        = propulsor.electronic_speed_controller  
    motor_0                    = network.propulsors[stored_propulsor_tag].motor 
    ducted_fan_0               = network.propulsors[stored_propulsor_tag].ducted_fan 
    esc_0                      = network.propulsors[stored_propulsor_tag].electronic_speed_controller
    
    conditions.energy[propulsor.tag][motor.tag]        = deepcopy(conditions.energy[stored_propulsor_tag][motor_0.tag])
    conditions.energy[propulsor.tag][ducted_fan.tag]   = deepcopy(conditions.energy[stored_propulsor_tag][ducted_fan_0.tag])
    conditions.energy[propulsor.tag][esc.tag]          = deepcopy(conditions.energy[stored_propulsor_tag][esc_0.tag])
  
    thrust                  = conditions.energy[propulsor.tag][ducted_fan.tag].thrust 
    power                   = conditions.energy[propulsor.tag][esc.tag].power 
    
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
    moment                  = np.cross(moment_vector, thrust)
    
    conditions.energy[propulsor.tag][ducted_fan.tag].moment = moment  
    conditions.energy[propulsor.tag].thrust            = thrust   
    conditions.energy[propulsor.tag].moment            = moment  
    
    return thrust,moment,power