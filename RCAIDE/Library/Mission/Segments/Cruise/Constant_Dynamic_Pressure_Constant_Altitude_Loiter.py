# RCAIDE/Library/Missions/Segments/Cruise/Constant_Dynamic_Pressure_Constant_Altitude_Loiter.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE 
import RCAIDE 

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant dynamic pressure and constant altitude with set loiter time

    Source:
    N/A

    Inputs:
    segment.altitude                [meters]
    segment.time                    [seconds]
    segment.dynamic_pressure        [pascals]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """     
    
    # unpack
    alt        = segment.altitude
    final_time = segment.time
    q          = segment.dynamic_pressure
    beta       = segment.sideslip_angle
    conditions = segment.state.conditions   
    
    # Update freestream to get density 
    RCAIDE.Library.Mission.Common.Update.atmosphere(segment) 
    rho        = conditions.freestream.density[:,0]   
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]       
    
    # check for initial velocity
    if q is None: 
        if not segment.state.initials: raise AttributeError('dynamic pressure not set')
        air_speed = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    else: # compute speed, constant with constant altitude
        air_speed = np.sqrt(q/(rho*0.5))
    
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_final   = final_time + t_initial
    t_nondim  = segment.state.numerics.dimensionless.control_points
    time      = t_nondim * (t_final-t_initial) + t_initial
    v_x       = np.cos(beta)*air_speed 
    v_y       = np.sin(beta)*air_speed 
    
    # pack
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = v_x
    segment.state.conditions.frames.inertial.velocity_vector[:,1] = v_y
    segment.state.conditions.frames.inertial.time[:,0]            = time[:,0]