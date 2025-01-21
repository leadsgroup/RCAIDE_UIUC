# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Common/operating_empty_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_operating_empty_weight as compute_operating_empty_weight_transport

# ---------------------------------------------------------------------------------------------------------------------- 
# Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle, settings=None, method_type='RCAIDE'):
    """
    Computes the operating empty weight for a general aircraft using component-based 
    weight estimation methods. Serves as a dispatcher to configuration-specific methods.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing all aircraft configuration and component data
    settings : Data, optional
        Configuration settings with:
            - use_max_fuel_weight : bool
                Flag to use maximum fuel capacity
    method_type : str, optional
        Weight estimation methodology to use, default 'RCAIDE'
        Options include:
            - 'RCAIDE': Default RCAIDE methods
            - 'Transport': Transport aircraft methods
            - 'General_Aviation': GA aircraft methods
            - 'BWB': Blended wing body methods

    Returns
    -------
    output : Data
        Container with weight breakdowns:
            - empty : Data
                Structural, propulsion, and systems weights
            - payload : Data
                Passenger, baggage, and cargo weights
            - fuel : float
                Total fuel weight [kg]
            - zero_fuel_weight : float
                Operating empty weight plus payload [kg]
            - total : float
                Total aircraft weight [kg]

    Notes
    -----
    Acts as a high-level dispatcher that routes weight calculation to the generic transport method.

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_operating_empty_weight
    """
    output =  compute_operating_empty_weight_transport(vehicle,settings,method_type) 

    return output
