# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_payload_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units ,  Data 

# ----------------------------------------------------------------------------------------------------------------------
# Payload Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_payload_weight(TOW, empty, num_pax, W_cargo, W_passenger = 225.*Units.lbs, W_baggage = 0.):
    """
    Calculates the total payload weight including passengers, baggage, and cargo.

    Parameters
    ----------
    TOW : float
        Maximum takeoff weight of the aircraft [kg]
    empty : float
        Operating empty weight of the aircraft [kg]
    num_pax : int
        Number of passengers
    W_cargo : float
        Weight of bulk cargo [kg]
    W_passenger : float, optional
        Weight per passenger [kg], defaults to 225 lbs converted to kg
    W_baggage : float, optional
        Weight of baggage per passenger [kg], defaults to 0 kg

    Returns
    -------
    output : Data()
        Payload weight breakdown
            - total : float
                Total payload weight (passengers + baggage + cargo) [kg]
            - passengers : float
                Total weight of all passengers [kg]
            - baggage : float
                Total weight of all passenger baggage [kg]
            - cargo : float
                Weight of bulk cargo [kg]

    Notes
    -----
    This method provides a simple calculation of payload weight components based on
    passenger count and per-passenger assumptions.

    **Major Assumptions**
        * All passengers are assumed to have the same weight
        * All passengers are assumed to have the same baggage weight
        * Cargo weight is treated as a bulk input separate from passenger effects

    **Theory**
    The total payload weight is calculated as:
    .. math::
        W_{payload} = n_{pax} * (W_{pax} + W_{bag}) + W_{cargo}

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """     

    # process
    W_pax     = W_passenger * num_pax 
    W_bag     = W_baggage * num_pax
    W_payload = W_pax + W_bag + W_cargo

    # packup outputs
    output = Data()
    output.total        = W_payload
    output.passengers   = W_pax
    output.baggage      = W_bag
    output.cargo        = W_cargo

    return output