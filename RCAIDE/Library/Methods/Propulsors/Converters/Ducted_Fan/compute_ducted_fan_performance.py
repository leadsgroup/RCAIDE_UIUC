# RCAIDE/Library/Methods/Propulsors/Converters/Rotor/compute_ducted_fan_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports
import  RCAIDE 
from RCAIDE.Framework.Core                              import Data , Units, orientation_product, orientation_transpose  

# package imports
import  numpy as  np 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Generalized Rotor Class
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_ducted_fan_performance(propulsor,state,center_of_gravity= [[0.0, 0.0,0.0]]):
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
    propulsor_conditions  = conditions.energy[propulsor.tag]
    commanded_TV          = propulsor_conditions.commanded_thrust_vector_angle
    ducted_fan_conditions = propulsor_conditions[ducted_fan.tag]
    
    if ducted_fan.fidelity == 'Blade_Element_Momentum_Theory': 
                      
        altitude  = conditions.freestream.altitude / 1000
        a         = conditions.freestream.speed_of_sound
        
        omega = ducted_fan_conditions.omega 
        n     = omega/(2.*np.pi)   # Rotations per second
        D     = ducted_fan.tip_radius * 2
        A     = 0.25 * np.pi * (D ** 2)
        
        # Unpack freestream conditions
        rho     = conditions.freestream.density[:,0,None] 
        Vv      = conditions.frames.inertial.velocity_vector 
    
        # Number of radial stations and segment control point
        B        = ducted_fan.number_of_rotor_blades
        Nr       = ducted_fan.number_of_radial_stations
        ctrl_pts = len(Vv)
         
        # Velocity in the rotor frame
        T_body2inertial         = conditions.frames.body.transform_to_inertial
        T_inertial2body         = orientation_transpose(T_body2inertial)
        V_body                  = orientation_product(T_inertial2body,Vv)
        body2thrust,orientation = ducted_fan.body_to_prop_vel(commanded_TV) 
        T_body2thrust           = orientation_transpose(np.ones_like(T_body2inertial[:])*body2thrust)
        V_thrust                = orientation_product(T_body2thrust,V_body)
    
        # Check and correct for hover
        V         = V_thrust[:,0,None]
        V[V==0.0] = 1E-6
         
        tip_mach = (omega * ducted_fan.tip_radius) / a
        mach     =  V/ a
        # create tuple for querying surrogate 
        pts      = (mach,tip_mach,altitude) 
        
        thrust         = ducted_fan.performance_surrogates.thrust(pts)            
        power          = ducted_fan.performance_surrogates.power(pts)                 
        efficiency     = ducted_fan.performance_surrogates.efficiency(pts)            
        torque         = ducted_fan.performance_surrogates.torque(pts)                
        Ct             = ducted_fan.performance_surrogates.thrust_coefficient(pts)    
        Cp             = ducted_fan.performance_surrogates.power_coefficient(pts) 
        Cq             = torque/(rho*(n*n)*(D*D*D*D*D))
        FoM            = thrust*np.sqrt(thrust/(2*rho*A))/power  
        
        # calculate coefficients    
        thrust_prop_frame      = np.zeros((ctrl_pts,3))
        thrust_prop_frame[:,0] = thrust[:,0]
        thrust_vector          = orientation_product(orientation_transpose(T_body2thrust),thrust_prop_frame)
     
        # Compute moment 
        moment_vector           = np.zeros((ctrl_pts,3))
        moment_vector[:,0]      = ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
        moment_vector[:,1]      = ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
        moment_vector[:,2]      = ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
        moment                  =  np.cross(moment_vector, thrust_vector)
        

        outputs                                   = Data(
                torque                            = torque,
                thrust                            = thrust_vector,  
                power                             = power,
                moment                            = moment, 
                rpm                               = omega /Units.rpm ,   
                tip_mach                          = tip_mach, 
                efficiency                        = efficiency,         
                number_radial_stations            = Nr, 
                orientation                       = orientation, 
                speed_of_sound                    = conditions.freestream.speed_of_sound,
                density                           = conditions.freestream.density,
                velocity                          = Vv,     
                omega                             = omega,  
                thrust_per_blade                  = thrust/B,
                thrust_coefficient                = Ct, 
                torque_per_blade                  = torque/B,
                figure_of_merit                   = FoM, 
                torque_coefficient                = Cq,
                power_coefficient                 = Cp)
        
    elif ducted_fan.fidelity == 'Rankine_Froude_Momentum_Theory': 
    
        # Unpack ducted_fan blade parameters and operating conditions  
        K_fan          = ducted_fan.fan_effectiveness
        A_exit         = np.pi*ducted_fan.tip_radius**2
        A_R            = np.pi*(ducted_fan.tip_radius**2 - ducted_fan.hub_radius**2)
        epsilon_d      = A_exit/A_R
        a              = conditions.freestream.speed_of_sound 
        rho            = conditions.freestream.density 
        u0             = conditions.freestream.velocity 
        propeller_type = 'fixed_pitch' 
        eta_p          = compute_ducted_fan_efficiency(ducted_fan, propeller_type, u0)
        
        # Compute power 
        P_EM        = propulsor.motor.design_torque*propulsor.motor.angular_velocity 
        P_req       = P_EM*eta_p/K_fan
    
        # Coefficients of the cubic equation
        a = 1 / (4 * rho * A_R * epsilon_d)
        b = -(1/2)*((u0) ** 2)
        c = +(3/2)*(u0)*P_req
        d = -P_req**2
    
        # Use numpy.roots to solve the cubic equation
        coefficients = [float(a[0]), float(b[0]), float(c[0]), d]
        roots = np.roots(coefficients)
    
        # Filter out the physical root (real, non-negative values)
        T = [root.real for root in roots if np.isreal(root) and root.real >= 0][-1]
    
        thrust_vector  = np.array([[T, 0.0, 0.0]] * len(rho))   
        power          = P_EM * np.ones_like(rho)              
        torque         = propulsor.motor.design_torque*np.ones_like(rho)
        
        # Compute moment 
        moment_vector         = np.zeros((3))
        moment_vector[0]      = ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
        moment_vector[1]      = ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
        moment_vector[2]      = ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
        moment                = moment_vector
           
        outputs                                   = Data( 
                thrust                            = thrust_vector,  
                power                             = power,
                moment                            = moment, 
                torque                            = torque)
        
    conditions.energy[propulsor.tag][ducted_fan.tag] = outputs   
    
    return  

