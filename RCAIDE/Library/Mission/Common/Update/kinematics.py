# RCAIDE/Library/Mission/Common/Update/kinematics.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------
def kinematics(segment):
    """
    Updates vehicle kinematic states by differentiating position

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function calculates vehicle accelerations by differentiating
    the inertial velocity vector. Similar to acceleration.py but focused
    on full kinematic state updates.

    **Required Segment Components**

    segment.state:
        conditions.frames.inertial:
            - velocity_vector : array
                Vehicle velocity [m/s]
        numerics.time:
            - differentiate : array
                Time differentiation operator

    **Major Assumptions**
    * Flat earth
    * Planar motion
    * Valid velocity data
    * Well-defined time discretization

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.acceleration_vector [m/s²]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    RCAIDE.Library.Mission.Common.Update.acceleration
    """   
    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   