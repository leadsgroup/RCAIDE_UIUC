# RCAIDE/Library/Methods/Powertrain/Converters/Rotor/Performance/Actuator_Disc_Theory/Actuator_Disk_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core  import Data   

# package imports
import  numpy as  np  
from scipy.interpolate import interp1d

# ---------------------------------------------------------------------------------------------------------------------- 
# Actuator_Disk_performance
# ----------------------------------------------------------------------------------------------------------------------  
def Actuator_Disk_performance(rotor, conditions, propulsor, center_of_gravity):
    '''
    
    MATTEO
    
    '''

    propulsor_conditions  = conditions.energy[propulsor.tag]
    rotor_conditions      = propulsor_conditions[rotor.tag] 
    omega                 = rotor_conditions.omega 
    rho                   = conditions.freestream.density  
    
    # Unpack ducted_fan blade parameters and operating conditions  
    V                     = conditions.freestream.velocity  
    n,D,J,eta_p,Cp,Ct     = compute_rotor_efficiency(rotor, V, omega)
    ctrl_pts              = len(V)

    thrust                = Ct*(rho * (n**2)*(D**4))                 
    power                 = Cp*(rho * (n**3)*(D**5) ) 
    torque                = power/omega
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

# ---------------------------------------------------------------------------------------------------------------------- 
#  compute_rotor_efficiency
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_rotor_efficiency(propeller, V, omega):
    """
    Calculate propeller efficiency based on propeller type and velocity.
    
    Parameters
    ----------
    propeller_type : str
        Type of propeller ('constant_speed' or 'fixed_pitch')
    u0 : float
        Current velocity
        
    Returns
    -------
    float
        Calculated propeller efficiency
    """

    n = omega/(2*np.pi)
    D = 2*propeller.tip_radius
    J = V/(n*D)

    eta_J_vector = propeller.etap_J_coefficients
    eta_vector = propeller.etap_eff_coefficients

    eta_fz = interp1d(eta_J_vector, eta_vector, kind='cubic', fill_value=0.0, bounds_error=False)
    eta_p = eta_fz(J)

    Cp_J_vector = propeller.Cp_J_coefficients
    Cp_vector = propeller.Cp_power_coefficients

    Cp_fz = interp1d(Cp_J_vector, Cp_vector, kind='cubic', fill_value=0.0, bounds_error=False)
    Cp = Cp_fz(J)

    Ct_J_vector = propeller.Ct_J_coefficients
    Ct_vector = propeller.Ct_thrust_coefficients

    Ct_fz = interp1d(Ct_J_vector, Ct_vector, kind='cubic', fill_value=0.0, bounds_error=False)
    Ct = Ct_fz(J)

    return n, D, J, eta_p, Cp, Ct
