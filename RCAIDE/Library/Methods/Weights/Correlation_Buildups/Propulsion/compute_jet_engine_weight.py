# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/compute_jet_engine_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Jet Engine Weight 
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_jet_engine_weight(thrust_sls):
    """
    Calculates the dry weight of a jet engine using empirical correlation.

    Parameters
    ----------
    thrust_sls : float
        Sea level static thrust of a single engine [N]

    Returns
    -------
    weight : float
        Dry weight of the engine [kg]

    Notes
    -----
    This method uses a simple power law correlation to estimate jet engine weight
    based on sea level static thrust. The correlation is based on historical data
    from commercial and military jet engines.

    **Major Assumptions**
        * Engine weight scales with thrust following a power law relationship
        * Correlation based on conventional turbofan engine designs
        * Weight estimate is for dry engine (no fluids)
        * Technology level representative of current generation engines

    **Theory**
    The engine weight is calculated using the following correlation:
    .. math::
        W_{engine} = 0.4054(T_{sls})^{0.9255}

    where:
        * :math:`T_{sls}` is the sea level static thrust in pounds force
        * Weight is output in pounds, then converted to kilograms

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_piston_engine_weight
    """     
    # setup
    thrust_sls_en = thrust_sls / Units.force_pound # Convert N to lbs force  
    
    # process
    weight = (0.4054*thrust_sls_en ** 0.9255) * Units.lb # Convert lbs to kg
    
    return weight