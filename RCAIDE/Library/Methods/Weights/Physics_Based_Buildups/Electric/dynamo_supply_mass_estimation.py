# dynamo_supply_mass_estimation.py
#
# Created:  Feb 2020,   K. Hamilton - Through New Zealand Ministry of Business Innovation and Employment Research Contract RTVU2004 
# Modified: Feb 2022,   S. Claridge 
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# import math
import numpy as np
import scipy.integrate as integrate

# ----------------------------------------------------------------------
#  Dynamo_Supply dynamo_supply_mass_estimation
# ----------------------------------------------------------------------      
def dynamo_supply_mass_estimation(HTS_Dynamo_Supply):
    """
    Estimates the mass of a High Temperature Superconducting (HTS) dynamo power supply system, including the electronic 
    speed controller (ESC), brushless motor, and gearbox.

    Parameters
    ----------
    HTS_Dynamo_Supply : Data()
        Data structure containing dynamo supply specifications
            - rated_power : float
                Rated power output of the dynamo supply [W]

    Returns
    -------
    mass : float
        Total mass of the dynamo supply system [kg]

    Notes
    -----
    The function computes component masses using empirical relationships:
    - Motor mass = 0.013 + 0.0046 * rated_power
    - Gearbox mass = 0.0109 + 0.0015 * rated_power
    - ESC mass = (5.0 + rated_power/50.0)/1000.0

    **Major Assumptions**
        * Mass scales linearly with power output
        * Based on Maxon EC-max 12V brushless motors under 100W
        * ESC mass scaling is an empirical estimate
        * Component relationships remain valid across power ranges

    **Extra modules required**
        * numpy
        * scipy.integrate

    References
    ----------
    [1] Maxon Motor drivetrain specifications and datasheets

    See Also
    --------
    RCAIDE.Library.Components.Propulsors.Converters.DC_Motor
    """

    # unpack
    rated_power     = HTS_Dynamo_Supply.rated_power

    # Estimate mass of motor and gearbox. Source: Maxon EC-max 12V brushless motors under 100W.
    mass_motor      = 0.013 + 0.0046 * rated_power
    mass_gearbox    = 0.0109 + 0.0015 * rated_power

    # Estimate mass of motor driver (ESC). Source: Estimate
    mass_esc        = (5.0 + rated_power/50.0)/1000.0

    # Sum masses to give total mass
    mass            = mass_esc + mass_motor + mass_gearbox

    # Store results
    HTS_Dynamo_Supply.mass_properties.mass       = mass

    # Return results
    return mass