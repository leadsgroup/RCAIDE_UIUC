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
    """
    Calculates the fuselage weight for transport aircraft using empirical correlation.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing:
            - mass_properties.max_zero_fuel : float
                Zero fuel weight [kg]
            - flight_envelope.positive_limit_load : float
                Positive limit load factor
            - wings.main_wing.chords.root : float
                Wing root chord [m]
    fuselage : RCAIDE.Component()
        Fuselage component containing:
            - differential_pressure : float
                Maximum cabin pressure differential [Pa]
            - width : float
                Maximum fuselage width [m]
            - heights.maximum : float
                Maximum fuselage height [m]
            - lengths.total : float
                Total fuselage length [m]
            - areas.wetted : float
                Wetted area [m^2]
    W_wing : float
        Weight of the wing [kg]
    W_propulsion : float
        Weight of the propulsion system [kg]

    Returns
    -------
    fuselage_weight : float
        Weight of the fuselage structure [kg]

    Notes
    -----
    This method estimates transport aircraft fuselage weight based on a correlation
    that accounts for pressure loads and bending loads separately.

    **Major Assumptions**
        * Standard tube and wing configuration
        * Pressurized cabin
        * Bending loads from wing and tail
        * Weight correlation based on transport category aircraft data

    **Theory**
    The fuselage weight is calculated by determining the dominant loading case
    between pressure and bending:
    .. math::
        I_p = 1.5 \\times 10^{-3} \\Delta p w

    .. math::
        I_b = 1.91 \\times 10^{-4} N W L/h^2

    The final weight index is:
    .. math::
        I_f = \\begin{cases} 
            I_p & \\text{if } I_p > I_b \\\\
            \\frac{I_p^2 + I_b^2}{2I_b} & \\text{otherwise}
        \\end{cases}

    The fuselage weight is then:
    .. math::
        W_{fus} = (1.051 + 0.102I_f)S_{wet}

    where:
        * :math:`\\Delta p` is cabin pressure differential
        * :math:`w` is fuselage width
        * :math:`N` is limit load factor
        * :math:`W` is zero fuel weight minus wing and propulsion
        * :math:`L` is fuselage length
        * :math:`h` is fuselage height
        * :math:`S_{wet}` is wetted area

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_operating_empty_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_wing_weight
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
