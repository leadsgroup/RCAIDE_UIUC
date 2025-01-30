# RCAIDE/Library/Methods/Propulsors/Converters/Ducted_Fan/compute_low_fidelity_ducted_fan_performance.py
# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core                              import Data 

# package imports
import  numpy as  np 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Generalized Rotor Class
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_low_fidelity_ducted_fan_performance(propulsor,state,center_of_gravity= [[0.0, 0.0,0.0]]):
    """Analyzes a general ducted_fan given geometry and operating conditions.

    Assumptions:
    N.A.

    Source:
    N.A.
    
    Inputs:
        propulsor          (dict): propulsor data structure 
        state              (dict): flight conditions data structure  
        center_of_gravity  (list): center of gravity  

    Outputs:
        None
    """

    # Unpack ducted_fan blade parameters and operating conditions 
    conditions            = state.conditions
    ducted_fan            = propulsor.ducted_fan
    eta_p                 = ducted_fan.eta_p
    K_fan                 = ducted_fan.K_fan
    epsilon_d             = ducted_fan.epsilon_d
    A_R                   = ducted_fan.A_R
    a         = conditions.freestream.speed_of_sound
    
    # Unpack freestream conditions
    rho     = conditions.freestream.density[:,0,None] 
    u0      = conditions.freestream.airspeed[:,0,None]

    # Compute power 
    P_EM                       = propulsor.motor.design_torque*propulsor.motor.angular_velocity

    P_req                      = P_EM*eta_p/K_fan

    # Coefficients of the cubic equation
    a = float(1 / (4 * rho * A_R * epsilon_d))
    b =  float(-(1/2)*((u0) ** 2))
    c =  float(+(3/2)*(u0)*P_req)
    d = -P_req**2

    # Use numpy.roots to solve the cubic equation
    coefficients = [a, b, c, d]
    roots = np.roots(coefficients)

    # Filter out the physical root (real, non-negative values)
    T = [root.real for root in roots if np.isreal(root) and root.real >= 0]

    thrust         = T       
    power          = P_EM              
 
    # Compute moment 
    moment_vector         = np.zeros((3))
    moment_vector[0]      = ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[1]      = ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[2]      = ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
    moment                = moment_vector
     
    outputs                                       = Data( 
                thrust                            = thrust,  
                power                             = power,
                moment                            = moment
        ) 
    
    conditions.energy[propulsor.tag][ducted_fan.tag] = outputs   
    
    return  
