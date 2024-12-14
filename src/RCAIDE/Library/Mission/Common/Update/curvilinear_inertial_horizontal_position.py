# RCAIDE/Library/Missions/Common/Update/curvilinear_inertial_horizontal_position.py
# 
# 
# Created:  September 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# Package imports 
import numpy as np
from RCAIDE.Framework.Core import Units   

# ----------------------------------------------------------------------------------------------------------------------
#  Integrate Position
# ---------------------------------------------------------------------------------------------------------------------- 
def curvilinear_inertial_horizontal_position(segment):
    """ Determines how far the airplane has traveled and calculates position. 
    
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

    conditions  = segment.state.conditions 
    psi         = conditions.frames.planet.true_heading
    x0          = conditions.frames.inertial.position_vector[0, 0] 
    y0          = conditions.frames.inertial.position_vector[0, 1]
    R0          = conditions.frames.inertial.aircraft_range[0,None,0:1+1]
    vx          = conditions.frames.inertial.velocity_vector[:,0:1+1]
    I           = segment.state.numerics.time.integrate 
    R           = segment.turn_radius
    sign        = np.sign(segment.turn_angle)
    
    # integrate
    speed       = np.sqrt(vx[:, 0]**2+vx[:, 1]**2)
    arc_length  = np.dot(I,speed)
    
    theta       = psi - sign * 90 * Units.degrees         # Angle from circle center to the flight trajectory
    beta        =  psi[0, 0] + sign * 90 * Units.degrees  # Angle to the center of the circle from the initial position
    
    delta_x     = R * np.cos(beta) + R * np.cos(theta) # vector addition with a vector from the starting point to the center and then from the center to the position
    delta_y     = R * np.sin(beta) + R * np.sin(theta)
    x_position  = x0 + delta_x
    y_position  = y0 + delta_y
    
    # pack
    conditions.frames.inertial.position_vector[:,0] = x_position[:,0]
    conditions.frames.inertial.position_vector[:,1] = y_position[:,0] 
    conditions.frames.inertial.aircraft_range[:,0]  = R0 + arc_length
    return