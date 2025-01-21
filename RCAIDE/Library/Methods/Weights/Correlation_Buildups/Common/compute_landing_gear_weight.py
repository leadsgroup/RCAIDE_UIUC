# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Common/compute_landing_gear_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core import Data 

# ---------------------------------------------------------------------------------------------------------------------- 
# Landing Gear 
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_landing_gear_weight(vehicle, landing_gear_W_factor=0.04):
    """
    Computes the weight of the aircraft landing gear using a simple fraction of takeoff weight.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - mass_properties.max_takeoff : float
                Maximum takeoff weight [kg]
    landing_gear_W_factor : float, optional
        Landing gear weight as fraction of MTOW, default 0.04

    Returns
    -------
    output : Data
        Container with weight breakdown:
            - main : float
                Main landing gear weight [kg]
            - nose : float
                Nose landing gear weight [kg]

    Notes
    -----
    Uses a simple mass fraction approach common in preliminary design.
    Weight is split 90/10 between main and nose gear.

    **Major Assumptions**
        * Landing gear weight scales linearly with MTOW
        * Fixed weight distribution between main and nose gear

    **Theory**
    Total landing gear weight is computed as:
    .. math::
        W_{lg} = k_{lg} \\cdot MTOW

    where:
        * k_lg = landing gear weight factor (typically 0.04)
        * MTOW = maximum takeoff weight

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common.compute_operating_empty_weight
    """

    # process
    weight          = landing_gear_W_factor * vehicle.mass_properties.max_takeoff
    output          = Data()
    output.main     = weight * 0.9
    output.nose     = weight * 0.1
    return output
