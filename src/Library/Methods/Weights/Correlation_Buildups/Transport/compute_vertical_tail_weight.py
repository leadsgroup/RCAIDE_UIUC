# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Raymer/compute_vertical_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core    import Units

# python imports 
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Vertical Tail Weight 
# ---------------------------------------------------------------------------------------------------------------------
def compute_vertical_tail_weight(vehicle, wing, rudder_fraction=0.25):
    """ Calculate the weight of the vertical fin of an aircraft without the weight of 
    the rudder and then calculate the weight of the rudder 
    
    Assumptions:
        Vertical tail weight is the weight of the vertical fin without the rudder weight.
        Rudder occupies 25% of the S_v and weighs 60% more per unit area.     
        
    Source: 
        N/A 
        
    Inputs:
        S_v - area of the vertical tail (combined fin and rudder)                      [meters**2]
        vehicle.flight_envelope.ultimate_load - ultimate load of the aircraft                 [dimensionless]
        wing.spans.projected - span of the vertical                                    [meters]
        vehicle.mass_properties.max_takeoff - maximum takeoff weight of the aircraft   [kilograms]
        wing.thickness_to_chord- thickness-to-chord ratio of the vertical tail         [dimensionless]
        wing.sweeps.quarter_chord - sweep angle of the vertical tail                   [radians]
        vehicle.reference_area - wing gross area                                       [meters**2]
        wing.t_tail - factor to determine if aircraft has a t-tail                     [dimensionless]
        rudder_fraction - fraction of the vertical tail that is the rudder             [dimensionless]
    
    Outputs:
        output - a dictionary with outputs:
            W_tail_vertical - weight of the vertical fin portion of the vertical tail [kilograms]
            W_rudder - weight of the rudder on the aircraft                           [kilograms]
  
    Properties Used:
        N/A
    """
    # unpack inputs
    span                   = wing.spans.projected / Units.ft  # Convert meters to ft
    sweep                  = wing.sweeps.quarter_chord  # Convert deg to radians
    area                   = wing.areas.reference / Units.ft ** 2  # Convert meters squared to ft squared
    mtow                   = vehicle.mass_properties.max_takeoff / Units.lb  # Convert kg to lbs
    Sref                   = vehicle.reference_area / Units.ft ** 2  # Convert from meters squared to ft squared
    thickness_to_chord_v   = wing.thickness_to_chord
    # Determine weight of the vertical portion of the tail
    if wing.t_tail == "yes":
        T_tail_factor = 1.25  # Weight of vertical portion of the T-tail is 25% more than a conventional tail
    else:
        T_tail_factor = 1.0

        # Calculate weight of wing for traditional aircraft vertical tail without rudder
    tail_vert_English = T_tail_factor * (
                2.62 * area + 1.5 * 10. ** (-5.) * vehicle.flight_envelope.ultimate_load * span ** 3. * (8. + 0.44 * mtow / Sref) / (
                    thickness_to_chord_v * (np.cos(sweep) ** 2.)))

    tail_weight  = tail_vert_English * Units.lbs
    tail_weight += tail_weight * rudder_fraction * 1.6

    return tail_weight
