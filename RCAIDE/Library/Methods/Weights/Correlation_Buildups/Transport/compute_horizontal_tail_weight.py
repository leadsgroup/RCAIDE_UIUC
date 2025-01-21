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
    """ 
    Calculates horizontal tail weight for transport aircraft using empirical correlation.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - mass_properties.max_takeoff : float
                Maximum takeoff weight [kg]
            - flight_envelope.ultimate_load : float
                Ultimate load factor
            - wings['main_wing'] : Data()
                Main wing properties:
                    - origin : array
                        Root location [m]
                    - aerodynamic_center : array
                        Location of aerodynamic center [m]
    wing : RCAIDE.Component()
        Horizontal tail component containing:
            - spans.projected : float
                Projected span [m]
            - sweeps.quarter_chord : float
                Quarter chord sweep angle [rad]
            - areas.reference : float
                Reference area [m^2]
            - areas.exposed : float
                Exposed area [m^2]
            - areas.wetted : float
                Wetted area [m^2]
            - thickness_to_chord : float
                Thickness-to-chord ratio
            - origin : array
                Root location [m]
            - aerodynamic_center : array
                Location of aerodynamic center [m]

    Returns
    -------
    weight : float
        Weight of the horizontal tail [kg]

    Notes
    -----
    This method implements an empirical correlation for transport aircraft horizontal
    tail weight estimation, accounting for geometry, loads, and configuration effects.

    **Major Assumptions**
        * Elevator comprises approximately 25% of tail area
        * Correlation based on transport category aircraft data
        * Elevator is included in the weight

    **Theory**
    The horizontal tail weight is calculated using:
    .. math::
        W_{ht} = 5.25S_{ht} + 0.8 \\times 10^{-6}N_{ult}b_{ht}^3W_{to}\\bar{c}_w
        \\sqrt{\\frac{S_{exp}}{S_{ht}}} \\left(\\frac{1}{(t/c)\\cos^2\\Lambda L_{ht}S_{ht}^{1.5}}\\right)

    where:
        * :math:`S_{ht}` is horizontal tail area
        * :math:`N_{ult}` is ultimate load factor
        * :math:`b_{ht}` is tail span
        * :math:`W_{to}` is takeoff weight
        * :math:`\\bar{c}_w` is wing mean chord
        * :math:`S_{exp}` is exposed tail area
        * :math:`t/c` is thickness ratio
        * :math:`\\Lambda` is quarter-chord sweep
        * :math:`L_{ht}` is tail arm length

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_vertical_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_operating_empty_weight
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
