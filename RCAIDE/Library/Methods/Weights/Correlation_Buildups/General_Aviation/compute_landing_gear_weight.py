# RCAIDE/Library/Methods/Weights/Correlation_Buildups/General_Aviation/compute_landing_gear_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units ,  Data  

# ----------------------------------------------------------------------------------------------------------------------
# Main Wing Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_landing_gear_weight(landing_weight, Nult, strut_length_main, strut_length_nose):
    """
    Computes landing gear weight for general aviation aircraft using Raymer's method.
    Includes both main and nose gear assemblies.

    Parameters
    ----------
    landing_weight : float
        Maximum landing weight [kg]
    Nult : float
        Ultimate load factor
    strut_length_main : float
        Main landing gear strut length [m]
    strut_length_nose : float
        Nose landing gear strut length [m]

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
    Uses Raymer's correlation developed for general aviation aircraft. Refer to Raymer, 
    page 460 (in the 4th edition) for more details.

    **Major Assumptions**
        * Conventional general aviation aircraft

    **Theory**
    Main gear weight is computed using:
    .. math::
        W_{main} = 0.095(N_zW_l)^{0.768}(L_m/12)^{0.409}

    Nose gear weight is computed using:
    .. math::
        W_{nose} = 0.125(N_zW_l)^{0.566}(L_n/12)^{0.845}

    where:
        * N_z = ultimate load factor
        * W_l = landing weight
        * L_m = main gear strut length
        * L_n = nose gear strut length

    References
    ----------
    [1] Raymer, D. P. (2018). Aircraft design: A conceptual approach: A conceptual approach. 
        American Institute of Aeronautics and Astronautics Inc. 
    
    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight
    """

    #unpack
    W_l = landing_weight/Units.lbs
    l_n = strut_length_nose/Units.inches
    l_m = strut_length_main/Units.inches
    main_weight = .095*((Nult*W_l)**.768)*(l_m/12.)**.409
    nose_weight = .125*((Nult*W_l)**.566)*(l_n/12.)**.845

    # pack outputs
    output      = Data()
    output.main = main_weight*Units.lbs
    output.nose = nose_weight*Units.lbs

    return output