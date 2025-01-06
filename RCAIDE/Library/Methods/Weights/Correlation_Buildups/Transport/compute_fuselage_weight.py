# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Transport/compute_fuselage_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core    import Units

# python imports 
 
# ----------------------------------------------------------------------------------------------------------------------
# fuselage Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_fuselage_weight(vehicle, fuselage, W_wing, W_propulsion):
    """ Calculate the weight of a fuselage in the state tube and wing configuration
    
    Assumptions:
        fuselage in a standard wing and tube configuration         
    
    Source: 
        N/A 
        
    Inputs:
        fuselage.areas.wetted - fuselage wetted area                                                            [meters**2]
        fuselage.differential_pressure- Maximum fuselage pressure differential                                  [Pascal]
        fuselage.width - width of the fuselage                                                                  [meters]
        fuselage.heights.maximum - height of the fuselage                                                       [meters]
        fuselage.lengths.total - length of the fuselage                                                         [meters]
        vehicle.flight_envelope.limit_load - limit load factor at zero fuel weight of the aircraft                 [dimensionless]
        vehicle.mass_properties.max_zero_fuel - zero fuel weight of the aircraft                            [kilograms]
        W_wing - weight of the wing of the aircraft                           [kilograms]
        W_propulsion - weight of the entire propulsion system of the aircraft                              [kilograms]
        vehicle.wings.main_wing.chords.root - wing root chord                                               [meters]
        
    Outputs:
        weight - weight of the fuselage                                                                     [kilograms]
            
    Properties Used:
        N/A
    """
    # unpack inputs

    differential_pressure  = fuselage.differential_pressure / (Units.force_pound / Units.ft ** 2)  # Convert Pascals to lbs/ square ft
    width                  = fuselage.width / Units.ft  # Convert meters to ft
    height                 = fuselage.heights.maximum / Units.ft  # Convert meters to ft

    # setup
    length  = fuselage.lengths.total - vehicle.wings.main_wing.chords.root / 2.
    length  = length / Units.ft  # Convert meters to ft
    weight  = (vehicle.mass_properties.max_zero_fuel - W_wing - W_propulsion) / Units.lb  # Convert kg to lbs
    area    = fuselage.areas.wetted / Units.ft ** 2  # Convert square meters to square ft

    # process

    # Calculate fuselage indices
    I_p = 1.5 * 10 ** -3. * differential_pressure * width
    I_b = 1.91 * 10 ** -4. * vehicle.flight_envelope.positive_limit_load* weight * length / height ** 2.

    if I_p > I_b:
        I_f = I_p
    else:
        I_f = (I_p ** 2. + I_b ** 2.) / (2. * I_b)

    # Calculate weight of wing for traditional aircraft vertical tail without rudder
    fuselage_weight = ((1.051 + 0.102 * I_f) * area) * Units.lb  # Convert from lbs to kg

    return fuselage_weight
