# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_main_wing_weight.py
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
# Main Wing Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_main_wing_weight(S_wing, m_fuel, AR_w, sweep_w, q_c, taper_w, t_c_w, Nult, TOW):
    """
    Computes main wing weight for general aviation aircraft using Raymer's method.
    Accounts for geometry, loads, fuel storage, and basic systems integration.

    Parameters
    ----------
    S_wing : float
        Wing reference area [m²]
    m_fuel : float
        Predicted weight of fuel in wing [kg]
    AR_w : float
        Wing aspect ratio
    sweep_w : float
        Quarter-chord sweep angle [rad]
    q_c : float
        Dynamic pressure at cruise [Pa]
    taper_w : float
        Wing taper ratio
    t_c_w : float
        Average thickness-to-chord ratio
    Nult : float
        Ultimate load factor
    TOW : float
        Maximum takeoff weight [kg]

    Returns
    -------
    weight : float
        Wing structural weight [kg]

    Notes
    -----
    Uses Raymer's correlation developed for general aviation aircraft.

    **Major Assumptions**
        * Conventional general aviation aircraft

    **Theory**
    Weight is computed using:
    .. math::
        W_{wing} = 0.036S_w^{0.758}W_f^{0.0035}
                   (\\frac{A}{cos^2\\Lambda})^{0.6}q^{0.006}\\lambda^{0.04}
                   (\\frac{100t/c}{cos\\Lambda})^{-0.3}(N_zW_{to})^{0.49}

    where:
        * S_w = wing area
        * W_f = fuel weight
        * A = aspect ratio
        * Λ = quarter-chord sweep
        * q = dynamic pressure
        * λ = taper ratio
        * t/c = thickness ratio
        * N_z = ultimate load factor
        * W_to = takeoff weight

    References
    ----------
    [1] Raymer, D. P. (2018). Aircraft design: A conceptual approach: A conceptual approach. 
        American Institute of Aeronautics and Astronautics Inc. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """
    # unpack inputs 
    W_0  = TOW / Units.lb # Convert kg to lbs
    S_w  = S_wing/ (Units.ft**2) # Convert from meters squared to ft squared  
    W_fw = m_fuel/Units.lbs #convert from kg to lbs
    q    = q_c /(Units.lbs/(Units.ft**2.))

    # Calculate weight of wing for traditional aircraft vertical tail without rudder
    weight_English = .036 * (S_w**.758)*(W_fw**.0035)*((AR_w/(np.cos(sweep_w)**2))**.6)*(q**.006)*(taper_w**.04)*((100.*t_c_w/np.cos(sweep_w))**(-.3))*((Nult*W_0)**.49)
    
    # packup outputs    
    weight =  weight_English * Units.lbs # Convert from lbs to kg

    return weight
