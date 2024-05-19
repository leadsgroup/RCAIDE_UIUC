## @ingroup Library-Methods-Missions-Common-Residuals
# RCAIDE/Library/Methods/Missions/Common/Residuals/vertical_flight_dynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Residuals  
def vertical_flight_dynamics(segment):
    """ Calculates a residual based on forces
    
        Assumptions:
        The vehicle is not accelerating, doesn't use gravity. Only vertical forces
        
        Inputs:
            state.conditions:
                frames.inertial.total_force_vector [Newtons]
            
        Outputs:
            state.residuals.forces [meters/second^2]

        Properties Used:
        N/A
                                
    """            
    
    FT = segment.state.conditions.frames.inertial.total_force_vector
 
    if segment.flight_dynamics.force_x: 
        segment.state.residuals.force_x[:,0] = FT[:,0] 
    if segment.flight_dynamics.force_y: 
        segment.state.residuals.force_y[:,0] = FT[:,1]      
    if segment.flight_dynamics.force_z: 
        segment.state.residuals.force_z[:,0] = FT[:,2] 
    return
    
    
 
    
