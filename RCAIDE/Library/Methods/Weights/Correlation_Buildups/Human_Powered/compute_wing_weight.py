# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Human_Powered/compute_wing_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Wing Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_wing_weight(Sw, bw, cw, Nwr, t_cw, Nwer, nult, GW):
    """
    Computes wing weight for human-powered aircraft using MIT Daedalus correlations.
    Includes primary structure, secondary structure, and covering weights.

    Parameters
    ----------
    Sw : float
        Wing reference area [m²]
    bw : float
        Wing span [m]
    cw : float
        Average wing chord [m]
    Nwr : float
        Number of wing ribs = (bw²)/(deltaw*Sw)
    t_cw : float
        Wing airfoil thickness to chord ratio
    Nwer : float
        Number of wing end ribs (2*number of individual wing panels - 2)
    nult : float
        Ultimate load factor
    GW : float
        Aircraft gross weight [kg]

    Returns
    -------
    weight : float
        Total wing weight [kg], including:
            - Wws : Wing spar weight
            - Wwr : Wing rib weight
            - Wwer : Wing end rib weight
            - WwLE : Wing leading edge weight
            - WwTE : Wing trailing edge weight
            - Wwc : Wing covering weight

    Notes
    -----
    Uses empirical correlations developed from the MIT Daedalus human-powered aircraft project.

    **Major Assumptions**
        * Ultra-lightweight carbon fiber composite construction
        * Low-speed flight regime
        * Weight must be solved iteratively since gross weight is an input

    **Theory**
    Component weights computed using:
    .. math::
        W_{ws} = (0.117b_w + 0.011b_w^2)(1 + \\frac{n_{ult}GW/100 - 2}{4})

        W_{wr} = N_{wr}(0.055c_w^2t_{c_w} + 0.00191c_w)

        W_{wer} = N_{wer}(0.662c_w^2t_{c_w} + 0.00657c_w)

        W_{wLE} = 0.456\\frac{S_w^2\\delta_w^{4/3}}{b_w}

        W_{wTE} = 0.0277b_w

        W_{wc} = 0.0308S_w

    where:
        * b_w = wing span
        * n_ult = ultimate load factor
        * GW = gross weight
        * c_w = average chord
        * t_c_w = thickness to chord ratio
        * δ_w = average rib spacing ratio
        * S_w = wing area

    References
    ----------
    [1] Langford, J. (1989). The daedalus project - a summary of lessons learned. 
    Aircraft Design and Operations Meeting. https://doi.org/10.2514/6.1989-2048 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_operating_empty_weight
    """
    
    deltaw = (bw**2)/(Sw*Nwr)
    
    #Wing One Wire Main Spar:
    #Wws    = (bw * (3.10e-2) + (7.56e-3) * (bw**2)) * (1.0 + (nult * GW /100.0 - 2.0) / 4.0)
    
    #Wing Cantilever Main Spar:
    Wws    = (bw * (1.17e-1) + (1.1e-2) * (bw**2)) * (1.0 + (nult * GW /100.0 - 2.0) / 4.0)    
    
    #Wing Secondary Structure:
    Wwr    = Nwr * ((cw**2) * t_cw * 5.50e-2 + cw * 1.91e-3)
    Wwer   = Nwer * ((cw**2) * t_cw * 6.62e-1 + cw * 6.57e-3)
    WwLE   = 0.456 * ((Sw**2)*(deltaw**(4./3.))/bw)
    WwTE   = bw * 2.77e-2
    Wwc    = Sw * 3.08e-2
    
    weight = Wws + Wwr + Wwer + WwLE + WwTE + Wwc
    
    return weight