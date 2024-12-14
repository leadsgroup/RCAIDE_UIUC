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
def compute_systems_weight(W_uav, V_fuel, V_int, N_tank, N_eng, l_fuselage, span, TOW, Nult, num_seats,  mach_number, has_air_conditioner=1):
    """ output = RCAIDE.Methods.Weights.Correlations.General_Avation.systems(num_seats, ctrl_type, S_h, S_v, S_gross_w, ac_type)
        Calculate the weight of the different engine systems on the aircraft

        Source:
            Raymer, Aircraft Design: A Conceptual Approach (pg 461 in 4th edition)

        Inputs:
            V_fuel              - total fuel volume                     [meters**3]
            V_int               - internal fuel volume                  [meters**3]
            N_tank              - number of fuel tanks                  [dimensionless]
            N_eng               - number of engines                     [dimensionless]
            span                - wingspan                              [meters]
            TOW                 - gross takeoff weight of the aircraft  [kg]
            num_seats           - total number of seats on the aircraft [dimensionless]
            mach_number         - mach number                           [dimensionless]
            has_air_conditioner - integer of 1 if the vehicle has ac, 0 if not

        Outputs:
            output - a data dictionary with fields:
                W_flight_controls - weight of the flight control system [kilograms]
                W_apu - weight of the apu [kilograms]
                W_hyd_pnu - weight of the hydraulics and pneumatics [kilograms]
                W_avionics - weight of the avionics [kilograms]
                W_opitems - weight of the optional items based on the type of aircraft [kilograms]
                W_electrical - weight of the electrical items [kilograms]
                W_ac - weight of the air conditioning and anti-ice system [kilograms]
                W_furnish - weight of the furnishings in the fuselage [kilograms]
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