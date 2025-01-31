# RCAIDE/Library/Methods/Propulsors/Converters/PMSM_Motor/compute_PMSM_motor_performance.py

# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_PMSM_motor_performance
# ----------------------------------------------------------------------------------------------------------------------    
def compute_RPM_and_torque(motor,motor_conditions,conditions):
    I = motor_conditions.current
    V = motor_conditions.voltage
    I_turn         = I/motor.N                                               # [A]            current in each turn
    omega          = motor.speed_constant*(V - I*motor.R)* (2 * np.pi / 60)        # [RPM -> rad/s] rotor angular velocity
    A              = np.pi * ((motor.D_out**2 - motor.D_in**2) / 4)                    # [m**2]         cross-sectional area of the reluctance path perpendicular to length 𝑙    
    MMF_coil       = motor.N*I_turn                                                    # [A*turns]      magnetomotive force applied to the reluctance path for a coil (Eq.14)  
    R              = motor.l/(A*motor.mu_0*motor.mu_r)                                 # [A*turn/Wb]    reluctance of a given path or given reluctant element (Eq.16) 
    phi            = MMF_coil/R                                                        # [Wb]           magnetic flux through the reluctance path (Eq.12)
    B_sign         = phi/A                                                             # [V*s/m**2]     ranges from 0.5 to 1.2, average magnitude of the radial flux density produced by the rotor
    A_sign         = (motor.k_w*I)/(np.pi*motor.D_in)                        # [-]            stator electrical loading (Eq.2)        
    TQ             = (np.pi/2)*(B_sign*A_sign)*(motor.D_in**2)*motor.L                 # [Nm]           torque (Eq.1)
    P              = omega*TQ/1000                                                     # [kW]           power (Eq.1)  
    motor_conditions.torque  = TQ
    motor_conditions.omega   = omega 
    motor_conditions.power   = P
    return 
