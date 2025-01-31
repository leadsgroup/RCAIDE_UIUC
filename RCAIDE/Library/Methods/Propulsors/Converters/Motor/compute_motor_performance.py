# RCAIDE/Library/Methods/Propulsors/Converters/Motor/compute_motor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import  RCAIDE

# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_omega_and_Q_from_Cp_and_V
# ----------------------------------------------------------------------------------------------------------------------    
def compute_motor_performance(motor,motor_conditions,conditions):
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

    if (type(motor) == RCAIDE.Library.Components.Propulsors.Converters.PMSM_Motor): 
        I = motor_conditions.current
        V = motor_conditions.voltage
        I_turn         = I/motor.number_of_turns                                                         # [A]            current in each turn
        omega          = motor.speed_constant*(V - I*Res)* (2 * np.pi / 60)                # [RPM -> rad/s] rotor angular velocity
        A              = np.pi * ((motor.stator_outer_diameter**2 - motor.stator_inner_diameter**2) / 4)                    # [m**2]         cross-sectional area of the reluctance path perpendicular to length 𝑙    
        MMF_coil       = motor.number_of_turns*I_turn                                                    # [A*turns]      magnetomotive force applied to the reluctance path for a coil (Eq.14)  
        R              = motor.length_of_path/(A*motor.mu_0*motor.mu_r)                                 # [A*turn/Wb]    reluctance of a given path or given reluctant element (Eq.16) 
        phi            = MMF_coil/R                                                        # [Wb]           magnetic flux through the reluctance path (Eq.12)
        B_sign         = phi/A                                                             # [V*s/m**2]     ranges from 0.5 to 1.2, average magnitude of the radial flux density produced by the rotor
        A_sign         = (motor.winding_factor*I)/(np.pi*motor.stator_inner_diameter)                                  # [-]            stator electrical loading (Eq.2)        
        TQ             = (np.pi/2)*(B_sign*A_sign)*(motor.stator_inner_diameter**2)*motor.motor_stack_length                 # [Nm]           torque (Eq.1)
        P              = omega*TQ/1000                                                     # [kW]           power (Eq.1)  
        motor_conditions.torque  = TQ
        motor_conditions.omega   = omega 
        motor_conditions.power   = P   
    else:
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
        I    = (v-(omega*G)/KV)/Res 
         
        motor_conditions.torque  = Q
        motor_conditions.omega   = omega  
        motor_conditions.current    = I
        motor_conditions.efficiency = (1-I0/I)*(1-I*Res/v) 
     
    return