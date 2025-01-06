# RCAIDE/Library/Methods/Propulsors/Converters/DC_Motor/compute_motor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_omega_and_Q_from_Cp_and_V
# ----------------------------------------------------------------------------------------------------------------------    
def compute_RPM_and_torque_from_power_coefficent_and_voltage(motor,motor_conditions,conditions):
    """Calculates the motors RPM and torque using power coefficient and operating voltage.
    The following perperties of the motor are computed  
    motor_conditions.torque                    (numpy.ndarray):  torque [Nm]
    motor_conditions.omega                     (numpy.ndarray):  omega  [radian/s] 

    Assumptions: 
      Omega is solved by setting the torque of the motor equal to the torque of the prop
      It assumes that the Cp is constant 

    Source:
        None

    Args:
    conditions.freestream.density  (numpy.ndarray): density [kg/m^3] 
    motor.
        gear_ratio                                 (float): gear ratio                [unitless]
        speed_constant                             (float): motor speed constant      [radian/s/V]
        resistance                                 (float): motor internal resistnace [ohm]
        outputs.omega                      (numpy.ndarray): angular velocity          [radian/s]
        gearbox_efficiency                         (float): gearbox efficiency        [unitless]
        expected_current                           (float): current                   [A]
        no_load_current                            (float): no-load current           [A]
        inputs.volage                      (numpy.ndarray): operating voltage         [V]
        inputs.rotor_power_coefficient     (numpy.ndarray): power coefficient         [unitless]
        rotor_radius                               (float): rotor radius              [m]
           
    Returns:
        None
    """           
    # Unpack 
    rho   = conditions.freestream.density[:,0,None]
    Res   = motor.resistance
    eta_G = motor.gearbox_efficiency
    exp_I = motor.expected_current
    I0    = motor.no_load_current + exp_I*(1-eta_G)
    G     = motor.gear_ratio
    KV    = motor.speed_constant/G
    R     = motor.rotor_radius
    v     = motor_conditions.voltage
    Cp    = motor_conditions.rotor_power_coefficient 

    # compute angular velocity, omega 
    omega   =   ((np.pi**(3./2.))*((- 16.*Cp*I0*rho*(KV*KV*KV)*(R*R*R*R*R)*(Res*Res) +
                16.*Cp*rho*v*(KV*KV*KV)*(R*R*R*R*R)*Res + (np.pi*np.pi*np.pi))**(0.5) - 
                np.pi**(3./2.)))/(8.*Cp*(KV*KV)*(R*R*R*R*R)*Res*rho)
    omega [np.isnan(omega )] = 0.0
    
    # compute torque 
    Q = ((v-omega /KV)/Res -I0)/KV 
    
    # store values 
    motor_conditions.torque  = Q
    motor_conditions.omega   = omega 

    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_I_from_omega_and_V
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_current_from_RPM_and_voltage(motor, motor_conditions,conditions):
    """Calculates the motor's current from its RPM and voltage. 
    The following perperties of the motor are computed   
    motor_conditions.current     (numpy.ndarray): current      [A]
    motor_conditions.efficiency  (numpy.ndarray): efficiency   [unitless] 
      
    Assumptions:
        None
        
    Source:
        None

    Args: 
        gear_ratio                  (float): gear ratio                [unitless]
        speed_constant              (float): motor speed constant      [radian/s/V]
        resistance                  (float): motor internal resistnace [ohm]
        outputs.omega       (numpy.ndarray): angular velocity          [radian/s]
        gearbox_efficiency          (float): gearbox efficiency        [unitless]
        expected_current            (float): current                   [A]
        no_load_current             (float): no-load current           [A]
        inputs.volage       (numpy.ndarray): operating voltage         [V] 
        rotor_radius                (float): rotor radius              [m]

    Returns:
        None 
    """                      
    
    # Unpack
    KV    = motor.speed_constant
    Res   = motor.resistance
    omega = motor_conditions.omega
    V     = motor_conditions.voltage
    G     = motor.gear_ratio
    eta_G = motor.gearbox_efficiency
    exp_I = motor.expected_current
    I0    = motor.no_load_current + exp_I*(1-eta_G)
    
    # compute current 
    I    = (V-(omega*G)/KV)/Res 

    # Pack results 
    motor_conditions.current    = I
    motor_conditions.efficiency = (1-I0/I)*(1-I*Res/V)
    return