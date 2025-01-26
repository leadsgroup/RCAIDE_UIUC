# RCAIDE/Library/Methods/Propulsors/Common/compute_payload_power_draw.py
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports  
def compute_payload_power_draw(payload,payload_conditions,conditions): 
    """
    Adds the power draw of the payload system during mission operations.
    
    Parameters
    ----------
    payload : RCAIDE.Library.Components.Payloads.Payload
        The payload system object containing system specifications and power requirements
    payload_conditions : RCAIDE.Framework.Mission.Common.Conditions
        Container for payload-specific conditions during the mission
    conditions : RCAIDE.Framework.Mission.Common.Conditions
        General mission conditions container
        
    Returns
    -------
    None
        
    Notes
    -----
    This function assigns the constant power draw specified in the payload
    system configuration to the power conditions array. The power draw is
    assumed to be constant throughout the mission segment.
    
    **Major Assumptions**
        * Payload power draw is constant throughout the mission segment
    
    See Also
    --------
    RCAIDE.Library.Components.Payloads.Payload
    RCAIDE.Framework.Mission.Common.Conditions
    """
    payload_conditions.power[:,0] = payload.power_draw  
    return 