# RCAIDE/Library/Methods/Propulsors/Converters/Rotor/compute_ducted_fan_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core                              import Data , Units, orientation_product, orientation_transpose   

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
    eta_p                 = propulsor.eta_p
    K_fan                 = propulsor.K_fan
    epsilon_d             = propulsor.epsilon_d
    A_R                   = propulsor.A_R
    propulsor_conditions  = conditions.energy[propulsor.tag]
    commanded_TV          = propulsor_conditions.commanded_thrust_vector_angle
    ducted_fan_conditions = propulsor_conditions[ducted_fan.tag]
                  
    altitude  = conditions.freestream.altitude / 1000
    a         = conditions.freestream.speed_of_sound
    
    omega = ducted_fan_conditions.omega 
    n     = omega/(2.*np.pi)   # Rotations per second
    D     = ducted_fan.tip_radius * 2
    A     = 0.25 * np.pi * (D ** 2)
    
    # Unpack freestream conditions
    rho     = conditions.freestream.density[:,0,None] 
    u0      = conditions.freestream.velocity[:,0,None]

    # Compute power 
    P_EM                       = ducted_fan_conditions.power

    P_req                      = P_EM*eta_p/K_fan

    # Coefficients of the cubic equation
    a = 1 / (4 * rho * A_R * epsilon_d)
    b = -(1/2)*((u0) ** 2)
    c = +(3/2)*(u0)*P_req
    d = -P_req**2

    # Use numpy.roots to solve the cubic equation
    coefficients = [a, b, c, d]
    roots = np.roots(coefficients)

    # Filter out the physical root (real, non-negative values)
    T = [root.real for root in roots if np.isreal(root) and root.real >= 0]

    thrust         = T       
    power          = P_EM              
 
    # Compute moment 
    moment_vector           = np.zeros((3))
    moment_vector[:,0]      = ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust) 
     
    outputs                                       = Data( 
                thrust                            = thrust,  
                power                             = power,
                moment                            = moment
        ) 
    
    conditions.energy[propulsor.tag][ducted_fan.tag] = outputs   
    
    return  
