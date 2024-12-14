# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Transport/compute_horizontal_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core    import Units
import numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Horizontal Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_horizontal_tail_weight(vehicle, wing):
    """ Calculate the weight of the horizontal tail in a standard configuration
    
    Assumptions:
        calculated weight of the horizontal tail including the elevator
        Assume that the elevator is 25% of the horizontal tail 
    
    Source: 
        Aircraft Design: A Conceptual Approach by Raymer
        
    Inputs:
        wing.spans.projected - span of the horizontal tail                                              [meters]
        wing.sweeps.quarter_chord - sweep of the horizontal tail                                        [radians]
        Nult - ultimate design load of the aircraft                                                     [dimensionless]
        S_h - area of the horizontal tail                                                               [meters**2]
        vehicle.mass_properties.max_takeoff - maximum takeoff weight of the aircraft                    [kilograms]
        vehicle.wings['main_wing'].origin[0] - mean aerodynamic chord of the wing                       [meters]
        wing.aerodynamic_center[0]  - mean aerodynamic chord of the horizontal tail                     [meters]
        wing.thickness_to_chord  - thickness-to-chord ratio of the horizontal tail                      [dimensionless]
        wing.areas.exposed - exposed surface area for the horizontal tail                               [m^2]
        wing.areas.wetted - wetted surface area of tail
    
    Outputs:
        weight - weight of the horizontal tail                                                          [kilograms]
       
    Properties Used:
        N/A
    """
    # unpack inputs
    span       = wing.spans.projected / Units.ft  # Convert meters to ft
    sweep      = wing.sweeps.quarter_chord
    area       = wing.areas.reference / Units.ft ** 2  # Convert meters squared to ft squared
    mtow       = vehicle.mass_properties.max_takeoff / Units.lb  # Convert kg to lbs
    exposed    = wing.areas.exposed / wing.areas.wetted
    
    # Compute length between the main wing's aerodynamic center and the horizontal tail
    l_w2h      = np.array([wing.origin[0][0] + wing.aerodynamic_center[0] - vehicle.wings['main_wing'].origin[0][0] -  vehicle.wings['main_wing'].aerodynamic_center[0]])
    l_w        = np.array([vehicle.wings['main_wing'].chords.mean_aerodynamic / Units.ft])   # Convert from meters to ft
    length_w_h = l_w2h / Units.ft  # Distance from mean aerodynamic center of wing to mean aerodynamic center of
     
    # Calculate weight of wing for traditional aircraft horizontal tail
    weight_English = 5.25 * area + 0.8 * 10. ** -6 * vehicle.flight_envelope.ultimate_load * span ** 3. * mtow * l_w *\
                     np.sqrt(exposed * area) / (wing.thickness_to_chord * (np.cos(sweep) ** 2.) * length_w_h * area ** 1.5)

    weight = weight_English * Units.lbs  # Convert from lbs to kg

    return weight
