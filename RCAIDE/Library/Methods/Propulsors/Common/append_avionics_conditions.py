# RCAIDE/Library/Methods/Propulsors/Common/append_avionics_conditions.py
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_motor_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_avionics_conditions(avionics,segment,bus):  
    """
    Appends avionics power conditions placeholders to the mission segment state for a given electrical bus.
    
    Parameters
    ----------
    avionics : RCAIDE.Library.Components.Systems.Avionics
        The avionics system object containing system specifications
    segment : RCAIDE.Framework.Mission.Segments.Segment
        The mission segment to which the conditions will be appended
    bus : RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus
        The electrical bus that powers the avionics system
        
    Returns
    -------
    None
        
    Notes
    -----
    This function initializes the power consumption state for avionics systems
    in the mission segment. The initial power is set to zero and can be updated
    late (for example, during mission analysis).
    
    See Also
    --------
    RCAIDE.Library.Components.Systems.Avionics
    """
    ones_row    = segment.state.ones_row
    segment.state.conditions.energy[bus.tag][avionics.tag]            = Conditions()
    segment.state.conditions.energy[bus.tag][avionics.tag].power      = 0 * ones_row(1) 
    
    return 
