# RCAIDE/Library/Mission/Common/Update/moments.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core  import  orientation_product  

# ----------------------------------------------------------------------------------------------------------------------
#  Update Moments
# ----------------------------------------------------------------------------------------------------------------------
def moments(segment):
    """
    Updates total resultant moments on the vehicle

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function transforms and sums all moment vectors (aerodynamic and thrust)
    into the inertial frame to get the total moment on the vehicle.

    **Required Segment Components**

    segment.state.conditions:
        frames:
            wind:
                - moment_vector : array
                    Aerodynamic moments [N·m]
                - transform_to_inertial : array
                    Wind to inertial transform matrix
            body:
                - thrust_moment_vector : array
                    Propulsive moments [N·m]
                - transform_to_inertial : array
                    Body to inertial transform matrix

    **Major Assumptions**
    * Valid coordinate transformations
    * Proper moment definitions
    * Compatible reference frames
    * Rigid body dynamics

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.total_moment_vector [N·m]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    RCAIDE.Framework.Core
    """

    # unpack
    conditions                = segment.state.conditions  
    wind_moment_vector        = conditions.frames.wind.moment_vector
    body_thrust_moment_vector = conditions.frames.body.thrust_moment_vector
    
    # unpack transformation matrices
    T_wind2inertial = conditions.frames.wind.transform_to_inertial 
    T_body2inertial = conditions.frames.body.transform_to_inertial 

    # to inertial frame 
    M_t = orientation_product(T_body2inertial,body_thrust_moment_vector) 
    M_w = orientation_product(T_wind2inertial, wind_moment_vector) 
    
    M = M_t + M_w
    
    # pack
    conditions.frames.inertial.total_moment_vector[:,:] = M[:,:]

    return
