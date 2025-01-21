# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_fuselage_moment_of_inertia.py 
# 
# Created:  September 2024, A. Molloy  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORTS
# ---------------------------------------------------------------------------------------------------------------------- 
# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Fuselage Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_fuselage_moment_of_inertia(fuselage, center_of_gravity=[[0, 0, 0]]):
    """
    Computes the moment of inertia tensor for a generic fuselage by modeling it as a combination 
    of a hemisphere, cylinder, and cone.

    Parameters
    ----------
    fuselage : Fuselage
        The fuselage instance containing:
            - mass_properties.mass : float
                Total fuselage mass [kg]
            - effective_diameter : float
                Fuselage outer diameter [m]
            - lengths : Data
                Container with:
                    - total : float
                        Total fuselage length [m]
                    - nose : float
                        Nose section length [m]
                    - tail : float
                        Tail section length [m]
            - origin : array
                Fuselage reference point location [m]
    center_of_gravity : array, optional
        Reference point for moment of inertia calculation [m], default [0,0,0]

    Returns
    -------
    I_total : ndarray
        3x3 moment of inertia tensor about reference point [kg-m²]
    mass_fuselage : float
        Total fuselage mass [kg]

    Notes
    -----
    Models the fuselage as three sections, Nose: Hemisphere, Center: Cylinder, Tail: Cone. 

    **Major Assumptions**
        * Hollow structure with inner radius 85% of outer radius
        * Uniform density throughout
        * Axisymmetric about x-axis
        * Mass distributed according to volume fractions
        * Rigid body
        * Sections are perfectly joined

    **Theory**
    The total moment of inertia is the sum of component inertias:
    .. math::
        I_{total} = I_{hemisphere} + I_{cylinder} + I_{cone}

    Each component's contribution follows:
    .. math::
        I_{component} = I_{cm} + m(d^2\\delta_{ij} - d_id_j)

    where volume fractions determine mass distribution:
    .. math::
        m_{component} = m_{total}\\frac{V_{component}}{V_{total}}

    References
    ----------
    [1] Moulton, B. C., and Hunsaker, D. F., "Simplified Mass and Inertial 
        Estimates for Aircraft with Components of Constant Density," AIAA 
        SCITECH 2023 Forum, January 2023, AIAA-2023-2432 
        DOI: 10.2514/6.2023-2432
    [2] Weisstein, E. W., "Moment of Inertia -- Cone," Wolfram Research, N.D., 
        https://scienceworld.wolfram.com/physics/MomentofInertiaCone.html

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_aircraft_moment_of_inertia
    """
    
    # ----------------------------------------------------------------------------------------------------------------------   
    # Setup
    # ----------------------------------------------------------------------------------------------------------------------       
    mass_fuselage = 1 * fuselage.mass_properties.mass
    radius_outer  = fuselage.effective_diameter / 2
    radius_inner  = 0.85 * fuselage.effective_diameter / 2 # Assume the inner radius is 85 % of the outer radius    
    center_length = fuselage.lengths.total - fuselage.lengths.nose - fuselage.lengths.tail     # Length of the cylinder (found by subtracting the tail and nose lengths from the total length)
    
    I_total = np.zeros((3, 3)) # Initialize matrix to hold the entire fuselage inertia tensor
    
    # ---------------------------------------------------------------------------------------------------------------------- 
    # Calculate volume fraction of each section
    # ---------------------------------------------------------------------------------------------------------------------- 
    volume_fraction = Volume_Fraction(radius_outer, radius_inner, center_length, fuselage.lengths.tail) # output = [hemisphere, cylinder, cone]
    
    # ----------------------------------------------------------------------------------------------------------------------   
    # Hemisphere
    # ----------------------------------------------------------------------------------------------------------------------   
    origin_hemisphere = np.array([fuselage.lengths.nose, 0, 0]) + np.array(fuselage.origin)
    mass_hemisphere   = mass_fuselage * volume_fraction[0] # mass of the hemisphere
    I                 = np.zeros((3, 3)) # Local inertia tensor 
    
    # Moment of inertia in local system. From Weisstein [2]
    I[0][0] = 2 * mass_hemisphere / 5 *  (radius_outer ** 5 - radius_inner ** 5) /(radius_outer **3 -radius_inner **3) # Ixx
    I[1][1] = 2 * mass_hemisphere / 5 *  (radius_outer ** 5 - radius_inner ** 5) /(radius_outer **3 -radius_inner **3)# Iyy
    I[2][2] = 2 * mass_hemisphere / 5 *  (radius_outer ** 5 - radius_inner ** 5) /(radius_outer **3 -radius_inner **3) # Izz

    # global system
    s        = np.array(center_of_gravity) - np.array(origin_hemisphere)
    I_global = np.array(I) + mass_hemisphere * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s)) # global inertia tensor for hemisphere
    
    # Add hemisphere to the fuselage inertia tensor
    I_total  = np.array(I_total) + np.array(I_global)
    
    # ----------------------------------------------------------------------------------------------------------------------   
    # cylinder
    # ----------------------------------------------------------------------------------------------------------------------   
    mass_cylinder   = mass_fuselage * volume_fraction[1]
    origin_cylinder = np.array([fuselage.lengths.nose + center_length / 2,0, 0]) + np.array(fuselage.origin) # origin of the cylinder is located a the middle of the cylinder
    
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system. From Moulton and Hunsaker [1]
    I[0][0]  = mass_cylinder / 2 *  (radius_outer ** 2 + radius_inner ** 2) # Ixx
    I[1][1]  = mass_cylinder / 12 * (3 * (radius_outer ** 2 + radius_inner ** 2) + center_length ** 2) # Iyy
    I[2][2]  = mass_cylinder / 12 * (3 * (radius_outer ** 2 + radius_inner ** 2) + center_length ** 2) # Izz
      
    # transform moment of inertia to global system   
    s        = np.array(center_of_gravity) - np.array(origin_cylinder)
    I_global = np.array(I) + mass_cylinder * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    # Add cylinder to fuselage inertia matrix
    I_total = np.array(I_total) + np.array(I_global)

    # ----------------------------------------------------------------------------------------------------------------------   
    # cone
    # ----------------------------------------------------------------------------------------------------------------------   
    tail_length = fuselage.lengths.tail # length of the cone is defined to be the tail length.
    mass_cone   = mass_fuselage * volume_fraction[2]
    origin_cone = np.array([fuselage.lengths.total - fuselage.lengths.tail,0, 0]) + np.array(fuselage.origin)
    
    I =  np.zeros((3, 3))
  
    # Moment of inertia in local system. From Weisstein [2]. 
    rho     = (mass_cone / (1 / 3 * np.pi * (radius_outer ** 2 * center_length - radius_inner ** 2 * (center_length * radius_inner / radius_outer)))) # density of the cone. Mass divided by volume.
    I[0][0] = rho * (1 / 3 * np.pi * radius_outer ** 2 * tail_length ** 3 + np.pi / 20 * radius_outer ** 4 *tail_length - 1 / 3 * np.pi * radius_inner ** 2 * (tail_length * radius_inner / radius_outer) ** 3 + np.pi / 20 * radius_inner ** 4 *(tail_length * radius_inner / radius_outer))
    I[1][1] = rho * (1 / 3 * np.pi * radius_outer ** 2 * tail_length ** 3 + np.pi / 20 * radius_outer ** 4 *tail_length - 1 / 3 * np.pi * radius_inner ** 2 * (tail_length * radius_inner / radius_outer) ** 3 + np.pi / 20 * radius_inner ** 4 *(tail_length * radius_inner / radius_outer))
    I[2][2] = rho * (np.pi /10 *radius_outer **4 *tail_length -np.pi /10 *radius_inner **4 *(tail_length * radius_inner / radius_outer)) # Izz

    # transform moment of inertia to global system   
    s        = np.array(center_of_gravity) - np.array(origin_cone) # vector from the cone base to the center of gravity of the aircraft. 
    I_global = np.array(I) + mass_cone * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    # Add cone to the fuselage inertia tensor
    I_total = np.array(I_total) + np.array(I_global)
    
    return I_total,  mass_fuselage

