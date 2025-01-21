# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Human_Powered/compute_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_tail_weight(Sts, bts, cts, Ntsr, t_cts, qm):
    """
    Computes tail surface weight for human-powered aircraft using MIT Daedalus correlations.
    Applicable for both horizontal and vertical tail surfaces.

    Parameters
    ----------
    Sts : float
        Tail surface area [m²]
    bts : float
        Tail surface span [m]
    cts : float
        Average tail surface chord [m]
    Ntsr : float
        Number of tail surface ribs = (bts²)/(deltats*Sts)
    t_cts : float
        Tail airfoil thickness to chord ratio
    qm : float
        Dynamic pressure at maneuvering speed [Pa]

    Returns
    -------
    weight : float
        Total tail surface weight [kg], including:
            - Wtss : Tail surface spar weight
            - Wtsr : Tail surface rib weight
            - Wts : Tail surface secondary structure weight
            - Wtsc : Tail surface covering weight

    Notes
    -----
    Uses empirical correlations developed from the MIT Daedalus human-powered aircraft project.

    **Major Assumptions**
        * Ultra-lightweight carbon fiber composite construction
        * Low-speed flight regime
        * Weight must be solved iteratively since gross weight is an input

    **Theory**
    Total weight is computed using:
    .. math::
        W_{tss} = (4.15\\times10^{-2}b_{ts} + 3.91\\times10^{-3}b_{ts}^2)(1 + \\frac{q_mS_{ts}/78.5 - 1}{12})

        W_{tsr} = N_{tsr}(0.116c_{ts}^2t_{c_{ts}} + 4.01\\times10^{-3}c_{ts})

        W_{ts} = 0.174\\frac{S_{ts}^2\\delta_{ts}^{4/3}}{b_{ts}}

        W_{tsc} = 1.93\\times10^{-2}S_{ts}

    where:
        * b_ts = tail surface span
        * S_ts = tail surface area
        * q_m = maneuvering dynamic pressure
        * c_ts = average tail surface chord
        * t_c_ts = thickness to chord ratio
        * δ_ts = average rib spacing ratio
        * N_tsr = number of tail surface ribs

    References
    ----------
    [1] Langford, J. (1989). The daedalus project - a summary of lessons learned. Aircraft Design 
        and Operations Meeting. https://doi.org/10.2514/6.1989-2048 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_operating_empty_weight
    """
    deltats = (bts**2)/(Sts*Ntsr)
    
    #Rudder & Elevator Primary Structure:
    Wtss = (bts * 4.15e-2 + (bts**2) * 3.91e-3) * (1.0 + ((qm * Sts)/78.5 - 1.0)/12.0)
    
    #Rudder & Elevator Secondary Structure:
    Wtsr = Ntsr * (cts**2 * t_cts * 1.16e-1 + cts * 4.01e-3)
    Wts  = 0.174*((Sts**2)*(deltats**(4./3.))/bts)
    Wtsc = Sts * 1.93e-2
    
    weight = Wtss + Wtsr + Wts + Wtsc
    
    return weight