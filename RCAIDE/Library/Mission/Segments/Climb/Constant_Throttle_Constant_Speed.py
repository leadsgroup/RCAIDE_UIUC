# RCAIDE/Library/Mission/Segments/Climb/Constant_Throttle_Constant_Speed.py
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
def unpack_body_angle(segment):
    """
    Unpacks and sets the proper value for body angle

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function handles the initialization of the body angle for a climb segment
    with constant throttle and constant speed.

    **Required Segment Components**

    segment:
        state:
            unknowns:
                body_angle : array
                    Aircraft body angle [rad]
            conditions:
                frames:
                    body:
                        transform_to_inertial : array
                            Rotation matrix from body to inertial frame

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.body.transform_to_inertial
    """
    
    ctrls    = segment.assigned_control_variables 

    # Body Angle Control    
    if ctrls.body_angle.active: 
        segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0] 
    else:
        segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.angle_of_attack            

    if ctrls.bank_angle.active: 
        segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.state.unknowns.bank_angle[:,0]
    else:
        segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.bank_angle
            
    segment.state.conditions.frames.body.inertial_rotations[:,2] =  segment.state.conditions.frames.planet.true_heading[:,0]     
         
# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------

def initialize_conditions(segment):
    """
    Initializes conditions for constant throttle climb with fixed speed

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function sets up the initial conditions for a climb segment with constant
    throttle setting and constant airspeed.

    **Required Segment Components**

    segment:
        - air_speed : float
            True airspeed to maintain [m/s]
        - throttle : float
            Throttle setting to maintain [-]
        - altitude_start : float
            Initial altitude [m]
        - altitude_end : float
            Final altitude [m]
        - sideslip_angle : float
            Aircraft sideslip angle [rad]
        - state:
            numerics.dimensionless.control_points : array
                Discretization points [-]
            conditions : Data
                State conditions container

    **Calculation Process**
    1. Set initial conditions
    2. Decompose velocity into components using:
        - Wind angle (to be solved)
        - Body angle (to be solved)
        - Sideslip angle
        - Constant speed requirement

    **Major Assumptions**
    * Constant throttle setting
    * Constant true airspeed
    * Small angle approximations
    * Quasi-steady flight

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
    
    # unpack 
    alt0       = segment.altitude_start 
    v_mag      = segment.air_speed 
    beta       = segment.sideslip_angle
    alpha      = segment.state.unknowns.wind_angle[:,0][:,None]
    theta      = segment.state.unknowns.body_angle[:,0][:,None]
    conditions = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
   
    # Flight path angle
    gamma = theta-alpha

    # process
    v_x =   np.cos(beta) *v_mag * np.cos(gamma)
    v_y =   np.sin(beta) *v_mag * np.cos(gamma)
    v_z = -v_mag * np.sin(gamma) # z points down

    # pack
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = v_z[:,0]
 

def update_differentials_altitude(segment):
    """
    Updates time derivatives and integration for altitude-based discretization

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function handles the time integration for segments discretized in altitude
    for constant throttle, constant speed climbs. It scales the differentiation and 
    integration operators based on the vertical velocity profile.

    **Required Segment Components**

    segment:
        state:
            numerics:
                dimensionless:
                    - control_points : array
                        Discretization points [-]
                    - differentiate : array
                        Differentiation operator
                    - integrate : array
                        Integration operator
            conditions:
                frames.inertial:
                    - position_vector : array
                        Position vector [m]
                    - velocity_vector : array
                        Velocity vector [m/s]
                    - time : array
                        Time vector [s]
        - altitude_start : float
            Initial altitude [m]
        - altitude_end : float
            Final altitude [m]

    **Process Flow**
    1. Calculate time step from altitude change and vertical velocity
    2. Scale operators by time step
    3. Integrate altitude profile
    4. Update time vector

    **Major Assumptions**
    * Vertical velocity is well-behaved
    * Altitude change is monotonic
    * Time step is positive

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.time [s]
        - conditions.frames.inertial.position_vector [m]
        - conditions.freestream.altitude [m]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    
    # unpack
    t = segment.state.numerics.dimensionless.control_points
    I = segment.state.numerics.dimensionless.integrate
    
    # Unpack segment initials
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end    
    conditions = segment.state.conditions  
    v          = segment.state.conditions.frames.inertial.velocity_vector
    
    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]    
    
    # get overall time step
    vz = -v[:,2,None] # Inertial velocity is z down
    dz = altf- alt0    
    dt = dz / np.dot(I[-1,:],vz)[-1] # maintain column array
    
    # Integrate vz to get altitudes
    alt = alt0 + np.dot(I*dt,vz)

    # rescale operators
    t = t * dt

    # pack
    t_initial = segment.state.conditions.frames.inertial.time[0,0]
    segment.state.conditions.frames.inertial.time[:,0] = t_initial + t[:,0]
    conditions.frames.inertial.position_vector[:,2]    = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]                =  alt[:,0] # positive altitude in this context    

    return

# ----------------------------------------------------------------------
#  Update Velocity Vector from Wind Angle
# ----------------------------------------------------------------------

def update_velocity_vector_from_wind_angle(segment):
    """
    Updates velocity vector based on wind angle solution

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function updates the velocity vector components based on the solved
    wind angle and body angle values.

    **Required Segment Components**

    segment:
        - air_speed : float
            True airspeed [m/s]
        - sideslip_angle : float
            Aircraft sideslip angle [rad]
        state:
            unknowns:
                wind_angle : array
                    Angle between velocity vector and horizon [rad]
                body_angle : array
                    Aircraft body angle [rad]

    **Calculation Process**
    1. Calculate flight path angle from body and wind angles
    2. Decompose velocity into components using:
        - Flight path angle
        - Sideslip angle
        - Constant speed requirement

    Returns
    -------
    conditions : Data
        Updated segment conditions with new velocity vector
    """
    
    # unpack
    conditions = segment.state.conditions 
    v_mag      = segment.air_speed 
    beta       = segment.sideslip_angle
    alpha      = segment.state.unknowns.wind_angle[:,0][:,None]
    theta      = segment.state.unknowns.body_angle[:,0][:,None]
    
    # Flight path angle
    gamma = theta-alpha

    # process
    v_x =   np.cos(beta) *v_mag * np.cos(gamma)
    v_y =   np.sin(beta) *v_mag * np.cos(gamma)
    v_z = -v_mag * np.sin(gamma) # z points down

    # pack
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = v_z[:,0]

    return conditions
