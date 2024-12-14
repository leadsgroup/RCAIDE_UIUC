# RCAIDE/Library/Missions/Common/Update/angular_acceleration.py
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
    """ Differentiates the angular velocity vector to get angular accelerations
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Inputs:
            segment.state.conditions:
                frames.inertial.angular_velocity_vector     [rad/second]
            segment.state.numerics.time.differentiate       [float]
            
        Outputs:
            segment.state.conditions:           
                frames.inertial.angular_acceleration_vector [rad/s^2]

        Properties Used:
        N/A
                                
    """            
    
    # unpack conditions
    omega = segment.state.conditions.frames.inertial.angular_velocity_vector
    D     = segment.state.numerics.time.differentiate
    
    # accelerations
    ang_acc = np.dot(D,omega)
    
    # pack conditions
    segment.state.conditions.frames.inertial.angular_acceleration_vector[:,:] = ang_acc[:,:]   