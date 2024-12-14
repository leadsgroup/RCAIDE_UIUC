# RCAIDE/Library/Missions/Segments/Descent/ Constant_Speed_Constant_Angle_noise.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------  
#  IMPORT 
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports  
from RCAIDE.Framework.Core import Units 

# pacakge imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Expand State
# ----------------------------------------------------------------------------------------------------------------------   
def expand_state(segment):
    """Makes all vectors in the state the same size.

    Assumptions:
    A 4 km threshold, this discretizes the mission to take measurements at the right place for certification maneuvers.

    Source:
    N/A

    Inputs:
    state.numerics.number_of_control_points  [Unitless]
    segment.descent_angle                 [Radians]
    segment.air_speed                     [meters/second]
 
    Outputs:
    state.numerics.number_of_control_points

    Properties Used:
    N/A
    """         
    dt            = 0.5  # time step in seconds for noise calculation - Certification requirement    
    air_speed     = segment.air_speed  
    s0            = 4000. # Defining the initial position of the measureament will start at 4 km from the threshold
    v_x           = air_speed * np.cos(segment.descent_angle) 
    
    #number of time steps (space discretization)  
    total_time    = s0/v_x    
    n_points      = np.ceil(total_time/dt +1)       
    
    segment.state.numerics.number_of_control_points = n_points
    segment.state.expand_rows(int(n_points),override=True)   
    
    return

# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------

def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant speed, constant descent angle. However, this follows a 2000 meter segment. This is a certification maneuver standard. The last point for the noise measurement is 50 feet.

    Source:
    N/A

    Inputs:
    segment.descent_angle                       [radians]
    segment.altitude_start                      [meters]
    segment.altitude_end                        [meters]
    segment.air_speed                           [meters/second]
    state.numerics.dimensionless.control_points [array]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """     
    
    
    # unpack
    descent_angle= segment.descent_angle
    air_speed    = segment.air_speed  
    beta         = segment.sideslip_angle 
    t_nondim     = segment.state.numerics.dimensionless.control_points
    conditions   = segment.state.conditions  
    
    altf = 50. * Units.feet #(50ft last point for the noise measureament)
    
    #Linear equation: y-y0=m(x-x0)
    m_xx0 = 2000 * np.tan(descent_angle)
    y0    =  m_xx0 + altf  #(Altitude at the microphone X position)
    
    alt0 = y0 + m_xx0 #(Initial altitude of the aircraft)

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0 
    
    # check for initial velocity vector
    if air_speed is None:
        if not segment.state.initials: raise AttributeError('initial airspeed not set')
        air_speed  =  np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1,:])     
        
    # process velocity vector
    v_mag = air_speed
    v_x   = np.cos(beta) * v_mag * np.cos(-descent_angle)
    v_y   = np.sin(beta) * v_mag * np.cos(-descent_angle)
    v_z   = -v_mag * np.sin(-descent_angle)
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context    
    
