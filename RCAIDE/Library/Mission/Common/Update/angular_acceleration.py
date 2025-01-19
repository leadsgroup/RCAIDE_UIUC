# RCAIDE/Library/Mission/Common/Update/angular_acceleration.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------   
def angular_acceleration(segment):
    """
    Computes angular acceleration by differentiating angular velocity

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function calculates the angular acceleration vector by differentiating
    the inertial angular velocity vector. Assumes planar motion.

    **Required Segment Components**

    segment.state:
        conditions.frames.inertial:
            - angular_velocity_vector : array
                Vehicle angular velocity [rad/s]
        numerics.time:
            - differentiate : array
                Time differentiation operator

    **Major Assumptions**
    * Flat earth
    * Planar motion
    * Valid angular velocity data
    * Well-defined time discretization

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.angular_acceleration_vector [rad/s²]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """            
    
    # unpack conditions
    omega = segment.state.conditions.frames.inertial.angular_velocity_vector
    D     = segment.state.numerics.time.differentiate
    
    # accelerations
    ang_acc = np.dot(D,omega)
    
    # pack conditions
    segment.state.conditions.frames.inertial.angular_acceleration_vector[:,:] = ang_acc[:,:]   