# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Human_Powered/compute_fuselage_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------
# Fuselage Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_fuselage_weight(Sts, qm, Ltb):
    """
    Computes fuselage weight for human-powered aircraft using MIT Daedalus correlations.
    Specifically designed for ultra-lightweight carbon fiber composite structures.

    Parameters
    ----------
    Sts : float
        Tail surface area [m²]
    qm : float
        Dynamic pressure at maneuvering speed [Pa]
    Ltb : float
        Tailboom length [m]

    Returns
    -------
    Wtb : float
        Tailboom weight [kg]

    Notes
    -----
    Uses empirical correlations developed from the MIT Daedalus human-powered aircraft project.

    **Major Assumptions**
        * Ultra-lightweight carbon fiber composite construction
        * Minimal structural margins
        * Simple tubular tailboom design
        * No pressurization requirements
        * Limited payload capacity
        * Low-speed flight regime
        * Single-pilot configuration

    **Theory**
    Weight is computed using:
    .. math::
        W_{tb} = (0.114L_{tb} + 0.0196L_{tb}^2)(1 + \\frac{q_mS_{ts}/78.5 - 1}{2})

    where:
        * L_tb = tailboom length
        * q_m = dynamic pressure at maneuvering speed
        * S_ts = tail surface area

    The correlation accounts for:
        * Bending and torsional loads
        * Tail surface attachment structure
        * Minimum gauge constraints
        * Basic systems integration

    References
    ----------
    [1] Langford, J. (1989). The daedalus project - a summary of lessons learned. 
        Aircraft Design and Operations Meeting. https://doi.org/10.2514/6.1989-2048 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_operating_empty_weight
    """
    Wtb=(Ltb*1.14e-1 +(1.96e-2)*(Ltb**2))*(1.0+((qm*Sts)/78.5-1.0)/2.0)
    
    return Wtb