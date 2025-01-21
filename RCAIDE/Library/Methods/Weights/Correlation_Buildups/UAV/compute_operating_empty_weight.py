# RCAIDE/Library/Methods/Weights/Correlation_Buildups/UAV/compute_operating_empty_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE
from RCAIDE.Framework.Core    import  Data  
 
 # ----------------------------------------------------------------------------------------------------------------------
# Compute Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle):
    """
    Computes the operating empty weight of a UAV using empirical correlations based on wing geometry.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle()
        Vehicle data structure containing vehicle properties
            - reference_area : float
                Aircraft reference area [m²]
            - wings : list
                List of wing components
                    - areas.reference : float
                        Wing reference area [m²]
                    - aspect_ratio : float
                        Wing aspect ratio

    Returns
    -------
    weight : Data()
        Weight breakdown data structure
            - empty : Data()
                Empty weight components
                    - total : float
                        Total empty weight [kg]

    Notes
    -----
    The function uses a correlation developed specifically for fixed-wing UAVs and sailplanes,
    based on a statistical analysis of 415 aircraft samples.

    **Major Assumptions**
        * Aircraft has at least one 'main wing' component
        * Correlation is valid for fixed-wing UAVs and sailplanes
        * Weight scales primarily with wing area and aspect ratio

    **Theory**
    The empty weight is calculated using:
    .. math::
        W_{airframe} = \\frac{5.58(S^{1.59})(AR^{0.71})}{g}

    where:
        - :math:`W_{airframe}` = airframe weight [kg]
        - :math:`S` = wing reference area [m²]
        - :math:`AR` = wing aspect ratio
        - :math:`g` = gravitational acceleration [m/s²]

    References
    ----------
    [1] Noth, A. (2008). Design of solar powered airplanes for continuous flight by andré Noth (thesis). 
        Design of solar powered airplanes for continuous flight by André Noth. ETH, Zürich. 
    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_operating_empty_weight
    """    
    # ----------------------------------------------------------------------------------------------------------------------
    # Unpack
    # ----------------------------------------------------------------------------------------------------------------------
    S     = vehicle.reference_area
    
    # ----------------------------------------------------------------------------------------------------------------------
    #  find max wing area and aspect ratio 
    # ----------------------------------------------------------------------------------------------------------------------    
    S_max = 0
    for wing in vehicle.wings:
        if S_max < wing.areas.reference:
            AR    = wing.aspect_ratio 
            S_max = wing.areas.reference 
        if isinstance(wing,RCAIDE.Library.Components.Wings.Main_Wing):
            AR = wing.aspect_ratio
            break 
            
    Earth = RCAIDE.Library.Attributes.Planets.Earth()
    g     = Earth.sea_level_gravity 
    
    # ----------------------------------------------------------------------------------------------------------------------
    # Airframe weight
    # ----------------------------------------------------------------------------------------------------------------------
    W_airframe   = (5.58*(S**1.59)*(AR**0.71))/g  
    
    # Pack
    weight              = Data()
    weight.empty        = Data()
    weight.empty.total  = W_airframe
    
    return weight