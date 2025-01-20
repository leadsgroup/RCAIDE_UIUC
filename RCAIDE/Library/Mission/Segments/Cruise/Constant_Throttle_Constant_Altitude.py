# RCAIDE/Library/Mission/Segments/Cruise/Constant_Throttle_Constant_Altitude.py
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
def unpack_unknowns(segment):
    """
    Unpacks and processes unknown variables for constant throttle cruise

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function handles the unpacking and processing of unknown variables that
    are solved during the segment analysis.

    **Required Segment Components**

    segment:
        state:
            unknowns:
                acceleration : array
                    Acceleration in x-direction [m/s^2]
                elapsed_time : array
                    Time duration [s]
            numerics:
                dimensionless:
                    control_points : array
                        Discretization points [-]
            conditions:
                frames:
                    inertial:
                        acceleration_vector : array
                            Acceleration vector [m/s^2]
                        time : array
                            Time vector [s]

    **Calculation Process**
    1. Extract acceleration and time from unknowns
    2. Scale time points between initial and final values
    3. Build acceleration vector with x-component

    Returns
    -------
    None
        Updates segment conditions directly
    """
    
    # unpack unknowns
    unknowns   = segment.state.unknowns 
    accel_x    = unknowns.acceleration 
    time       = unknowns.elapsed_time
     
    # rescale time
    t_initial  = segment.state.conditions.frames.inertial.time[0,0]
    t_final    = t_initial + time  
    t_nondim   = segment.state.numerics.dimensionless.control_points
    time       = t_nondim * (t_final-t_initial) + t_initial     

    # build acceleration
    N          = segment.state.numerics.number_of_control_points
    a          = np.zeros((N, 3))
    a[:, 0]    = accel_x[:,0]
    
    # apply unknowns
    conditions = segment.state.conditions 
    conditions.frames.inertial.acceleration_vector  = a
    conditions.frames.inertial.time[:,0]            = time[:,0]
    
    return 

# ----------------------------------------------------------------------
#  Integrate Velocity
# ---------------------------------------------------------------------- 

def integrate_velocity(segment):
    """
    Integrates acceleration to get velocity profile

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function integrates the acceleration to obtain the velocity profile,
    considering the initial velocity and sideslip angle.

    **Required Segment Components**

    segment:
        - air_speed_start : float
            Initial true airspeed [m/s]
        - sideslip_angle : float
            Aircraft sideslip angle [rad]
        state:
            numerics:
                time:
                    integrate : array
                        Integration operator
            conditions:
                frames:
                    inertial:
                        acceleration_vector : array
                            Acceleration vector [m/s^2]
                        velocity_vector : array
                            Velocity vector [m/s]

    **Calculation Process**
    1. Integrate acceleration to get velocity magnitude
    2. Decompose into components using sideslip angle

    Returns
    -------
    None
        Updates velocity vector in segment conditions
    """
    
    # unpack 
    conditions = segment.state.conditions
    v0         = segment.air_speed_start 
    beta       = segment.sideslip_angle
    I          = segment.state.numerics.time.integrate
    a          = conditions.frames.inertial.acceleration_vector
    
    # compute x-velocity
    velocity_xy = v0 + np.dot(I, a)[:,0]   
    v_x         = np.cos(beta)*velocity_xy
    v_y         = np.sin(beta)*velocity_xy

    # pack velocity
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    
    return

# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------    

def initialize_conditions(segment):
    """
    Initializes conditions for constant throttle cruise at fixed altitude

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function sets up the initial conditions for a cruise segment with constant
    throttle setting and constant altitude. The segment allows for acceleration
    between initial and final speeds.

    **Required Segment Components**

    segment:
        - altitude : float
            Cruise altitude [m]
        - air_speed_start : float
            Initial true airspeed [m/s]
        - air_speed_end : float
            Final true airspeed [m/s]
        - state:
            numerics:
                number_of_control_points : int
                    Number of discretization points
            conditions : Data
                State conditions container
            initials : Data, optional
                Initial conditions from previous segment

    **Major Assumptions**
    * Constant throttle setting
    * Constant altitude
    * Non-zero velocities required
    * Initial and final speeds must differ

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.freestream.altitude [m]
        - conditions.frames.inertial.position_vector [m]
    """    
    # unpack inputs
    alt      = segment.altitude 
    v0       = segment.air_speed_start
    vf       = segment.air_speed_end    
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]   

    if v0  is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        v0 = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    # avoid having zero velocity since aero and propulsion models need non-zero Reynolds number
    if v0 == 0.0: v0 = 0.01
    if vf == 0.0: vf = 0.01
    
    # intial and final speed cannot be the same
    if v0 == vf:
        vf = vf + 0.01
        
    # repack
    segment.air_speed_start = v0
    segment.air_speed_end   = vf
    
    # pack conditions   
    segment.state.conditions.freestream.altitude[:,0] = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down    
    
# ----------------------------------------------------------------------
#  Solve Residuals
# ----------------------------------------------------------------------    

def solve_velocity(segment):
    """
    Calculates velocity residual for segment convergence

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function computes the residual between the achieved and target final
    velocities to ensure proper segment convergence.

    **Required Segment Components**

    segment:
        - air_speed_end : float
            Target final airspeed [m/s]
        state:
            conditions:
                frames:
                    inertial:
                        velocity_vector : array
                            Current velocity vector [m/s]
            residuals:
                final_velocity_error : float
                    Velocity convergence error [m/s]

    **Calculation Process**
    1. Calculate magnitude of final velocity
    2. Compare with target final velocity
    3. Store residual for solver

    Returns
    -------
    None
        Updates residuals in segment state
    """    

    # unpack inputs
    conditions = segment.state.conditions 
    vf         = segment.air_speed_end
    v          = conditions.frames.inertial.velocity_vector 
    
    segment.state.residuals.final_velocity_error = (np.linalg.norm(v[-1,:])- vf)

    return