# RCAIDE/Library/Missions/Segments/Climb/Constant_Dynamic_Pressure_Constant_Rate.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE 
from RCAIDE.Library.Mission.Common.Update.atmosphere import atmosphere

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant dynamic pressure and constant rate of climb

    Source:
    N/A

    Inputs:
    segment.climb_rate                                  [meters/second]
    segment.dynamic_pressure                            [pascals]
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.state.numerics.dimensionless.control_points [Unitless]
    conditions.freestream.density                       [kilograms/meter^3]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]

    Properties Used:
    N/A
    """        
    
    # unpack
    climb_rate = segment.climb_rate
    q          = segment.dynamic_pressure
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions
    beta       = segment.sideslip_angle
    rho        = conditions.freestream.density[:,0]
    
    # Update freestream to get density
    atmosphere(segment)
    rho = conditions.freestream.density[:,0]   

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    

    # check for initial velocity
    if q is None: 
        if not segment.state.initials: raise AttributeError('dynamic pressure not set')
        v_mag = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
    else: 
        # process velocity vector
        v_mag = np.sqrt(2*q/rho)
    v_z   = -climb_rate # z points down
    v_xy  = np.sqrt( v_mag**2 - v_z**2 )
    v_x   = np.cos(beta)*v_xy 
    v_y   = np.sin(beta)*v_xy 
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context