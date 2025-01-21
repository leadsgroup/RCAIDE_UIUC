# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/compute_piston_engine_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Piston Engine Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_piston_engine_weight(max_power, kwt2=5.22, xwt=.780):
    """
    Calculates the weight of a piston engine using empirical correlation.

    Parameters
    ----------
    max_power : float
        Maximum safe operating power [W]
    kwt2 : float, optional
        Weight correlation coefficient, defaults to 5.22
    xwt : float, optional
        Weight correlation exponent, defaults to 0.780

    Returns
    -------
    mass : float
        Mass of the piston engine [kg]

    Notes
    -----
    This method uses a power law correlation to estimate piston engine weight
    based on maximum power output. The correlation is derived from general 
    aviation engine data.

    **Major Assumptions**
        * Engine weight scales with power following a power law relationship
        * Correlation based on conventional aircraft piston engine designs
        * Weight estimate is for dry engine (no fluids)
        * Technology level representative of current generation engines

    **Theory**
    The engine weight is calculated using the following correlation:
    .. math::
        W_{engine} = k_{wt2}(P_{max})^{x_{wt}}

    where:
        * :math:`P_{max}` is the maximum power in brake horsepower
        * :math:`k_{wt2}` is the weight correlation coefficient
        * :math:`x_{wt}` is the weight correlation exponent
        * Weight is calculated in pounds, then converted to kilograms

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_jet_engine_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_motor_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.integrated_propulsion_general_aviation
    """    
    bhp    = max_power/Units.horsepower
    weight = kwt2*((bhp)**xwt)  # weight in lbs.
    mass   = weight*Units.lbs
    return mass