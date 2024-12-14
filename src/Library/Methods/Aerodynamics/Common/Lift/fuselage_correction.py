# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/fuselage_correction.py
# (c) Copyright 2023 Aerospace Research Community LLC
#  
# Created: Mar 2024 M. Carke     

# ----------------------------------------------------------------------------------------------------------------------
#  Fuselage Correction
# ----------------------------------------------------------------------------------------------------------------------
def fuselage_correction(state,settings,geometry):  
    """Corrects aircraft lift based on fuselage effects

    Assumptions:
        None

    Source:
        adg.stanford.edu (Stanford AA241 A/B Course Notes)

    Args:
        settings.fuselage_lift_correction (float): fuselage lift correction [unitless]
        state.conditions.
          freestream.mach_number          (numpy.ndarray): mach number      [unitless]
          aerodynamics.angles.alpha       (numpy.ndarray): angle of attack  [radians]
          aerodynamics.coefficients.lift  (numpy.ndarray): lift coefficient [unitless]

    Returns:
        aircraft_total_lift               (numpy.ndarray): lift coefficient [unitless]   
    """        
    # unpack 
    fus_correction  = settings.fuselage_lift_correction
    wings_lift_comp = state.conditions.aerodynamics.coefficients.lift.total
    
    # total lift, assuming one fuselage
    aircraft_total_lift = wings_lift_comp * fus_correction  

    state.conditions.aerodynamics.coefficients.lift.total = aircraft_total_lift

    return 