# RCAIDE/Library/Methods/Powertrain/Converters/Rotor/Performance/Actuator_Disc_Theory/Actuator_Disk_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core                              import Data  

# package imports
import  numpy as  np  

# ---------------------------------------------------------------------------------------------------------------------- 
# Actuator_Disk_performance
# ----------------------------------------------------------------------------------------------------------------------  
def Actuator_Disk_performance(rotor, conditions, propulsor, center_of_gravity):

    propulsor_conditions  = conditions.energy[propulsor.tag]
    rotor_conditions      = propulsor_conditions[rotor.tag]
    commanded_TV          = propulsor_conditions.commanded_thrust_vector_angle
    eta                   = rotor_conditions.throttle 
    omega                 = rotor_conditions.omega
    a                     = conditions.freestream.speed_of_sound 
    rho                   = conditions.freestream.density 
    alt                   = conditions.freestream.altitude  
    
    # Unpack ducted_fan blade parameters and operating conditions  
    V                     = conditions.freestream.velocity  
    n, D, J, eta_p, Cp, Ct        = compute_propeller_efficiency(rotor, V, omega)
    ctrl_pts              = len(V)

    thrust                = Ct*(rho * (n**2)*(D**4))                 
    power                 = Cp*(rho * (n**3)*(D**5) ) 
    torque                = power/omega
    # power                 = torque*omega
    # thrust                = eta_p*power/V   
    # Cp                    = power/(rho * (n**3)*(D**5) ) 
    # Ct                    = thrust/(rho * (n**2)*(D**4)) 
    thrust_vector         = np.zeros((ctrl_pts,3))
    thrust_vector[:,0]    = thrust[:,0]           
     
    # Compute moment 
    moment_vector         = np.zeros((ctrl_pts,3))
    moment_vector[:,0]    = rotor.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]    = rotor.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]    = rotor.origin[0][2]  -  center_of_gravity[0][2]
    moment                = np.cross(moment_vector, thrust_vector)
       
    outputs                                   = Data( 
            thrust                            = thrust_vector,  
            power                             = power,
            power_coefficient                 = Cp, 
            thrust_coefficient                = Ct,
            efficiency                        = eta_p, 
            moment                            = moment, 
            torque                            = torque)

    return outputs 