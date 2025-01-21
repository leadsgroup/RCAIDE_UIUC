# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_horizontal_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units
import  numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
# Horizontal Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_horizontal_tail_weight(S_h, AR_h, sweep_h, q_c, taper_h, t_c_h, Nult, TOW):
    """
    Computes horizontal tail weight for general aviation aircraft using Raymer's method.
    Accounts for geometry, loads, and basic systems integration.

    Parameters
    ----------
    S_h : float
        Horizontal tail reference area [m²]
    AR_h : float
        Horizontal tail aspect ratio
    sweep_h : float
        Quarter-chord sweep angle [rad]
    q_c : float
        Dynamic pressure at cruise [Pa]
    taper_h : float
        Horizontal tail taper ratio
    t_c_h : float
        Average thickness-to-chord ratio
    Nult : float
        Ultimate load factor
    TOW : float
        Maximum takeoff weight [kg]

    Returns
    -------
    weight : float
        Horizontal tail structural weight [kg]

    Notes
    -----
    Uses Raymer's correlation developed for general aviation aircraft.

    **Major Assumptions**
        * General aviation aircraft

    **Theory**
    Weight is computed using:
    .. math::
        W_{ht} = 0.016(N_zW_{to})^{0.414}q^{0.168}S_{ht}^{0.896}
                 (\\frac{100t/c}{cos\\Lambda})^{-0.12}
                 (\\frac{A}{cos^2\\Lambda})^{0.043}\\lambda^{-0.02}

    where:
        * N_z = ultimate load factor
        * W_to = takeoff weight
        * q = dynamic pressure
        * S_ht = horizontal tail area
        * t/c = thickness ratio
        * Λ = quarter-chord sweep
        * A = aspect ratio
        * λ = taper ratio

    The correlation accounts for:
        * Bending and torsional loads
        * Elevator integration
        * Control system attachments
        * Minimum gauge requirements
        * Standard structural margins

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018.

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_vertical_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """
    # unpack inputs
    W_0   = TOW / Units.lb # Convert kg to lbs
    S_ht  = S_h/ Units.ft**2 # Convert from meters squared to ft squared  
    q     = q_c /(Units.force_pound / Units.ft**2.)

    #Calculate weight of wing for traditional aircraft horizontal tail
    weight_English = .016*((Nult*W_0)**.414)*(q**.168)*(S_ht**.896)*((100.*t_c_h/np.cos(sweep_h))**(-.12))*((AR_h/(np.cos(sweep_h)**2))**.043)*(taper_h**(-.02))
    weight         = weight_English * Units.lbs # Convert from lbs to kg

    return weight