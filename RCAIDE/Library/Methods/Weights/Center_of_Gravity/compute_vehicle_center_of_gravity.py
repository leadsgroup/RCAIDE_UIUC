# RCAIDE/Methods/Stability/Center_of_Gravity/compute_vehicle_center_of_gravity.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports   
from RCAIDE.Library.Components import Component 
from RCAIDE.Library.Methods.Weights.mass_and_intertia_functions import *  
from .compute_component_centers_of_gravity import compute_component_centers_of_gravity

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Computer Aircraft Center of Gravity
# ----------------------------------------------------------------------------------------------------------------------   
def compute_vehicle_center_of_gravity(vehicle, update_CG=True):
    """
    Computes the overall vehicle center of gravity by aggregating component masses and moments.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing all components and their mass properties
    update_CG : bool, optional
        If True, updates the vehicle's mass_properties.center_of_gravity attribute.
        Default is True.

    Returns
    -------
    CG : ndarray
        3x1 array of [x, y, z] coordinates for vehicle center of gravity [m]
    total_mass : float
        Total mass of the vehicle [kg]

    Notes
    -----
    The function first computes individual component CGs using compute_component_centers_of_gravity(),
    then calculates the overall vehicle CG using the weighted average formula:

    .. math::
        \vec{CG}_{total} = \frac{\sum_{i} m_i\vec{r}_i}{\sum_{i} m_i}

    where:
        * m_i is the mass of each component
        * r_i is the position vector of each component's CG

    **Major Assumptions**
        * All component masses and CGs are accurately defined
        * Components are treated as point masses at their CG locations
        * Vehicle coordinate system is consistent across all components

    References
    ----------
    [1] Moulton, B. C., & Hunsaker, D. F. (2023). Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density. AIAA SCITECH 2023 Forum. DOI: 10.2514/6.2023-2432

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Center_of_Gravity.compute_component_centers_of_gravity
    RCAIDE.Library.Methods.Weights.mass_and_intertia_functions
    """
    
    # compute compoment center of gravity     
    compute_component_centers_of_gravity(vehicle)
    
    # compute total aircraft center of grabity 
    total_moment = np.array([[0.0,0.0,0.0]])
    total_mass   = 0

    for key in vehicle.keys():
        item = vehicle[key]
        if isinstance(item,Component.Container):
            Moment, Mass  = sum_moment(item)  
            total_moment += Moment
            total_mass   += Mass         
    
    if update_CG:
        vehicle.mass_properties.center_of_gravity = total_moment/total_mass 
    
    CG =  total_moment/total_mass
   
    return CG, total_mass


