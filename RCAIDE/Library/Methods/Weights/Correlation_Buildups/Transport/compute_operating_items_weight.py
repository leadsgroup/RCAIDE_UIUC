# RCAIDE/Library/Methods/Weights/Correlation_Buildups/FLOPS/compute_operating_items_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core    import Units ,  Data

# python imports 
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Operating Items Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_items_weight(vehicle):
    """
    Calculate the weight of operating items for a transport aircraft, including crew, baggage, unusable 
    fuel, engine oil, passenger service items, and cargo containers.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing vehicle properties
            - passengers : int
                Number of passengers
            - systems.accessories : str
                Type of aircraft. Options:
                    - 'short-range': Short-range domestic with austere accommodations
                    - 'medium-range': Medium-range domestic
                    - 'long-range': Long-range overwater
                    - 'business': Business jet
                    - 'cargo': All cargo
                    - 'commuter': Commuter aircraft
                    - 'sst': Supersonic transport

    Returns
    -------
    output : Data()
        Operating items weight breakdown
            - misc : float
                Weight of unusable fuel, engine oil, passenger service items and cargo containers [kg]
            - flight_crew : float
                Weight of flight crew including their baggage [kg]
            - flight_attendants : float
                Weight of flight attendants including their baggage [kg]
            - total : float
                Total operating items weight [kg]

    Notes
    -----
    Flight crew sizing:
        * 2 crew members for aircraft < 150 passengers
        * 3 crew members for aircraft >= 150 passengers

    Flight attendant sizing:
        * 1 attendant for aircraft < 51 passengers
        * 1 + floor(passengers/40) for aircraft >= 51 passengers

    **Major Assumptions**
        * Flight crew weight: 190 lbs per person + 50 lbs baggage
        * Flight attendant weight: 170 lbs per person + 40 lbs baggage
        * Operating items weight varies by aircraft type per passenger

    References
    ----------
    [1] Stanford Aircraft Design Course, "Aircraft Weight Estimation", http://aerodesign.stanford.edu/aircraftdesign/AircraftDesign.html

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_operating_items_weight
    """
    num_seats   = vehicle.passengers
    ac_type     = vehicle.systems.accessories
    if ac_type   == "short-range":  # short-range domestic, austere accomodations
        operitems_wt = 17.0 * num_seats * Units.lb
    elif ac_type == "medium-range":  # medium-range domestic
        operitems_wt = 28.0 * num_seats * Units.lb
    elif ac_type == "long-range":  # long-range overwater
        operitems_wt = 28.0 * num_seats * Units.lb
    elif ac_type == "business":  # business jet
        operitems_wt = 28.0 * num_seats * Units.lb
    elif ac_type == "cargo":  # all cargo
        operitems_wt = 56.0 * Units.lb
    elif ac_type == "commuter":  # commuter
        operitems_wt = 17.0 * num_seats * Units.lb
    elif ac_type == "sst":  # sst
        operitems_wt = 40.0 * num_seats * Units.lb
    else:
        operitems_wt = 28.0 * num_seats * Units.lb

    if vehicle.passengers >= 150:
        flight_crew = 3  # FLOPS: NFLCR
    else:
        flight_crew = 2

    if vehicle.passengers < 51:
        flight_attendants = 1  # FLOPS: NSTU
    else:
        flight_attendants = 1 + np.floor(vehicle.passengers / 40.)

    W_flight_attendants = flight_attendants * (170 + 40)  # FLOPS: WSTUAB
    W_flight_crew = flight_crew * (190 + 50)  # FLOPS: WFLCRB

    output                           = Data()
    output.misc = operitems_wt
    output.flight_crew               = W_flight_crew * Units.lbs
    output.flight_attendants         = W_flight_attendants * Units.lbs
    output.total                     = output.misc + output.flight_crew + \
                                       output.flight_attendants
    return output
