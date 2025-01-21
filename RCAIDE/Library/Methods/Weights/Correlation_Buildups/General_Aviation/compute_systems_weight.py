# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_systems_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
from RCAIDE.Framework.Core import  Units , Data 

# ----------------------------------------------------------------------------------------------------------------------
# Systems Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_systems_weight(W_uav, V_fuel, V_int, N_tank, N_eng, l_fuselage, span, TOW, Nult, num_seats, mach_number, has_air_conditioner=1):
    """
    Calculates the weight of various aircraft systems using empirical correlations for general aviation aircraft.

    Parameters
    ----------
    W_uav : float
        Weight of uninstalled avionics [kg]
    V_fuel : float
        Total fuel volume [m^3]
    V_int : float
        Internal fuel volume [m^3]
    N_tank : int
        Number of fuel tanks
    N_eng : int
        Number of engines
    l_fuselage : float
        Length of fuselage [m]
    span : float
        Wing span [m]
    TOW : float
        Maximum takeoff weight [kg]
    Nult : float
        Ultimate load factor
    num_seats : int
        Number of passenger seats
    mach_number : float
        Design cruise Mach number
    has_air_conditioner : int, optional
        Binary flag for air conditioning system (1=yes, 0=no), defaults to 1

    Returns
    -------
    output : Data()
        System weights breakdown
            - W_flight_control : float
                Flight control system weight [kg]
            - W_hyd_pnu : float
                Hydraulics and pneumatics weight [kg]
            - W_avionics : float
                Avionics system weight [kg]
            - W_electrical : float
                Electrical system weight [kg]
            - W_ac : float
                Air conditioning system weight [kg]
            - W_furnish : float
                Furnishings weight [kg]
            - W_fuel_system : float
                Fuel system weight [kg]
            - total : float
                Total systems weight [kg]

    Notes
    -----
    This method uses empirical correlations from Raymer to estimate the weight
    of various aircraft systems based on aircraft characteristics. Refer to 
    page 461 of the 4th edition of Raymer [1] for more details.

    **Major Assumptions**
        * Correlations are based on historical general aviation aircraft data
        * Systems are of conventional design and technology level

    **Theory**
    Key weight correlations used:
    .. math::
        W_{fuel\_sys} = 2.49(V_{tot}^{0.726})(\frac{V_{tot}}{V_{tot}+V_{int}})^{0.363}(N_{tank}^{0.242})(N_{eng}^{0.157})
    
    .. math::
        W_{flight\_ctrl} = 0.053(l_{fus}^{1.536})(b^{0.371})(N_{ult}W_{0}10^{-4})^{0.8}

    References
    ----------
    [1] Raymer, D. P. (2018). Aircraft design: A conceptual approach: A conceptual approach. 
        American Institute of Aeronautics and Astronautics Inc. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """
    # unpack inputs 
    Q_tot  = V_fuel/Units.gallons
    Q_int  = V_int/Units.gallons 
    l_fus  = l_fuselage / Units.ft  # Convert meters to ft
    b_wing = span/Units.ft 
    W_0    = TOW/Units.lb
    
    # Fuel system
    W_fuel_system = 2.49*(Q_tot**.726)*((Q_tot/(Q_tot+Q_int))**.363)*(N_tank**.242)*(N_eng**.157)*Units.lb

    # Flight controls
    W_flight_controls = .053*(l_fus**1.536)*(b_wing**.371)*((Nult*W_0**(10.**(-4.)))**.8)*Units.lb
    
    # Hydraulics & Pneumatics Group Wt
    hyd_pnu_wt = (.001*W_0) * Units.lb

    # Avionics weight
    W_avionics = 2.117*((W_uav/Units.lbs)**.933)*Units.lb 

    # Electrical Group Wt
    W_electrical = 12.57*((W_avionics/Units.lb + W_fuel_system/Units.lb)**.51)*Units.lb

    # Environmental Control 
    W_air_conditioning = has_air_conditioner*.265*(W_0**.52)*((1. * num_seats)**.68)*((W_avionics/Units.lb)**.17)*(mach_number**.08)*Units.lb

    # Furnishings Group Wt
    W_furnish = (.0582*W_0-65.)*Units.lb

    # packup outputs
    output = Data()   
    output.W_flight_control    = W_flight_controls
    output.W_hyd_pnu           = hyd_pnu_wt
    output.W_avionics          = W_avionics
    output.W_electrical        = W_electrical
    output.W_ac                = W_air_conditioning
    output.W_furnish           = W_furnish
    output.W_fuel_system       = W_fuel_system
    output.total               = output.W_flight_control + output.W_hyd_pnu \
                                  + output.W_ac + output.W_avionics + output.W_electrical \
                                  + output.W_furnish + output.W_fuel_system

    return output