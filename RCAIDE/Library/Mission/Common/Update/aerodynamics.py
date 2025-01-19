# RCAIDE/Library/Mission/Common/Update/aerodynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------
def aerodynamics(segment):
    """
    Computes aerodynamic forces and coefficients

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function evaluates the aerodynamic model to obtain forces and moments.
    Uses a right-handed coordinate system:
    - +X out nose
    - +Y out starboard wing
    - +Z down

    **Required Segment Components**

    segment:
        analyses.aerodynamics:
            - vehicle.reference_area : float
                Reference wing area [m²]
            - settings.maximum_lift_coefficient : float
                Maximum allowable lift coefficient
            - vehicle.wings.main_wing:
                - chords.mean_aerodynamic : float
                    Mean aerodynamic chord [m]
                - spans.projected : float
                    Projected wingspan [m]

    state.conditions:
        freestream:
            - dynamic_pressure : array
                Dynamic pressure [Pa]

    **Major Assumptions**
    * Valid aerodynamic model
    * Subsonic flow
    * Small angle approximations
    * Rigid aircraft

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.aerodynamics.coefficients
        - conditions.frames.wind.force_vector
        - conditions.frames.wind.moment_vector

    
    """
    
    # unpack
    conditions         = segment.state.conditions
    aerodynamics_model = segment.analyses.aerodynamics
    q                  = segment.state.conditions.freestream.dynamic_pressure
    Sref               = aerodynamics_model.vehicle.reference_area
    CLmax              = aerodynamics_model.settings.maximum_lift_coefficient 
    MAC                = aerodynamics_model.vehicle.wings.main_wing.chords.mean_aerodynamic
    span               = aerodynamics_model.vehicle.wings.main_wing.spans.projected 
    
    # call aerodynamics model
    _ = aerodynamics_model(segment)     

    # Forces 
    CL = conditions.aerodynamics.coefficients.lift.total
    CD = conditions.aerodynamics.coefficients.drag.total
    CY = conditions.static_stability.coefficients.Y

    CL[q<=0.0] = 0.0
    CD[q<=0.0] = 0.0
    CL[CL>CLmax] = CLmax
    CL[CL< -CLmax] = -CLmax

    # dimensionalize
    F      = segment.state.ones_row(3) * 0.0
    F[:,2] = ( -CL * q * Sref )[:,0]
    F[:,1] = ( -CY * q * Sref )[:,0]
    F[:,0] = ( -CD * q * Sref )[:,0]

    # rewrite aerodynamic CL and CD
    conditions.aerodynamics.coefficients.lift.total  = CL
    conditions.aerodynamics.coefficients.drag.total  = CD
    conditions.frames.wind.force_vector[:,:]   = F[:,:]

    # -----------------------------------------------------------------
    # Moments
    # -----------------------------------------------------------------
    C_M = conditions.static_stability.coefficients.M
    C_L = conditions.static_stability.coefficients.L
    C_N = conditions.static_stability.coefficients.N

    C_M[q<=0.0] = 0.0

    # dimensionalize
    M      = segment.state.ones_row(3) * 0.0
    M[:,0] = (C_L[:,0] * q[:,0] * Sref * span)
    M[:,1] = (C_M[:,0] * q[:,0] * Sref * MAC)
    M[:,2] = (C_N[:,0] * q[:,0] * Sref * span)

    # pack conditions
    conditions.frames.wind.moment_vector[:,:] = M[:,:] 

    return