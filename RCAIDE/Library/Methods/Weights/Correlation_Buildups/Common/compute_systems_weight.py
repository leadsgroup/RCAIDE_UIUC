# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Common/compute_systems_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Framework.Core import Data, Units
import RCAIDE.Library.Components.Wings as Wings 

# ---------------------------------------------------------------------------------------------------------------------- 
# Payload
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_systems_weight(vehicle):
    """
    Computes the weight of aircraft systems using empirical correlations based on 
    aircraft type and size.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - passengers : int
                Total number of seats
            - systems.control : str
                Control system type ('fully powered', 'partially powered', or 'unpowered')
            - systems.accessories : str
                Aircraft type ('short-range', 'medium-range', 'long-range', 'business', 
                'cargo', 'commuter', 'sst')
            - reference_area : float
                Wing reference area [m²]
            - wings : list
                Wing surfaces for control surface area calculation

    Returns
    -------
    output : Data
        Container with systems weight breakdown:
            - W_flight_control : float
                Flight control system weight [kg]
            - W_apu : float
                APU system weight [kg]
            - W_hyd_pnu : float
                Hydraulics and pneumatics weight [kg]
            - W_instruments : float
                Instruments weight [kg]
            - W_avionics : float
                Avionics weight [kg]
            - W_electrical : float
                Electrical system weight [kg]
            - W_ac : float
                Air conditioning weight [kg]
            - W_furnish : float
                Furnishings weight [kg]
            - W_anti_ice : float
                Anti-ice system weight [kg]
            - W_systems : float
                Total systems weight [kg]

    Notes
    -----
    Uses correlations developed from historical aircraft data, adjusted for 
    aircraft type and systems complexity along with FAA regulations.

    **Major Assumptions**
        * Systems complexity scales with aircraft size
        * Standard system architectures for each aircraft type
        * Similar technology levels across systems
        * Control surface area proportional to tail area
        * APU requirements based on passenger count
        * Environmental control sized for passenger count

    References
    ----------
    [1] http://aerodesign.stanford.edu/aircraftdesign/structures/componentweight.html

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common.compute_operating_empty_weight
    """ 
    num_seats   = vehicle.passengers
    ctrl_type   = vehicle.systems.control
    ac_type     = vehicle.systems.accessories
    S_gross_w   = vehicle.reference_area
    sref        = S_gross_w / Units.ft ** 2  # Convert meters squared to ft squared
    s_tail      = 0
    for wing in vehicle.wings:
        if isinstance(wing, Wings.Horizontal_Tail) or isinstance(wing, Wings.Vertical_Tail):
            s_tail += wing.areas.reference
    if s_tail == 0: # assume flight control only on wing, for example on a BWB
        for wing in vehicle.wings:
            if isinstance(wing, Wings.Main_Wing):
                s_tail += wing.areas.reference * 0.01
    area_hv = s_tail / Units.ft ** 2  # Convert meters squared to ft squared
 
    # Flight Controls Group Wt
    if ctrl_type == "fully powered":  # fully powered controls
        flt_ctrl_scaler = 3.5
    elif ctrl_type == "partially powered":  # partially powered controls
        flt_ctrl_scaler = 2.5
    else:
        flt_ctrl_scaler = 1.7  # fully aerodynamic controls
    W_flight_controls = (flt_ctrl_scaler * (area_hv)) * Units.lb

    # APU Group Wt
    if num_seats >= 6.:
        apu_wt = 7.0 * num_seats * Units.lb
    else:
        apu_wt = 0.0 * Units.lb  # no apu if less than 9 seats
    apu_wt = max(apu_wt, 70.)
    
    # Hydraulics & Pneumatics Group Wt
    hyd_pnu_wt = (0.65 * sref) * Units.lb

    # Electrical Group Wt
    W_electrical = (13.0 * num_seats) * Units.lb

    # Furnishings Group Wt
    W_furnish = ((43.7 - 0.037 * min(num_seats, 300.)) * num_seats + 46.0 * num_seats) * Units.lb

    # Environmental Control
    W_air_conditioning = (15.0 * num_seats) * Units.lb

    # Instruments, Electronics, Operating Items based on Type of Vehicle 
    if ac_type == "short-range":  # short-range domestic, austere accomodations
        W_instruments = 800.0 * Units.lb
        W_avionics = 900.0 * Units.lb
    elif ac_type == "medium-range":  # medium-range domestic
        W_instruments = 800.0 * Units.lb
        W_avionics = 900.0 * Units.lb
    elif ac_type == "long-range":  # long-range overwater
        W_instruments = 1200.0 * Units.lb
        W_avionics = 1500.0 * Units.lb
        W_furnish += 23.0 * num_seats * Units.lb  # add aditional seat wt
    elif ac_type == "business":  # business jet
        W_instruments = 100.0 * Units.lb
        W_avionics = 300.0 * Units.lb
    elif ac_type == "cargo":  # all cargo
        W_instruments = 800.0 * Units.lb
        W_avionics = 900.0 * Units.lb
        W_electrical = 1950.0 * Units.lb  # for cargo a/c
    elif ac_type == "commuter":  # commuter
        W_instruments = 300.0 * Units.lb
        W_avionics = 500.0 * Units.lb
    elif ac_type == "sst":  # sst
        W_instruments = 1200.0 * Units.lb
        W_avionics = 1500.0 * Units.lb
        W_furnish += 23.0 * num_seats * Units.lb  # add aditional seat wt
    else:
        W_instruments = 800.0 * Units.lb
        W_avionics = 900.0 * Units.lb 

    # packup outputs
    output = Data()
    output.W_flight_control    = W_flight_controls
    output.W_apu               = apu_wt
    output.W_hyd_pnu           = hyd_pnu_wt
    output.W_instruments       = W_instruments
    output.W_avionics          = W_avionics
    output.W_electrical        = W_electrical
    output.W_ac                = W_air_conditioning
    output.W_furnish           = W_furnish
    output.W_anti_ice          = 0 # included in AC
    output.W_systems           = output.W_flight_control + output.W_apu + output.W_hyd_pnu \
                                + output.W_ac + output.W_avionics + output.W_electrical \
                                + output.W_furnish + output.W_instruments

    return output
