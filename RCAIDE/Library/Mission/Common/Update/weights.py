# RCAIDE/Library/Mission/Common/Update/weights.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Update Weights
# ----------------------------------------------------------------------------------------------------------------------  
def weights(segment):
    """
    Updates vehicle mass and weight forces during mission

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function integrates mass flow rates to track vehicle mass changes
    and updates the corresponding gravitational forces. It handles both
    primary and additional fuel consumption.

    **Required Segment Components**

    segment:
        state:
            numerics.time:
                - integrate : array
                    Time integration operator
            conditions:
                weights:
                    - total_mass : array
                        Vehicle mass [kg]
                    - vehicle_mass_rate : array
                        Mass consumption rate [kg/s]
                freestream:
                    - gravity : array
                        Gravitational acceleration [m/s²]
        analyses.energy.vehicle.networks:
            fuel_lines:
                - fuel_tanks : list
                    List of fuel tanks
                - mass : array
                    Fuel mass [kg]
                - mass_flow_rate : array
                    Fuel flow rate [kg/s]

    **Major Assumptions**
    * Continuous mass flow
    * Well-defined fuel systems
    * Valid integration scheme
    * Conservative mass transfer

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.weights.total_mass [kg]
        - conditions.frames.inertial.gravity_force_vector [N]
        - conditions.energy.*.*.mass [kg]


    """
    
    # unpack
    conditions   = segment.state.conditions
    I            = segment.state.numerics.time.integrate  
    m0           = conditions.weights.total_mass[0,0]
    mdot_fuel    = conditions.weights.vehicle_mass_rate
    g            = conditions.freestream.gravity   
    
    networks = segment.analyses.energy.vehicle.networks
    for network in networks:
        if 'fuel_lines' in network:
            for fuel_line in network.fuel_lines:  
                fuel_line_results   = conditions.energy[fuel_line.tag] 
                for fuel_tank in fuel_line.fuel_tanks: 
                    fuel_line_results[fuel_tank.tag].mass[:,0]  =  fuel_line_results[fuel_tank.tag].mass[0,0]  + np.dot(I, -fuel_line_results[fuel_tank.tag].mass_flow_rate[:,0])   
            
    # calculate
    m = m0 + np.dot(I, -mdot_fuel )

    # weight
    W = m*g

    # pack
    conditions.weights.total_mass[1:,0]                  = m[1:,0]  
    conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]

    return
 