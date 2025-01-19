# RCAIDE/Library/Mission/Common/Update/linear_inertial_horizontal_position.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# Package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Integrate Position
# ----------------------------------------------------------------------------------------------------------------------
 
def linear_inertial_horizontal_position(segment):
    """
    Computes linear position for straight-line flight segments

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function calculates the horizontal position components for straight
    flight paths. Uses velocity integration and heading angle to determine
    position changes.

    **Required Segment Components**

    segment:
        state.conditions:
            frames.inertial:
                - position_vector : array
                    Current position [m]
                - velocity_vector : array
                    Current velocity [m/s]
                - aircraft_range : array
                    Distance traveled [m]
        state.numerics:
            - number_of_control_points : int
                Number of discretization points
            time:
                - integrate : array
                    Time integration operator
        true_course : float
            Vehicle heading angle [rad]

    **Major Assumptions**
    * Flat earth
    * Constant heading
    * Planar motion
    * Well-defined trajectory

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.frames.inertial.position_vector [m]
        - conditions.frames.inertial.aircraft_range [m]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """        

    conditions = segment.state.conditions
    psi        = segment.true_course       # sign convetion is clockwise positive
    cpts       = int(segment.state.numerics.number_of_control_points)
    x0         = conditions.frames.inertial.position_vector[0,None,0:1+1]
    R0         = conditions.frames.inertial.aircraft_range[0,None,0:1+1]
    vx         = conditions.frames.inertial.velocity_vector[:,0:1+1]
    I          = segment.state.numerics.time.integrate  
    trajectory = np.repeat( np.atleast_2d(np.array([np.cos(psi),np.sin(psi)])),cpts , axis = 0) 
    
    # integrate
    x = np.dot(I,vx)  
    x[:,1] = x[:,0]
    
    # pack
    conditions.frames.inertial.position_vector[:,0:1+1] = x0 + x[:,:]*trajectory
    conditions.frames.inertial.aircraft_range[:,0]      = R0 + x[:,0]  
    
    return