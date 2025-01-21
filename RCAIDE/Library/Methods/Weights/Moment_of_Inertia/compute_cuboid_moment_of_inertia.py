# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cuboid_moment_of_inertia.py 
# 
# Created:  September 2024, A. Molloy  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cuboid Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cuboid_moment_of_inertia(origin, mass, length_outer, width_outer, height_outer, 
                                   length_inner=0, width_inner=0, height_inner=0, 
                                   center_of_gravity=np.array([[0,0,0]])):
    """
    Computes the moment of inertia tensor for a hollow cuboid about a specified reference point.

    Parameters
    ----------
    origin : array
        Location of cuboid center [m]
    mass : float
        Total mass of cuboid [kg]
    length_outer : float
        Outer length (x-direction) [m]
    width_outer : float
        Outer width (y-direction) [m]
    height_outer : float
        Outer height (z-direction) [m]
    length_inner : float, optional
        Inner cavity length [m], default 0
    width_inner : float, optional
        Inner cavity width [m], default 0
    height_inner : float, optional
        Inner cavity height [m], default 0
    center_of_gravity : array, optional
        Reference point for moment of inertia calculation [m], default [0,0,0]

    Returns
    -------
    I_global : ndarray
        3x3 moment of inertia tensor about reference point [kg-m²]
    mass : float
        Input mass returned for consistency [kg]

    Notes
    -----
    Computes the moment of inertia for both solid and hollow cuboids. For a solid cuboid,
    set all inner dimensions to 0. Equations come from Moulton and Hunsaker [1].

    **Major Assumptions**
        * Uniform density throughout material
        * Cuboid aligned with coordinate axes
            - Length along x-axis
            - Width along y-axis
            - Height along z-axis
        * Inner cavity (if present) is centered
        * Rigid body
           - Cuboid has a constant density

    **Theory**
    For a hollow cuboid, the moment of inertia about its center of mass is:
    .. math::
        I_{xx} = \\frac{m}{12} \\frac{V_2(w_2^2 + h_2^2) - V_1(w_1^2 + h_1^2)}{V_2 - V_1}

    where:
        * V₂ = outer volume
        * V₁ = inner volume
        * w = width
        * h = height
        * Subscript 1 = inner
        * Subscript 2 = outer

    References
    ----------
    [1] Moulton, B. C., and Hunsaker, D. F., "Simplified Mass and Inertial 
        Estimates for Aircraft with Components of Constant Density," AIAA 
        SCITECH 2023 Forum, January 2023, AIAA-2023-2432 
        DOI: 10.2514/6.2023-2432

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_aircraft_moment_of_inertia
    """
    # ----------------------------------------------------------------------------------------------------------------------    
    # Setup
    # ----------------------------------------------------------------------------------------------------------------------
    I = np.zeros((3, 3)) 
    
    # calcualte volumes
    V2 = length_outer * width_outer * height_outer # Outer volume
    V1 = length_inner * width_inner * height_inner # Inner volume
    
    if  V2 == 0 and V1 == 0:
        temp = 0.000001 # Assigns an arbitrary value to avoid a divide by zero error. This will not affect results as V2 and V1 will be 0
        # Treats object as a point mass
    else:
        temp = (V2 - V1)
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Calculate inertia tensor. Equations from Moulton adn Hunsaker [1]
    # ----------------------------------------------------------------------------------------------------------------------    
    I[0][0] = mass / 12 * (V2 * (width_outer ** 2 + height_outer ** 2) - V1 * (width_inner ** 2 + height_inner ** 2)) / temp
    I[1][1] = mass / 12 * (V2 * (length_outer ** 2 + height_outer ** 2) - V1 * (length_inner ** 2 + height_inner ** 2)) / temp
    I[2][2] = mass / 12 * (V2 * (length_outer ** 2 + width_outer ** 2) - V1 * (length_inner ** 2 + width_inner ** 2)) / temp
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s        = np.array(center_of_gravity) - np.array(origin) # Vector between component and the CG
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    return I_global,  mass