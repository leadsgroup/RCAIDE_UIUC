# RCAIDE/Library/Missions/Common/Update/kinematics.py
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
    """ Updates the kinematics of the rigid body (aircraft) 
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.:
                 conditions.frames.inertial.velocity_vector    [m/s]
                 numerics.time.differentiate                   [-]
                 
        Outputs:
            segment.conditions 
                 frames.inertial.acceleration_vector 
      
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