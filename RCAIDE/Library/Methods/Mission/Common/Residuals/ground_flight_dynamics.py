## @ingroup Library-Methods-Missions-Common-Residuals
# RCAIDE/Library/Methods/Missions/Common/Residuals/ground_flight_dynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Residuals 
def ground_flight_dynamics(segment):
    """ Calculates a residual based on forces
    
        Assumptions:
        
        Inputs:
            segment.state.conditions:
                frames.inertial.total_force_vector    [Newtons]
                frames.inertial.velocity_vector       [meters/second]
                weights.total_mass                    [kg]
            segment.state.numerics.time.differentiate [vector]
            segment.velocity_end                      [meters/second]
            
        Outputs:
            segment.state: 
                residuals.final_velocity_error     [meters/second]
        Properties Used:
        N/A
                                
    """   

    # unpack inputs
    conditions = segment.state.conditions
    FT         = conditions.frames.inertial.total_force_vector
    vf         = segment.velocity_end
    v          = conditions.frames.inertial.velocity_vector
    m          = conditions.weights.total_mass
    D          = segment.state.numerics.time.differentiate

    # process and pack
    acceleration                                   = np.dot(D , v)
    conditions.frames.inertial.acceleration_vector = acceleration
    
    if vf == 0.0: vf = 0.01 
    segment.state.residuals.force_x[:,0] = FT[1:,0]/m[1:,0] - acceleration[1:,0] 
    segment.state.residuals.final_velocity_error = (v[-1,0] - vf)
    
    return