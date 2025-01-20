# RCAIDE/Library/Mission/Segments/Climb/Constant_Speed_Constant_Angle_Noise.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def expand_state(segment):
    """
    Expands state array for noise certification analysis

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function determines the minimum number of points needed for noise
    certification analysis and expands the state arrays accordingly.

    **Required Segment Components**

    segment:
        state:
            numerics:
                number_of_control_points : int
                    Number of discretization points

    **Major Assumptions**
    * Half-second time intervals required for certification
    * Fixed microphone position at 6500m
    * Continuous noise characteristics

    Returns
    -------
    None
        Updates segment state arrays directly
    """
    
    # unpack
    climb_angle  = segment.climb_angle
    air_speed    = segment.air_speed   
    conditions   = segment.state.conditions
    
    #Necessary input for determination of noise trajectory    
    dt = 0.5  #time step in seconds for noise calculation - Certification requirement    
    x0 = 6500 #Position of the Flyover microphone relatively to the break-release point
    
    # process velocity vector
    v_x=air_speed*np.cos(climb_angle)
    
    #number of time steps (space discretization)
    total_time=(x0+500)/v_x    
    n_points   = np.int(np.ceil(total_time/dt +1))       
    
    segment.state.numerics.number_of_control_points = n_points
    
    segment.state.expand_rows(n_points,override=True)      
    
    return

# ----------------------------------------------------------------------
#  Initialize Conditions
# ---------------------------------------------------------------------- 
def initialize_conditions(segment):
    """
    Initializes conditions for constant speed noise certification climb

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function sets up the initial conditions for a noise certification climb
    segment with constant true airspeed and constant climb angle. Initial altitude
    is fixed at 35ft (10.668m) per certification requirements.

    **Required Segment Components**

    segment:
        - climb_angle : float
            Fixed climb angle [rad]
        - air_speed : float
            True airspeed to maintain [m/s]
        - sideslip_angle : float
            Aircraft sideslip angle [rad]
        - state:
            numerics.dimensionless.control_points : array
                Discretization points [-]
            conditions : Data
                State conditions container

    **Calculation Process**
    1. Set initial altitude (35ft)
    2. Calculate final altitude based on time steps
    3. Decompose constant velocity into components using:
        - Fixed climb angle
        - Sideslip angle
        - Constant speed requirement

    **Major Assumptions**
    * Initial altitude of 35ft (10.668m)
    * Constant true airspeed
    * Fixed climb angle
    * Half-second time steps
    * Small angle approximations

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.velocity_vector [m/s]
        - conditions.frames.inertial.position_vector [m]
        - conditions.freestream.altitude [m]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    
    dt=0.5  #time step in seconds for noise calculation
    
    # unpack
    climb_angle = segment.climb_angle
    air_speed   = segment.air_speed     
    beta        = segment.sideslip_angle
    t_nondim    = segment.state.numerics.dimensionless.control_points
    conditions  = segment.state.conditions  

    # check for initial velocity
    if air_speed is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        air_speed = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    # process velocity vector
    v_mag = air_speed
    v_x   = np.cos(beta)*v_mag * np.cos(climb_angle)
    v_y   = np.sin(beta)*v_mag * np.cos(climb_angle)
    v_z   = -v_mag * np.sin(climb_angle)    

    #initial altitude
    alt0 = 10.668   #(35ft)
    altf = alt0 + (-v_z)*dt*len(t_nondim)

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0    
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context
