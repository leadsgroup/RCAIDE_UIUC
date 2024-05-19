## @ingroup Library-Methods-Missions-Common-Residuals
# RCAIDE/Library/Methods/Missions/Common/Residuals/transition_flight_dynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke
  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# Pacakge imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Residuals 
def transition_flight_dynamics(segment):
    """ Calculates a residual based on forces
    
        Assumptions:
        The vehicle is not accelerating, doesn't use gravity
        
        Inputs:
            segment.state.conditions:
                frames.inertial.total_force_vector [Newtons]
                weights.total_mass                 [kg]
            
        Outputs:
            segment.state.residuals.forces [meters/second^2]

        Properties Used:
        N/A
                                
    """        
    
    FT = segment.state.conditions.frames.inertial.total_force_vector
    m  = segment.state.conditions.weights.total_mass[:,0] 
     
    if segment.flight_dynamics.force_x: 
        segment.state.residuals.force_x[:,0] = FT[:,0]/m 
    if segment.flight_dynamics.force_y: 
        segment.state.residuals.force_y[:,0] = FT[:,1]/m      
    if segment.flight_dynamics.force_z: 
        segment.state.residuals.force_z[:,0] = FT[:,2]/m     

    return
    
    
 
    
    