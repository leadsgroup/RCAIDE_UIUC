## @ingroup Library-Methods-Missions-Common-Residuals
# RCAIDE/Library/Methods/Missions/Common/Residuals/level_flight_dynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Residuals
def level_flight_dynamics(segment):
    """ Calculates a force and moment residuals 
                                
    """        
    if 'acceleration' in segment:
        ax      = segment.acceleration  
        one_row = segment.state.ones_row 
        a       = one_row(3)*0
        a[:,0]  = ax 
        segment.state.conditions.frames.inertial.acceleration_vector = a
    elif type(segment) == RCAIDE.Framework.Mission.Segments.Cruise.Constant_Pitch_Rate_Constant_Altitude:  
        v  = segment.state.conditions.frames.inertial.velocity_vector
        D  = segment.state.numerics.time.differentiate   
        segment.state.conditions.frames.inertial.acceleration_vector =  np.dot(D,v)
        
    FT = segment.state.conditions.frames.inertial.total_force_vector
    a  = segment.state.conditions.frames.inertial.acceleration_vector        
        
    if 'angular_acceleration' in segment:
        ang_acc_x      = segment.angular_acceleration  
        one_row = segment.state.ones_row 
        ang_acc        = one_row(3)*0
        ang_acc[:,0]  = ang_acc_x 
        segment.state.conditions.frames.inertial.angular_acceleration_vector = ang_acc
        
    elif type(segment) == RCAIDE.Framework.Mission.Segments.Cruise.Constant_Pitch_Rate_Constant_Altitude:  
        omega = segment.state.conditions.frames.inertial.angular_velocity_vector
        D  = segment.state.numerics.time.differentiate   
        segment.state.conditions.frames.inertial.angular_acceleration_vector =  np.dot(D,omega)        
    
    MT      = segment.state.conditions.frames.inertial.total_moment_vector    
    ang_acc = segment.state.conditions.frames.inertial.angular_acceleration_vector  
    m       = segment.state.conditions.weights.total_mass
    I       = segment.analyses.aerodynamics.geometry.mass_properties.moments_of_inertia.tensor 
    
    if segment.flight_dynamics.force_x: 
        segment.state.residuals.force_x[:,0] = FT[:,0]/m[:,0] - a[:,0]
    if segment.flight_dynamics.force_y: 
        segment.state.residuals.force_y[:,0] = FT[:,1]/m[:,0] - a[:,1]       
    if segment.flight_dynamics.force_z: 
        segment.state.residuals.force_z[:,0] = FT[:,2]/m[:,0] - a[:,2]  
    if  segment.flight_dynamics.moment_x:
        segment.state.residuals.moment_x[:,0] = MT[:,0]/I[0,0] - ang_acc[:,0]   
    if  segment.flight_dynamics.moment_y:
        segment.state.residuals.moment_y[:,0] = MT[:,1]/I[1,1] - ang_acc[:,1]   
    if  segment.flight_dynamics.moment_z:
        segment.state.residuals.moment_z[:,0] = MT[:,2]/I[2,2] - ang_acc[:,2]     

    return
    
    
 
    
