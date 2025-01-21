# RCAIDE/Library/Methods/Weights/Correlation_Buildups/FLOPS/compute_payload_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core    import Units ,  Data
  
# ----------------------------------------------------------------------------------------------------------------------
#  Operating Items Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_payload_weight(vehicle, W_passenger=195*Units.lbs, W_baggage=30*Units.lbs):
    """
    Computes the total payload weight including passengers, baggage, and cargo using 
    FLOPS weight estimation method.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - passengers : int
                Number of passengers
            - mass_properties.cargo : float
                Mass of cargo [kg]
    W_passenger : float, optional
        Standard passenger weight including clothing [kg], default 195 lbs
    W_baggage : float, optional
        Standard baggage allowance per passenger [kg], default 30 lbs

    Returns
    -------
    output : Data
        Container with payload breakdown:
            - total : float
                Total payload weight [kg]
            - passengers : float
                Total passenger weight [kg]
            - baggage : float
                Total baggage weight [kg]
            - cargo : float
                Bulk cargo weight [kg]

    Notes
    -----
    Uses FAA standard weights for commercial operations.

    **Major Assumptions**
        * Variation in baggage allowance per passenger based on design range

    **Theory**
    Total payload weight is computed as:
    .. math::
        W_{payload} = n_{pax}(W_{pax} + W_{bag}) + W_{cargo}

    where:
        * n_pax = number of passengers
        * W_pax = standard passenger weight
        * W_bag = standard baggage allowance
        * W_cargo = bulk cargo weight

    References
    ----------
    [1] NASA Flight Optimization System (FLOPS)

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_operating_empty_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.FLOPS.compute_operating_items_weight
    """
    WPPASS  = W_passenger
    WPASS   = vehicle.passengers * WPPASS
    DESRNG  = vehicle.flight_envelope.design_range / Units.nmi
    if DESRNG <= 900:
        BPP = 35 * Units.lbs  # luggage weight per passenger depends on the design range
    elif DESRNG <= 2900:
        BPP = 40 * Units.lbs
    else:
        BPP = 44 * Units.lbs
    WPBAG       = BPP * vehicle.passengers  # baggage weight
    WPAYLOAD    = WPASS + WPBAG + vehicle.mass_properties.cargo / Units.lbs  # payload weight

    output              = Data()
    output.total        = WPAYLOAD
    output.passengers   = WPASS
    output.baggage      = WPBAG
    output.cargo        = vehicle.mass_properties.cargo
    return output
