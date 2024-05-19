## @ingroup Methods-Stability-Center_of_Gravity
# RCAIDE/Methods/Stability/Center_of_Gravity/compute_vehicle_center_of_gravity.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
from Legacy.trunk.S.Components import Physical_Component 
from RCAIDE.Library.Components import Component 
from RCAIDE.Library.Methods.Stability.Common import * 
from .compute_component_centers_of_gravity import compute_component_centers_of_gravity

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Computer Aircraft Center of Gravity
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Center_of_Gravity 
def compute_vehicle_center_of_gravity(vehicle): 
    ''' Computes the moment of intertia of aircraft 
    
    Source:
    Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density
    Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components 
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    
    Assumtions:
    Assumes simplified shapes 
    
    Inputs:
    vehicle           - vehicle data structure           [m]
    
    Outputs:
    I                 - mass moment of inertia matrix    [kg-m^2]
    
    '''
    
    # compute compoment center of gravity     
    compute_component_centers_of_gravity(vehicle)
    
    # compute total aircraft center of grabity 
    total_moment = np.array([[0.0,0.0,0.0]])
    total_mass   = 0

    for key in vehicle.keys():
        item = vehicle[key]
        if isinstance(item,Physical_Component.Container) or isinstance(item,Component.Container):
            Moment, Mass  = sum_moment(item)  
            total_moment += Moment
            total_mass   += Mass 
    for network in vehicle.networks:
        for net_key in network.keys():
            net_item = network[net_key] 
            if isinstance(net_item,Energy_Component.Container):
                Moment, Mass  = sum_moment(net_item)  
                total_moment += Moment
                total_mass   += Mass  
        for bus in network.busses: 
            Moment, Mass  = sum_moment(bus)  
            total_moment += Moment
            total_mass   += Mass   
        for fuel_line in network.fuel_lines: 
            Moment, Mass  = sum_moment(fuel_line)  
            total_moment += Moment
            total_mass   += Mass            
            
    vehicle.mass_properties.center_of_gravity = total_moment/total_mass 
            
    return  


