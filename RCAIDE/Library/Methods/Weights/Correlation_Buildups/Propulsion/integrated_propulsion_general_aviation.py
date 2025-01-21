# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/integrated_propulsion_general_aviation.py
# 
# 
# Created:  Sep 2024, M. Clarke 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units

# ----------------------------------------------------------------------------------------------------------------------
#  Integrated Propulsion Weight 
# ----------------------------------------------------------------------------------------------------------------------
def integrated_propulsion_general_aviation(piston_engine_weight, num_eng, engine_W_factor=2.575, engine_W_exp=.922):
    """
    Calculates the total propulsion system weight for general aviation aircraft including engine installation effects.

    Parameters
    ----------
    piston_engine_weight : float
        Dry weight of a single engine [kg]
    num_eng : int
        Total number of engines on the aircraft
    engine_W_factor : float, optional
        Weight increase factor for entire integrated propulsion system, defaults to 2.575
    engine_W_exp : float, optional
        Weight correlation exponent, defaults to 0.922

    Returns
    -------
    mass : float
        Total mass of the integrated propulsion system [kg]

    Notes
    -----
    This method estimates the total propulsion system weight including engine mounts,
    cowling, propeller, and other installation effects for general aviation aircraft.
    The correlation accounts for the weight growth from bare engine to installed system.

    **Major Assumptions**
        * Installation effects scale with engine weight using power law relationship
        * Correlation based on conventional general aviation propulsion installations
        * Includes propeller, engine mounts, cowling, and basic engine systems
        * Weight factors representative of current generation installations
        * All engines on aircraft are identical

    **Theory**
    The total propulsion system weight is calculated using:
    .. math::
        W_{total} = N_{eng} * k_{factor} * (W_{engine})^{exp}

    where:
        * :math:`N_{eng}` is the number of engines
        * :math:`k_{factor}` is the installation weight factor
        * :math:`W_{engine}` is the bare engine weight in pounds
        * :math:`exp` is the weight correlation exponent

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018.

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_piston_engine_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.integrated_propulsion
    """
    engine_dry = piston_engine_weight/Units.lbs
    weight     = engine_W_factor * (engine_dry**engine_W_exp)*num_eng
    mass       = weight*Units.lbs #convert to kg

    return mass