# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_vertical_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units,  Data
import  numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
# Vertical Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_vertical_tail_weight(S_v, AR_v, sweep_v, q_c, taper_v, t_c_v, Nult, TOW, t_tail, rudder_fraction=0.25):
    """
    Calculates the weight of the vertical tail for a general aviation aircraft using empirical correlations.

    Parameters
    ----------
    S_v : float
        Vertical tail reference area [m^2]
    AR_v : float
        Vertical tail aspect ratio
    sweep_v : float
        Quarter-chord sweep angle [radians]
    q_c : float
        Dynamic pressure at cruise [Pa]
    taper_v : float
        Vertical tail taper ratio
    t_c_v : float
        Vertical tail thickness-to-chord ratio
    Nult : float
        Ultimate load factor
    TOW : float
        Maximum takeoff weight [kg]
    t_tail : str
        Flag indicating T-tail configuration ('yes' or 'no')
    rudder_fraction : float, optional
        Fraction of vertical tail area that is rudder, defaults to 0.25

    Returns
    -------
    W_tail_vertical : float
        Weight of the vertical tail [kg]

    Notes
    -----
    This method uses Raymer's empirical correlation to estimate vertical tail weight
    for general aviation aircraft. The correlation accounts for T-tail configurations
    with a weight penalty.

    **Major Assumptions**
        * Conventional aluminum construction
        * Rudder comprises 25% of vertical tail area by default
        * T-tail configuration adds 20% to vertical tail weight
        * Weight correlation based on historical general aviation data. Does not include rudder weight

    **Theory**
    The vertical tail weight is calculated using the following correlation:
    .. math::
        W_{vt} = 0.073(1 + 0.2T_{tail})(N_{ult}W_0)^{0.376}q^{0.122}S_{vt}^{0.873}
        (\frac{100t/c}{\cos\Lambda})^{-0.49}(\frac{A}{\cos^2\Lambda})^{0.357}\lambda^{0.039}

    where:
        * :math:`T_{tail}` is 1 for T-tail configuration, 0 otherwise
        * :math:`\Lambda` is the quarter-chord sweep angle
        * :math:`\lambda` is the taper ratio

    References
    ----------
    [1] Raymer, D. P. (2018). Aircraft design: A conceptual approach: A conceptual approach. 
        American Institute of Aeronautics and Astronautics Inc. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_horizontal_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """
    # unpack inputs
    W_0   = TOW / Units.lb # Convert kg to lbs
    S_vt  = S_v/ Units.ft**2 # Convert from meters squared to ft squared  
    q     = q_c /(Units.force_pound / Units.ft**2.)

    # Determine weight of the vertical portion of the tail
    if t_tail == "yes": 
        T_tail_factor = 1.# Weight of vertical portion of the T-tail is 20% more than a conventional tail
    else: 
        T_tail_factor = 0.

    # Calculate weight of wing for traditional aircraft vertical tail without rudder
    tail_vert_English = .073*(1+.2*T_tail_factor)*((Nult*W_0)**(.376))*(q**.122)*(S_vt**.873)*((100.*t_c_v/np.cos(sweep_v))**(-.49))*((AR_v/(np.cos(sweep_v)**2.))**.357)*(taper_v**.039)

    # packup outputs
    W_tail_vertical = tail_vert_English * Units.lbs # Convert from lbs to kg

    return W_tail_vertical
