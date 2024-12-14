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
    """ Calculate the weight of the different engine systems on the aircraft

    Assumptions:
        numbers based on FAA regulations and correlations from previous aircraft

    Source:
        http://aerodesign.stanford.edu/aircraftdesign/structures/componentweight.html

   Inputs:
       vehicle.passengers - total number of seats on the aircraft                                     [dimensionless]
       vehicle.systems.control - specifies if the control system is fully power,
                                    partially powered, or not powered                                 [dimensionless]
       wing.areas.reference - area of the horizontal tail                                             [meters**2]
       wing.areas.reference - area of the vertical tail                                               [meters**2]
       vehicle.reference_area - area of the wing                                                      [meters**2]
       vehicle.systems.accessories - determines type of instruments, electronics,
                                        and operating items based on type of vehicle                  [dimensionless]

   Outputs:
       output - a data dictionary with fields:
           W_flight_controls - weight of the flight control system                                               [kilograms]
           W_apu - weight of the apu                                                                      [kilograms]
           W_hyd_pnu - weight of the hydraulics and pneumatics                                            [kilograms]
           W_instruments - weight of the instruments and navigational equipment                           [kilograms]
           W_avionics - weight of the avionics                                                            [kilograms]
           W_opitems - weight of the optional items based on the type of aircraft                         [kilograms]
           W_electrical - weight of the electrical items                                                        [kilograms]
           W_ac - weight of the air conditioning and anti-ice system                                      [kilograms]
           W_furnish - weight of the furnishings in the fuselage                                          [kilograms]

    Properties Used:
        N/A
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
