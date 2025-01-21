# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cylinder_moment_of_inertia.py 
# 
# Created:  Sept. 2024, A. Molloy  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cylinder Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cylinder_moment_of_inertia(origin, mass, length_outer, radius_outer, 
                                     length_inner=0, radius_inner=0, 
                                     center_of_gravity=np.array([[0,0,0]])):
    """
    Computes the moment of inertia tensor for a hollow cylinder about a specified reference point.

    Parameters
    ----------
    origin : array
        Location of cylinder center [m]
    mass : float
        Total mass of cylinder [kg]
    length_outer : float
        Outer length [m]
    radius_outer : float
        Outer radius [m]
    length_inner : float, optional
        Inner cavity length [m], default 0
    radius_inner : float, optional
        Inner cavity radius [m], default 0
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
    Computes the moment of inertia for both solid and hollow cylinders. For a solid cylinder,
    set inner length and radius to 0. Equations come from Moulton and Hunsaker [1].

    **Major Assumptions**
        * Uniform density throughout material
        * Cylinder axis aligned with x-axis
        * Inner cavity (if present) is centered and coaxial
        * Rigid body
        * Point mass approximation used when radius or length is zero

    **Theory**
    For a hollow cylinder, the moments of inertia about its center of mass are:
    .. math::
        I_{xx} = \\frac{\\rho}{2}\\pi(r_2^4L_2 - r_1^4L_1)

        I_{yy} = I_{zz} = \\frac{\\rho}{12}(3\\pi r_2^4L_2 + \\pi r_2^2L_2^3 
                                         - 3\\pi r_1^4L_1 - \\pi r_1^2L_1^3)

    where:
        * r₂ = outer radius
        * r₁ = inner radius
        * L₂ = outer length
        * L₁ = inner length
        * ρ = density

    References
    ----------
    [1] Moulton, B. C., and Hunsaker, D. F., "Simplified Mass and Inertial 
        Estimates for Aircraft with Components of Constant Density," AIAA 
        SCITECH 2023 Forum, January 2023, AIAA-2023-2432 
        DOI: 10.2514/6.2023-2432

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_aircraft_moment_of_inertia
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_cuboid_moment_of_inertia
    """
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Setup
    # ----------------------------------------------------------------------------------------------------------------------           
    I =  np.zeros((3, 3))
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Moment of inertia in local system. From Moulton and Hunsaker [1]
    # ----------------------------------------------------------------------------------------------------------------------
    
    # Avoid divide by zero error for a point mass
    if  (radius_outer == 0 or length_outer == 0):
        volume = 1
    else:
        volume = (np.pi * radius_outer ** 2 * length_outer - np.pi * radius_inner ** 2 * length_inner) 
    
    rho     = mass / volume
    I[0][0] = rho * (1 / 2 * np.pi * (radius_outer ** 4 * length_outer) - 1 / 2 * np.pi * (radius_inner ** 4 * length_inner)) # Ixx
    I[1][1] = rho * (1 / 12 * (3 *np.pi*(radius_outer ** 4)*length_outer + np.pi * radius_outer ** 2 * length_outer ** 2) - 1 / 12 * (3 * (radius_inner ** 4) *np.pi *length_inner + np.pi * radius_inner ** 2 * length_inner ** 2)) # Iyy
    I[2][2] = rho * (1 / 12 * (3 *np.pi*(radius_outer ** 4)*length_outer + np.pi * radius_outer ** 2 * length_outer ** 2) - 1 / 12 * (3 * (radius_inner ** 4) *np.pi *length_inner + np.pi * radius_inner ** 2 * length_inner ** 2)) # Izz
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s        = np.array(center_of_gravity) - np.array(origin) # Vector between component and the CG    
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    return I_global,  mass