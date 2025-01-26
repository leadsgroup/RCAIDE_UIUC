# RCAIDE/Library/Methods/Propulsors/Common/append_payload_conditions.py
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_motor_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_payload_conditions(payload,segment,bus):  
    """
    Appends payload power conditions placeholders to the mission segment state for a given electrical bus.
    
    Parameters
    ----------
    payload : RCAIDE.Library.Components.Payloads.Payload
        The payload system object containing system specifications
    segment : RCAIDE.Framework.Mission.Segments.Segment
        The mission segment to which the conditions will be appended
    bus : RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus
        The electrical bus that powers the payload system/that the payload is connected to
        
    Returns
    -------
    None
        
    Notes
    -----
    This function initializes the power consumption state for payload systems
    in the mission segment. The initial power is set to zero and can be updated
    during mission analysis. In the case of multiple buses, this function must
    be called for each bus.
    
    See Also
    --------
    RCAIDE.Library.Components.Payloads.Payload
    """
    ones_row    = segment.state.ones_row 
    segment.state.conditions.energy[bus.tag][payload.tag]       = Conditions()
    segment.state.conditions.energy[bus.tag][payload.tag].power = 0 * ones_row(1)  
    return 
