# RCAIDE/Library/Missions/Common/Update/linear_inertial_horizontal_position.py
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
    """ Determines how far the airplane has traveled. 
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Inputs:
            segment.state.conditions:
                frames.inertial.position_vector [meters]
                frames.inertial.velocity_vector [meters/second]
            segment.state.numerics.time.integrate       [float]
            
        Outputs:
            segment.state.conditions:           
                frames.inertial.position_vector [meters]

        Properties Used:
        N/A
                                
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