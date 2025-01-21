# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_fuselage_weight.py
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
# Fuselage Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_fuselage_weight(S_fus, Nult, TOW, w_fus, h_fus, l_fus, l_ht, q_c, V_fuse, diff_p_fus):
    """
    Computes fuselage weight for general aviation aircraft using Raymer's method.
    Accounts for structural loads, pressurization, and basic systems integration.

    Parameters
    ----------
    S_fus : float
        Fuselage wetted area [m²]
    Nult : float
        Ultimate load factor
    TOW : float
        Maximum takeoff weight [kg]
    w_fus : float
        Maximum fuselage width [m]
    h_fus : float
        Maximum fuselage height [m]
    l_fus : float
        Fuselage length [m]
    l_ht : float
        Tail arm length (CG to horizontal tail 0.25MAC) [m]
    q_c : float
        Dynamic pressure at cruise [Pa]
    V_fuse : float
        Pressurized fuselage volume [m³]
    diff_p_fus : float
        Maximum cabin pressure differential [Pa]

    Returns
    -------
    weight : float
        Fuselage structural weight [kg]

    Notes
    -----
    Uses Raymer's correlation developed for general aviation aircraft. Refer to Raymer, 
    page 460 (in the 4th edition) for more details.

    **Major Assumptions**
        * Conventional aluminum construction
        * Standard structural design margins
        * Traditional fuselage layout
        * No special design features (e.g., cargo door)
        * FAR Part 23 certification basis
        * Basic systems integration requirements

    **Theory**
    Weight is computed using:
    .. math::
        W_{fus} = 0.052S_f^{1.086}(N_zW_{to})^{0.177}L_t^{-0.051}
                  (L/D)^{-0.072}q^{0.241} + 11.9(V_p\\Delta P)^{0.271}

    where:
        * S_f = fuselage wetted area
        * N_z = ultimate load factor
        * W_to = takeoff weight
        * L_t = tail arm length
        * L/D = fuselage fineness ratio
        * q = dynamic pressure
        * V_p = pressurized volume
        * ΔP = pressure differential

    The correlation accounts for:
        * Bending and torsional loads
        * Pressurization loads
        * Tail loads
        * Basic systems integration
        * Minimum gauge requirements
        * Standard structural margins

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018.

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """
    # take average as diameter
    d_fus    = (h_fus+w_fus)/2.
    
    # obtained from http://homepage.ntlworld.com/marc.barbour/structures.html
    d_str    = .025*d_fus+1.*Units.inches
    
    diff_p   = diff_p_fus / (Units.force_pound / Units.ft**2.) # Convert Pascals to lbs/ square ft 
    tail_arm = np.abs(l_ht)/Units.ft 
    weight   = TOW / Units.lb    # Convert kg to lbs
    area     = S_fus / (Units.ft**2.) # Convert square meters to square ft 
    q        = q_c /(Units.force_pound / Units.ft**2.)

    # Calculate weight of wing for traditional aircraft vertical tail without rudder
    fuselage_weight = .052*(area**1.086)*((Nult*weight)**.177)*(tail_arm**(-.051))*((l_fus/d_str)**(-.072))*(q**.241)+11.9*((V_fuse* diff_p)**.271)

    weight = fuselage_weight*Units.lbs #convert to kg
    return weight