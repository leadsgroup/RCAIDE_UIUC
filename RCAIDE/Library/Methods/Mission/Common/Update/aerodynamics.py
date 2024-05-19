## @ingroup Library-Methods-Missions-Common-Update 
# RCAIDE/Library/Methods/Missions/Common/Update/aerodynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Update
def aerodynamics(segment):
    """ Gets aerodynamics conditions
    
        Assumptions:
        +X out nose
        +Y out starboard wing
        +Z down

        Inputs:
            segment.analyses.aerodynamics_model                    [Function]
            aerodynamics_model.settings.maximum_lift_coefficient   [unitless]
            aerodynamics_model.geometry.reference_area             [meter^2]
            segment.state.conditions.freestream.dynamic_pressure   [pascals]

        Outputs:
            conditions.aerodynamics.coefficients.lift [unitless]
            conditions.aerodynamics.coefficients.drag [unitless]
            conditions.frames.wind.force_vector [newtons]
            conditions.frames.wind.drag_force_vector [newtons]

        Properties Used:
        N/A
    """
    
    # unpack
    conditions         = segment.state.conditions
    aerodynamics_model = segment.analyses.aerodynamics
    q                  = segment.state.conditions.freestream.dynamic_pressure
    Sref               = aerodynamics_model.geometry.reference_area
    CLmax              = aerodynamics_model.settings.maximum_lift_coefficient
    
    # call aerodynamics model
    results = aerodynamics_model(segment)    
    
    # unpack results
    CL = results.lift.total
    CD = results.drag.total

    CL[q<=0.0] = 0.0
    CD[q<=0.0] = 0.0
    
    # CL limit
    CL[CL>CLmax] = CLmax
    
    CL[CL< -CLmax] = -CLmax
        
    # dimensionalize
    F = segment.state.ones_row(3) * 0.0

    F[:,2] = ( -CL * q * Sref )[:,0]
    F[:,0] = ( -CD * q * Sref )[:,0]

    results.force_vector = F

    # pack conditions
    conditions.aerodynamics.coefficients.lift  = CL
    conditions.aerodynamics.coefficients.drag  = CD
    conditions.frames.wind.force_vector[:,:]   = F[:,:]

    return