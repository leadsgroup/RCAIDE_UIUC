# RCAIDE/Library/Mission/Segments/Single_Point/Set_Speed_Set_Throttle.py
# 
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------   
def initialize_conditions(segment):
    """
    Initializes conditions for fixed speed and throttle analysis

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function sets up the initial conditions for a single point analysis with
    fixed speed and throttle setting. The x-acceleration is treated as an unknown
    to be solved for during the analysis.

    **Required Segment Components**

    segment:
        - altitude : float
            Flight altitude [m]
        - air_speed : float
            True airspeed [m/s]
        - sideslip_angle : float
            Aircraft sideslip angle [rad]
        - linear_acceleration_z : float
            Acceleration in z-direction [m/s^2]
        - roll_rate : float
            Aircraft roll rate [rad/s]
        - pitch_rate : float
            Aircraft pitch rate [rad/s]
        - yaw_rate : float
            Aircraft yaw rate [rad/s]
        - state:
            unknowns:
                acceleration : array
                    X-direction acceleration [m/s^2]
            conditions : Data
                State conditions container
            initials : Data, optional
                Initial conditions from previous segment

    **Calculation Process**
    1. Check initial conditions
    2. Decompose velocity into components using sideslip angle:
       - v_x = V * cos(β)
       - v_y = V * sin(β)
       where:
       - V is true airspeed
       - β is sideslip angle
    3. Set position and altitude
    4. Initialize acceleration vector with unknown x-component
    5. Set angular rates

    **Major Assumptions**
    * Fixed throttle setting
    * Constant airspeed
    * Small angle approximations
    * Quasi-steady state
    * No lateral acceleration

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.freestream.altitude [m]
        - conditions.frames.inertial.position_vector [m]
        - conditions.frames.inertial.velocity_vector [m/s]
        - conditions.frames.inertial.acceleration_vector [m/s^2]
        - conditions.static_stability.roll_rate [rad/s]
        - conditions.static_stability.pitch_rate [rad/s]
        - conditions.static_stability.yaw_rate [rad/s]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """      
    
    # unpack
    alt                     = segment.altitude
    air_speed               = segment.air_speed
    beta                    = segment.sideslip_angle  
    linear_acceleration_z   = segment.linear_acceleration_z
    roll_rate               = segment.roll_rate
    pitch_rate              = segment.pitch_rate
    yaw_rate                = segment.yaw_rate
    acceleration            = segment.state.unknowns.acceleration[0][0]
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
    
    v_x  = np.cos(beta)*air_speed 
    v_y  = np.sin(beta)*air_speed
        
    # pack
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = v_x 
    segment.state.conditions.frames.inertial.velocity_vector[:,1] = v_y 
    segment.state.conditions.frames.inertial.acceleration_vector  = np.array([[acceleration,0.0,linear_acceleration_z]])  
    segment.state.conditions.static_stability.roll_rate[:,0]      = roll_rate         
    segment.state.conditions.static_stability.pitch_rate[:,0]     = pitch_rate
    segment.state.conditions.static_stability.yaw_rate[:,0]       = yaw_rate      

    
# ----------------------------------------------------------------------------------------------------------------------  
#  Unpack Unknowns 
# ----------------------------------------------------------------------------------------------------------------------  
def unpack_unknowns(segment):
    """
    Updates the x-acceleration from solver results

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function takes the solved x-acceleration value and updates the
    acceleration vector in the segment conditions.

    **Required Segment Components**

    segment:
        state:
            unknowns:
                acceleration : array
                    Solved x-acceleration value [m/s^2]
            conditions:
                frames:
                    inertial:
                        acceleration_vector : array
                            Full acceleration vector [m/s^2]

    Returns
    -------
    None
        Updates acceleration vector in segment conditions directly
    """      
    
    # unpack unknowns  
    acceleration  = segment.state.unknowns.acceleration 
    segment.state.conditions.frames.inertial.acceleration_vector[0,0] = acceleration         