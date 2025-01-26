# RCAIDE/Library/Methods/Propulsors/Common/compute_avionics_performance.py
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports

def compute_avionics_power_draw(avionics,avionics_conditions,conditions): 
    """
    Computes the power draw of the avionics system during mission operations.
    
    Parameters
    ----------
    avionics : RCAIDE.Library.Components.Systems.Avionics
        The avionics system object containing system specifications and power requirements
    avionics_conditions : RCAIDE.Framework.Mission.Common.Conditions
        Container for avionics-specific conditions during the mission
    conditions : RCAIDE.Framework.Mission.Common.Conditions
        General mission conditions container
        
    Returns
    -------
    None
        
    Notes
    -----
    This function assigns the constant power draw specified in the avionics
    system configuration to the power conditions array. The power draw is
    assumed to be constant throughout the mission segment.
    
    **Major Assumptions**
        * Avionics power draw is constant and does not vary with flight conditions
    
    See Also
    --------
    RCAIDE.Framework.Mission.Common.Conditions
    """
    avionics_conditions.power[:,0] = avionics.power_draw  
    return 