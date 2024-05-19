## @ingroup Library-Methods-Missions-Segments-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/orientations.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core  import  angles_to_dcms, orientation_product, orientation_transpose

# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Update Orientations
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Update
def orientations(segment):
    
    """ Updates the orientation of the vehicle throughout the mission for each relevant axis
    
        Assumptions:
        This assumes the vehicle has 3 frames: inertial, body, and wind 
        
        Inputs:
        segment.state.conditions:
            frames.inertial.velocity_vector          [meters/second]
            frames.body.inertial_rotations           [Radians]
        segment.analyses.planet.features.mean_radius [meters]
        state.numerics.time.integrate                [float]
            
        Outputs:
            segment.state.conditions:           
                aerodynamics.angles.alpha         [Radians]
                aerodynamics.angles.beta          [Radians]
                aerodynamics.angles.roll          [Radians]
                frames.body.transform_to_inertial [Radians]
                frames.wind.body_rotations        [Radians]
                frames.wind.transform_to_inertial [Radians]
    

        Properties Used:
        N/A
    """

    # unpack
    conditions = segment.state.conditions
    V_inertial = conditions.frames.inertial.velocity_vector
    body_inertial_rotations = conditions.frames.body.inertial_rotations

    # ------------------------------------------------------------------
    #  Body Frame
    # ------------------------------------------------------------------

    # body frame rotations
    phi = body_inertial_rotations[:,0,None] 

    # body frame tranformation matrices
    T_inertial2body = angles_to_dcms(body_inertial_rotations,(2,1,0))
    T_body2inertial = orientation_transpose(T_inertial2body)

    # transform inertial velocity to body frame
    V_body = orientation_product(T_inertial2body,V_inertial)

    # project inertial velocity into body x-z plane
    V_stability = V_body * 1.
    V_stability[:,1] = 0
    V_stability_magnitude = np.sqrt( np.sum(V_stability**2,axis=1) )[:,None]

    # calculate angle of attack
    alpha = np.arctan2(V_stability[:,2],V_stability[:,0])[:,None]

    # calculate side slip
    beta = np.arctan2(V_body[:,1],V_stability_magnitude[:,0])[:,None]

    # pack aerodynamics angles
    conditions.aerodynamics.angles.alpha[:,0] = alpha[:,0]
    conditions.aerodynamics.angles.beta[:,0]  = beta[:,0]
    conditions.aerodynamics.angles.phi[:,0] = phi[:,0]

    # pack transformation tensor
    conditions.frames.body.transform_to_inertial = T_body2inertial 

    # ------------------------------------------------------------------
    #  Wind Frame
    # ------------------------------------------------------------------

    # back calculate wind frame rotations
    wind_body_rotations = body_inertial_rotations * 0.
    wind_body_rotations[:,0] = 0          # no roll in wind frame
    wind_body_rotations[:,1] = alpha[:,0] # theta is angle of attack
    wind_body_rotations[:,2] = beta[:,0]  # psi is side slip angle

    # wind frame tranformation matricies
    T_wind2body     = angles_to_dcms(wind_body_rotations,(2,1,0)) 
    T_wind2inertial = orientation_product(T_wind2body,T_body2inertial)

    # pack wind rotations
    conditions.frames.wind.body_rotations = wind_body_rotations

    # pack transformation tensor
    conditions.frames.wind.transform_to_inertial = T_wind2inertial
    
    return
         