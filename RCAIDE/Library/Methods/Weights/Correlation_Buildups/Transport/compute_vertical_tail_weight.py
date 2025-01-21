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
    """
    Calculate the weight of the vertical tail assembly including the vertical fin and rudder.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing vehicle properties
            - flight_envelope.ultimate_load : float
                Ultimate load factor of the aircraft
            - mass_properties.max_takeoff : float
                Maximum takeoff weight [kg]
            - reference_area : float
                Wing reference area [m²]
    wing : RCAIDE.Components.Wings.Vertical_Tail()
        Vertical tail data structure
            - spans.projected : float
                Projected span of the vertical tail [m]
            - thickness_to_chord : float
                Thickness-to-chord ratio of the vertical tail
            - sweeps.quarter_chord : float
                Quarter chord sweep angle [radians]
            - areas.reference : float
                Reference area of the vertical tail [m²]
            - t_tail : str
                Indicates if vertical tail is part of T-tail configuration ('yes' or 'no')
    rudder_fraction : float, optional
        Fraction of vertical tail area that is rudder (default 0.25)

    Returns
    -------
    tail_weight : float
        Total weight of vertical tail assembly [kg]

    Notes
    -----
    The function first calculates the weight of the vertical fin without the rudder, then adds
    the rudder weight based on the specified area fraction.

    **Major Assumptions**
        * Rudder occupies 25% of vertical tail area by default
        * Rudder weighs 60% more per unit area than the vertical fin
        * T-tail configuration adds 25% to vertical fin weight
    
    **Theory**
    The weight estimation uses an empirical correlation based on:
    .. math::
        W_{vert} = T_{factor} * (2.62 * S_{v} + 1.5 * 10^{-5} * N_{ult} * b_{v}^3 * 
        (8 + 0.44 * \\frac{W_{to}}{S_{ref}}) / (t/c * cos^2(\\Lambda)))

    where:
        - :math:`W_{vert}` = vertical tail weight
        - :math:`T_{factor}` = T-tail factor (1.25 or 1.0)
        - :math:`S_{v}` = vertical tail area
        - :math:`N_{ult}` = ultimate load factor
        - :math:`b_{v}` = vertical tail span
        - :math:`W_{to}` = takeoff weight
        - :math:`S_{ref}` = reference wing area
        - :math:`t/c` = thickness to chord ratio
        - :math:`\\Lambda` = quarter chord sweep angle

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Raymer.compute_vertical_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_vertical_tail_weight
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
