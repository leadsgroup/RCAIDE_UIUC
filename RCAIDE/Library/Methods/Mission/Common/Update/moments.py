## @ingroup Library-Methods-Missions-Segments-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/moments.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core  import  orientation_product  

# ----------------------------------------------------------------------------------------------------------------------
#  Update Moments
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Segments-Common-Update
def moments(segment): 
    """ Updates the total resultant moment on the vehicle 
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.conditions.:
                frames.wind.force_vector          [N] 
                frames.body.thrust_force_vector        [N]
                frames.inertial.gravity_force_vector   [N]
        Outputs:
            segment.conditions
                frames.inertial.total_force_vector     [N]
 
      
        Properties Used:
        N/A
                    
    """    

    # unpack
    conditions         = segment.state.conditions  
    wind_moment_vector = conditions.frames.wind.moment_vector
    
    # unpack transformation matrices
    T_wind2inertial = conditions.frames.wind.transform_to_inertial

    # to inertial frame
    M = orientation_product(T_wind2inertial, wind_moment_vector) 
    
    # pack
    conditions.frames.inertial.total_moment_vector[:,:] = M[:,:]

    return
