# RCAIDE/Library/Methods/Weights/Buildups/Common/compute_boom_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute boom weight
# ----------------------------------------------------------------------------------------------------------------------
def compute_boom_weight(boom,
             maximum_g_load = 3.8,
             safety_factor = 1.5):
    """
    Calculates the structural mass of a cylindrical boom for an aircraft using material properties 
    and basic geometry.

    Parameters
    ----------
    boom : RCAIDE.Components.Booms.Boom()
        Boom data structure
            - lengths.total : float
                Total length of the boom [m]
            - heights.maximum : float
                Maximum height/diameter of the boom [m]
    maximum_g_load : float, optional
        Maximum load factor the boom must withstand (default 3.8)
    safety_factor : float, optional
        Design safety factor (default 1.5)

    Returns
    -------
    weight : float
        Estimated boom mass [kg]

    Notes
    -----
    The function calculates boom weight based on wetted surface area and material thickness.

    **Major Assumptions**
        * Boom is a hollow cylinder
        * Uniform material thickness of 1 cm
        * Uses carbon fiber with density of 1759 kg/m³
        * Uniform material properties throughout the boom
        * No stress concentrations or joints considered
    
    **Theory**
    Weight is calculated using:
    .. math::
        W = \\rho * t * (2\\pi * \\frac{d}{2} * L + 2\\pi * (\\frac{d}{2})^2)

    where:
        - :math:`\\rho` = material density
        - :math:`t` = wall thickness
        - :math:`d` = boom diameter
        - :math:`L` = boom length

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common.compute_fuselage_weight
    """

    #-------------------------------------------------------------------------------
    # Unpack Inputs
    #------------------------------------------------------------------------------- 
    bLength = boom.lengths.total
    bHeight = boom.heights.maximum 

    #-------------------------------------------------------------------------------
    # Unpack Material Properties
    #-------------------------------------------------------------------------------   
    density     = 1759   # a typical density of carbon fiber is 
    thickness   = 0.01  # thicness of boom is 1 cm

    # Calculate boom area assuming it is a hollow cylinder
    S_wet  = 2* np.pi* (bHeight/2) *bLength + 2*np.pi*(bHeight/2)**2
    weight = S_wet *thickness* density 
    
    return weight