# RCAIDE/Library/Mission/Common/Update/forces.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import  RCAIDE
from RCAIDE.Framework.Core  import  orientation_product
import  numpy as  np 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Forces
# ----------------------------------------------------------------------------------------------------------------------
def forces(segment):
    """
    Updates total resultant forces on the vehicle

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function transforms and sums all force vectors (aerodynamic, thrust,
    gravity) into the inertial frame to get the total force on the vehicle.
    Special handling is included for vertical flight segments.

    **Required Segment Components**

    segment.state.conditions:
        frames:
            wind:
                - force_vector : array
                    Aerodynamic forces [N]
                - transform_to_inertial : array
                    Wind to inertial transform matrix
            body:
                - thrust_force_vector : array
                    Propulsive forces [N]
                - transform_to_inertial : array
                    Body to inertial transform matrix
            inertial:
                - gravity_force_vector : array
                    Gravitational force [N]

    **Major Assumptions**
    * Valid coordinate transformations
    * Proper force definitions
    * Compatible reference frames
    * Rigid body dynamics

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.total_force_vector [N]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    RCAIDE.Framework.Core
    """
 
    # unpack 
    conditions                    = segment.state.conditions 
    wind_force_vector             = conditions.frames.wind.force_vector
    body_thrust_force_vector      = conditions.frames.body.thrust_force_vector
    inertial_gravity_force_vector = conditions.frames.inertial.gravity_force_vector

    # unpack transformation matrices
    T_body2inertial = conditions.frames.body.transform_to_inertial
    T_wind2inertial = conditions.frames.wind.transform_to_inertial

    # to inertial frame
    F = orientation_product(T_wind2inertial,wind_force_vector)
    T = orientation_product(T_body2inertial,body_thrust_force_vector)
    if type(segment) ==  RCAIDE.Framework.Mission.Segments.Vertical_Flight.Climb:
        F =  np.zeros_like(T)
    elif type(segment) ==  RCAIDE.Framework.Mission.Segments.Vertical_Flight.Hover:
        F =  np.zeros_like(T)
    elif type(segment) ==  RCAIDE.Framework.Mission.Segments.Vertical_Flight.Descent:
        F =  np.zeros_like(T) 
    W = inertial_gravity_force_vector

    # sum of the forces
    F_tot = F +  T  + W 

    # pack
    conditions.frames.inertial.total_force_vector[:,:] = F_tot[:,:]

    return
 