def Volume_Fraction(radius_outer, radius_inner, center_length, tail_length):
    '''
    Calculate the volume fraction of each of the three components that make up the entire fuselage
    
    Assumptions:

    Source:

    Inputs:
    - Fuselage dimensions (radii, center length, tail length)

    Outputs:
    - Volume fraction of each fuselage component

    Properties Used:
    N/A
    '''
    # ----------------------------------------------------------------------------------------------------------------------    
    # Individual Component Volumes
    # ----------------------------------------------------------------------------------------------------------------------    
    
    volume_cone       = np.pi * radius_outer ** 2 * tail_length / 3 - np.pi * radius_inner ** 2 * (tail_length * radius_inner / radius_outer) / 3
    volume_hemisphere = 2 / 3 * np.pi * radius_outer ** 3 -2 / 3 * np.pi * radius_inner ** 3 
    volume_cylinder   = np.pi * center_length * (radius_outer ** 2 - radius_inner ** 2)
   
    # ----------------------------------------------------------------------------------------------------------------------    
    # Total Volume
    # ----------------------------------------------------------------------------------------------------------------------        
    volume_total = volume_cone + volume_hemisphere + volume_cylinder
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Volume Fractions
    # ----------------------------------------------------------------------------------------------------------------------        
    volume_fraction = np.array([volume_hemisphere / volume_total, volume_cylinder / volume_total, volume_cone / volume_total])
    
    return volume_fraction