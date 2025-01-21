# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Raymer/compute_horizontal_tail_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE 
from RCAIDE.Framework.Core    import Units

# python imports 
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Horizontal Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_horizontal_tail_weight(vehicle, wing, elevator_fraction=0.4):
    """
    Calculates horizontal tail weight based on Raymer's empirical method.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - mass_properties.max_takeoff : float
                Maximum takeoff weight [kg]
            - flight_envelope.ultimate_load : float
                Ultimate load factor
            - wings['main_wing'] : Data()
                Main wing properties including origin and aerodynamic center
            - fuselages['fuselage'].width : float
                Width of the fuselage [m]
    wing : RCAIDE.Component()
        Horizontal tail component containing:
            - areas.reference : float
                Tail surface area [m^2]
            - origin : array
                Location of tail measured from nose [m]
            - aerodynamic_center : array
                Location of ac measured from leading edge [m]
            - sweeps.quarter_chord : float
                Quarter chord sweep angle [rad]
            - thickness_to_chord : float
                Thickness-to-chord ratio
            - spans.projected : float
                Projected span [m]
            - aspect_ratio : float
                Aspect ratio
    elevator_fraction : float, optional
        Fraction of horizontal tail area that is elevator, defaults to 0.4

    Returns
    -------
    tail_weight : float
        Weight of the horizontal tail [kg]

    Notes
    -----
    This method implements Raymer's correlation for horizontal tail weight estimation,
    accounting for geometry, loads, and configuration effects.

    **Major Assumptions**
        * Not an all-moving horizontal tail (Kuht = 1.0)
        * Elevator comprises 40% of tail area by default
        * Correlation based on transport category aircraft data

    **Theory**
    The horizontal tail weight is calculated using:
    .. math::
        W_{ht} = 0.0379K_{uht}(1 + \frac{F_w}{B_h})^{-0.25}W_{dg}^{0.639}N_{ult}^{0.1}S_{ht}^{0.75}L_t^{-1}K_y^{0.704}\cos(\Lambda)^{-1}AR^{0.166}(1 + \frac{S_e}{S_{ht}})^{0.1}

    where:
        * :math:`K_{uht}` is 1.0 for fixed tails, 1.143 for all-moving
        * :math:`F_w` is fuselage width
        * :math:`B_h` is horizontal tail span
        * :math:`L_t` is tail arm length
        * :math:`K_y` is a function of tail arm length
        * :math:`\Lambda` is quarter-chord sweep angle

    References
    ----------
    [1] Raymer, D., "Aircraft Design: A Conceptual Approach", AIAA 
        Education Series, 2018. 

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Raymer.compute_vertical_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Raymer.compute_operating_empty_weight
    """

    ref_wing = None 
    for wing in  vehicle.wings:
        if isinstance(wing, RCAIDE.Library.Components.Wings.Main_Wing):
            ref_wing  =  wing
    
    S = 0
    if ref_wing == None:
        for wing in  vehicle.wings:
            if S < wing.areas.reference:
                ref_wing = wing
    L_fuselage = 0
    for fuselage in vehicle.fuselages:
        if L_fuselage < fuselage.lengths.total:
            ref_fuselage = fuselage
            
    Kuht    = 1 # not a all-moving unit horizontal tail
    Fw      = ref_fuselage.width / Units.ft
    Bh      = wing.spans.projected / Units.ft
    DG      = vehicle.mass_properties.max_takeoff / Units.lbs
    Sht     = wing.areas.reference / Units.ft ** 2
    Lt      = (wing.origin[0][0] + wing.aerodynamic_center[0] - ref_wing.origin[0][0] -
                ref_wing.aerodynamic_center[0]) / Units.ft
    Ky      = 0.3 * Lt
    sweep   = wing.sweeps.quarter_chord
    Ah      = wing.aspect_ratio
    Se      = elevator_fraction * Sht

    tail_weight = 0.0379 * Kuht * (1 + Fw / Bh) ** (-0.25) * DG ** 0.639 *\
                  vehicle.flight_envelope.ultimate_load ** 0.1 * Sht ** 0.75 * Lt ** -1 *\
                  Ky ** 0.704 * np.cos(sweep) ** (-1) * Ah ** 0.166 * (1 + Se / Sht) ** 0.1
    return tail_weight * Units.lbs