def compute_ducted_fan_efficiency(ducted_fan, V, R, omega):
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
      
    # 
    
    
    a =  ducted_fan.actuator_disc_efficiency_coefficients[0]  
    b =  ducted_fan.actuator_disc_efficiency_coefficients[1]  
    c =  ducted_fan.actuator_disc_efficiency_coefficients[2]  
     
    # create polynominal
    
    # compute propulsive efficiency 
    
    
    #if propeller_type == 'constant_speed': 
        #eta_p_y   = 0.8
        #eta_p_opt = 0.88
        #eta_p_hs  = 0.8
        #V_hs      = V_c + 100 * Units.knots
    #elif propeller_type == 'fixed_pitch':
        #eta_p_y   = 0.7
        #eta_p_opt = 0.8
        #eta_p_hs  = 0.7
        #V_hs      = V_c + 50 * Units.knots
    #else:
        #raise ValueError(f"Unknown propeller type: {propeller_type}")

    ## Construct the matrix
    #matrix = np.array([
        #[V_y, V_y**2, V_y**3, V_y**4],
        #[V_c, V_c**2, V_c**3, V_c**4],
        #[1, 2*V_c, 3*V_c**2, 4*V_c**3],
        #[V_hs, V_hs**2, V_hs**3, V_hs**4]
    #])
 
    return eta_p
