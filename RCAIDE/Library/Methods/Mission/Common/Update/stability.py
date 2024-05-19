## @ingroup Library-Methods-Missions-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/stability.py
# 
# 
# Created:  Jul 2023, M. Clarke 

import numpy as np  
# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Update
def stability(segment): 
    """ Updates the stability of the aircraft 
        
        Assumptions:
        If stability model is defined, overwrite the aerodynamics calculations
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    # unpack
    stability_model    = segment.analyses.stability
    conditions         = segment.state.conditions
    
    if stability_model != None:
        Sref               = stability_model.geometry.reference_area
        MAC                = stability_model.geometry.wings.main_wing.chords.mean_aerodynamic
        span               = stability_model.geometry.wings.main_wing.spans.projected
        q                  = segment.state.conditions.freestream.dynamic_pressure
        CLmax              = stability_model.settings.maximum_lift_coefficient

        results = stability_model(segment)

        # -----------------------------------------------------------------
        # Forces
        # -----------------------------------------------------------------
        CL = results.lift.total
        CD = results.drag.total
        CY = conditions.static_stability.coefficients.Y

        CL[q<=0.0] = 0.0
        CD[q<=0.0] = 0.0
        CL[CL>CLmax] = CLmax
        CL[CL< -CLmax] = -CLmax

        # dimensionalize
        F      = segment.state.ones_row(3) * 0.0
        F[:,2] = ( -CL * q * Sref )[:,0]
        F[:,1] = ( CY * q * Sref * span )[:,0]
        F[:,0] = ( -CD * q * Sref )[:,0]

        # to implement when doing lateral stability
        phi    = conditions.frames.body.inertial_rotations[:,0]
        W      = conditions.weights.total_mass * conditions.freestream.gravity
        F[:,1] = F[:,1] + W[:,0]*np.sin(phi) 

        # rewrite aerodynamic CL and CD
        conditions.aerodynamics.coefficients.lift  = CL
        conditions.aerodynamics.coefficients.drag  = CD
        conditions.frames.wind.force_vector[:,:]   = F[:,:]

        # -----------------------------------------------------------------
        # Moments
        # -----------------------------------------------------------------
        CM = conditions.static_stability.coefficients.M
        CL = conditions.static_stability.coefficients.L
        CN = conditions.static_stability.coefficients.N

        CM[q<=0.0] = 0.0

        # dimensionalize
        M      = segment.state.ones_row(3) * 0.0
        M[:,0] = (CL[:,0] * q[:,0] * Sref * span)
        M[:,1] = (CM[:,0] * q[:,0] * Sref * MAC)
        M[:,2] = (CN[:,0] * q[:,0] * Sref * span)

        # pack conditions
        conditions.frames.wind.moment_vector[:,:] = M[:,:]

    return