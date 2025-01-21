# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_aircraft_moment_of_inertia.py 
# 
# Created:  September 2024, A. Molloy

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia import compute_cuboid_moment_of_inertia, compute_cylinder_moment_of_inertia, compute_wing_moment_of_inertia

import RCAIDE
import numpy as  np 

# ------------------------------------------------------------------        
#  Component moments of inertia (MOI) tensors
# ------------------------------------------------------------------  
def compute_aircraft_moment_of_inertia(vehicle, CG_location, update_MOI=True):
    """
    Computes the total aircraft moment of inertia tensor by summing contributions from all major components.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing components:
            - fuselages : list
                All fuselage segments
            - wings : list
                All wing surfaces (main wing, horizontal tail, etc.)
            - networks : list
                Propulsion networks containing:
                    - propulsors : list
                        Electric rotors, turbofans, etc.
                    - busses : list
                        Battery modules
                    - fuel_lines : list
                        Fuel tanks (central and wing)
    CG_location : array
        Vehicle center of gravity location [m]
    update_MOI : bool, optional
        Flag to update vehicle mass properties with computed MOI, default True

    Returns
    -------
    MOI_tensor : ndarray
        3x3 moment of inertia tensor about CG [kg-m²]
    MOI_mass : float
        Total mass of all components included in MOI calculation [kg]

    Notes
    -----
    Computes inertia tensors for:
        * Fuselage sections
        * Wing surfaces
        * Propulsion components
            - Motors/engines
            - Batteries
            - Fuel tanks

    **Major Assumptions**
        * Components can be approximated as basic geometric shapes
        * Small components' contributions are negligible
        * Rigid body dynamics
        * Component masses are uniformly distributed
        * Parallel axis theorem is valid for all components

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_wing_moment_of_inertia
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_cylinder_moment_of_inertia
    RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_cuboid_moment_of_inertia
    """    
    
    # ------------------------------------------------------------------        
    # Setup
    # ------------------------------------------------------------------      
    # Array to hold the entire aircraft's inertia tensor
    MOI_tensor = np.zeros((3, 3)) 
    MOI_mass = 0
    
    # ------------------------------------------------------------------        
    #  Fuselage(s)
    # ------------------------------------------------------------------      
    for fuselage in vehicle.fuselages:
        I, mass = fuselage.compute_moment_of_inertia(center_of_gravity = CG_location)
        MOI_tensor += I
        MOI_mass += mass
    
    # ------------------------------------------------------------------        
    #  Wing(s)
    # ------------------------------------------------------------------      
    for wing in vehicle.wings:
        I, mass = wing.compute_moment_of_inertia(mass=wing.mass_properties.mass, center_of_gravity =CG_location)
        MOI_tensor += I
        MOI_mass += mass
    
    # ------------------------------------------------------------------        
    #  Energy network
    # ------------------------------------------------------------------      
    I_network = np.zeros([3, 3]) 
    for network in vehicle.networks:
        for propulsor in network.propulsors:
            if isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Electric_Rotor):
                motor   = propulsor.motor 
                I, mass = compute_cylinder_moment_of_inertia(motor.origin,motor.mass_properties.mass, 0, 0, 0,0, CG_location)
                I_network += I
                MOI_mass  += mass
                    
            if isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turbofan):
                I, mass= compute_cylinder_moment_of_inertia(propulsor.origin, propulsor.mass_properties.mass, propulsor.engine_length, propulsor.nacelle.diameter/2, 0, 0, CG_location)                    
                I_network += I
                MOI_mass += mass
            if isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turboprop):
                I, mass= compute_cylinder_moment_of_inertia(propulsor.origin, propulsor.mass_properties.mass, propulsor.engine_length, propulsor.engine_diameter/2, 0, 0, CG_location)                    
                I_network += I
                MOI_mass += mass
            if isinstance(propulsor,RCAIDE.Library.Components.Propulsors.ICE_Propeller):
                I, mass= compute_cylinder_moment_of_inertia(propulsor.origin, propulsor.mass_properties.mass, propulsor.engine_length, propulsor.engine_diameter/2, 0, 0, CG_location)                    
                I_network += I
                MOI_mass += mass
        
        for bus in network.busses: 
            for battery in bus.battery_modules: 
                I_battery, mass_battery = compute_cuboid_moment_of_inertia(battery.origin, battery.mass_properties.mass, battery.length, battery.width, battery.height, 0, 0, 0, CG_location)
                I_network += I_battery
                MOI_mass  += mass_battery         
                                 
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks:
                if isinstance(fuel_tank,RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks.Central_Fuel_Tank ): 
                    I, mass = compute_cuboid_moment_of_inertia(fuel_tank.origin, fuel_tank.fuel.mass_properties.mass, fuel_tank.length, fuel_tank.width, fuel_tank.height, 0, 0, 0, CG_location)
                    I_network += I
                    MOI_mass += mass
                if isinstance(fuel_tank,RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks.Wing_Fuel_Tank): 
                    I, mass =  compute_wing_moment_of_inertia(vehicle.wings["main_wing"], mass=fuel_tank.fuel.mass_properties.mass, center_of_gravity = CG_location, fuel_flag=True)
                    I_network += I
                    MOI_mass += mass                    
                else:
                    pass # TO DO
                        
    MOI_tensor += I_network    
    
    if update_MOI:
        vehicle.mass_properties.moments_of_inertia.tensor = MOI_tensor  
    return MOI_tensor,MOI_mass     