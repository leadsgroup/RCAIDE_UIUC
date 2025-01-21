# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/integrated_propulsion.py
# 
# 
# Created:  Sep 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Integrated Propulsion Weight 
# ----------------------------------------------------------------------------------------------------------------------
def integrated_propulsion(jet_engine_weight, engine_W_factor=1.6):
    """
    Calculates the total propulsion system weight for jet aircraft including installation effects.

    Parameters
    ----------
    jet_engine_weight : float
        Dry weight of the engine [kg]
    engine_W_factor : float, optional
        Weight increase factor for entire integrated propulsion system, defaults to 1.6

    Returns
    -------
    weight : float
        Total weight of the integrated propulsion system [kg]

    Notes
    -----
    This method estimates the total propulsion system weight including engine installation,
    nacelle, pylon, and all supporting systems for jet aircraft. The correlation uses a
    simple multiplicative factor to account for the weight growth from bare engine to
    installed system.

    **Major Assumptions**
        * Installation effects add 60% to bare engine weight by default
        * Includes engine exhaust, reverser, starting systems
        * Includes controls, lubricating, and fuel systems
        * Includes nacelle and pylon weights
        * Weight factor representative of current generation installations
        * Linear scaling of installation weight with engine weight

    **Theory**
    The total propulsion system weight is calculated using:
    .. math::
        W_{total} = k_{factor} * W_{engine}

    where:
        * :math:`k_{factor}` is the installation weight factor (default 1.6)
        * :math:`W_{engine}` is the bare engine weight

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_jet_engine_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.integrated_propulsion_general_aviation
    """   
    
    weight = jet_engine_weight * engine_W_factor
    
    return weight
    