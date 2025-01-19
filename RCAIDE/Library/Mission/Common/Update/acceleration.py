# RCAIDE/Library/Mission/Common/Update/acceleration.py
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
def acceleration(segment):
    """
    Computes vehicle acceleration by differentiating velocity

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function calculates the acceleration vector by differentiating
    the inertial velocity vector. It assumes planar motion on a flat earth.

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
    """            
    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   