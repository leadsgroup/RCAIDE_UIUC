# RCAIDE/Library/Missions/Common/Update/acceleration.py
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
    """ Differentiates the velocity vector to get accelerations
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Inputs:
            segment.state.conditions:
                frames.inertial.velocity_vector     [meters/second]
            segment.state.numerics.time.differentiate       [float]
            
        Outputs:
            segment.state.conditions:           
                frames.inertial.acceleration_vector [meters]

        Properties Used:
        N/A
                                
    """            
    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   