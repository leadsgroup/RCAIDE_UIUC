# RCAIDE/Library/Methods/Propulsors/Converters/Engine/compute_fuel_flow_rate_from_torque.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
# calculate_fuel_flow_rate_from_torque
# ----------------------------------------------------------------------------------------------------------------------    
def compute_fuel_flow_rate_from_torque(engine,engine_conditions,conditions):
    """ The internal combustion engine output power and specific power consumption. The following
    properties are computed:
    engine 
       .outputs.throttle                         (numpy.ndarray): throttle setting              [unitless]
       .outputs.power_specific_fuel_consumption  (numpy.ndarray): Power (brake) SFC             [lbf/(HP · h) ]
       .outputs.fuel_flow_rate                   (numpy.ndarray): fuel flow rate                [kg/s]
       .outputs.power                            (numpy.ndarray): Brake power (or Shaft power)  [W]

    Source:
        Gagg and Ferrar model (ref: S. Gudmundsson, 2014 - eq. 7-16)

    Assumtions:
        None 

    Args:
        freestream conditions 
          .altitude                               (float): altitde                  [m]
          .delta_isa                              (float): altitude offset          [m]
        engine 
            .sea_level_power                           (float): sea-level power     [W]
            .flat_rate_altitude                        (float): flat rate altitude  [m]
            .outputs.omega                     (numpy.ndarray): rated_speed         [RPM]
            .outputs.torque                    (numpy.ndarray): torque              [Nm]
            .power_specific_fuel_consumption   (numpy.ndarray): PSFC                [lbf/(HP · h) ]
            
    Returns:
        None
    """

    # Unpack conditions 
    altitude   = conditions.freestream.altitude
    delta_isa  = conditions.freestream.delta_ISA
    
    # Unpack engine properties 
    PSLS       = engine.sea_level_power
    h_flat     = engine.flat_rate_altitude
    PSFC       = engine.power_specific_fuel_consumption
    omega      = engine_conditions.omega
    torque     = engine_conditions.torque
    
    # compute atmospheric properties 
    altitude_virtual = altitude - h_flat
    altitude_virtual[altitude_virtual<0.] = 0. 
    atmo             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_values_0    = atmo.compute_values(0,0)
    rho0             = atmo_values_0.density[0,0]
    atmo_values      = atmo.compute_values(altitude_virtual,delta_isa)
    rho              = atmo_values.density 
 
    # Compute density ratio
    sigma = rho / rho0
    
    # compute power 
    Pavailable                    = PSLS * (sigma-0.117) / 0.883
    Pavailable[h_flat > altitude] = PSLS 
    P                             = torque * omega
    P[P<0.]                       = 0.
    
    # compute SFC, fuel flow rate and throtttle 
    SFC             = PSFC * Units['lb/hp/hr']
    a               = np.zeros_like(altitude)
    fuel_flow_rate  = np.fmax(P*SFC,a)
    throttle        = P/Pavailable

    # Store results as engine outputs
    engine_conditions.throttle                        = throttle
    engine_conditions.power_specific_fuel_consumption = PSFC
    engine_conditions.fuel_flow_rate                  = fuel_flow_rate
    engine_conditions.power                           = P

    return

