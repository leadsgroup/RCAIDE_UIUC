# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/total_drag.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  Wave Drag 
# ---------------------------------------------------------------------------------------------------------------------- 
def total_drag(state,settings,geometry):
    """ Computes the total drag of an aircraft.

    Assumptions:
        None

    Source:
        None 

    Args:
        settings.
          drag_coefficient_increment                          (float): drag_coefficient_increment [Unitless]
          lift_to_drag_adjustment                             (float): lift_to_drag_adjustment    [Unitless]  
        state.conditions.aerodynamics.coefficients.drag.
          trim_corrected_drag                         (numpy.ndarray): trim corrected drag        [Unitless]
          spoiler_drag                                (numpy.ndarray): spoiler drag               [Unitless]
        geometry                                               (dict): aircraft data structure    [-]


    Returns:
        None 
    """

    # unpack inputs  
    trim_correction_factor  = settings.trim_drag_correction_factor    
    drag                    =  state.conditions.aerodynamics.coefficients.drag

    # various drag components
    parasite_total        = drag.parasite.total            
    induced_total         = drag.induced.total            
    compressibility_total = drag.compressible.total     
    miscellaneous_drag    = drag.miscellaneous.total
    cooling_drag          = drag.cooling.total 

    # untrimmed drag 
    untrimmed_drag  =  parasite_total + induced_total  + compressibility_total + miscellaneous_drag + cooling_drag
    
    # trim correction
    corrected_aircraft_total_trim_drag = trim_correction_factor * untrimmed_drag 
    drag.miscellaneous.trim_correction_factor = trim_correction_factor    

    # Unpack inputs 

    drag_coefficient_increment = settings.drag_coefficient_increment 
    spoiler_drag               = drag.spoiler_drag 

    # Add drag_coefficient_increment
    aircraft_total_drag =  corrected_aircraft_total_trim_drag   + drag_coefficient_increment + spoiler_drag
    drag.drag_coefficient_increment = drag_coefficient_increment
    
    # Add L/D correction
    aircraft_total_drag  = aircraft_total_drag/(1.+settings.lift_to_drag_adjustment) 

    # Store to results 
    drag.total           = aircraft_total_drag
    
    return  