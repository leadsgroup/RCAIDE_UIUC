# RCAIDE/Methods/Energy/Propulsors/Turboprop_Propulsor/compute_thrust.py
# 
# 
# Created:  Sep 2024, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Framework.Core      import Units 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_thrust
# ----------------------------------------------------------------------------------------------------------------------
def compute_thrust(turboprop,turboprop_conditions,conditions):
    
    """Computes thrust and other properties as below.

    Assumptions:
    Perfect gas

    Source:
    Mattingly, Jack D.. “Elements of Gas Turbine Propulsion.” (1996).

    Inputs:
    conditions.freestream.gravity 
    conditions.freestream.temperature
    conditions.freestream.pressure      
    conditions.freestream.mach_number
    conditions.freestream.velocity
    conditions.freestream.speed_of_sound
    turboprop.reference_temperature
    turboprop.reference_pressure 
    turboprop.combustor.turbine_inlet_temperature
    turboprop.design_propeller_efficiency
    turboprop.design_gearbox_efficiency
    turboprop.low_pressure_turbine.mechanical_efficiency
    turboprop.combustor.fuel_data.lower_heating_value
    turboprop_conditions.stag_temp_hpt_out
    turboprop_conditions.stag_temp_hpt_in
    turboprop_conditions.stag_temp_lpt_out
    turboprop_conditions.stag_temp_lpt_in
    turboprop_conditions.total_temperature_reference
    turboprop_conditions.total_pressure_reference     
    turboprop_conditions.fuel_to_air_ratio 
    turboprop_conditions.cpt
    turboprop_conditions.cpc
    turboprop_conditions.R_t
    turboprop_conditions.R_c
    turboprop_conditions.T9
    turboprop_conditions.P9  
    turboprop_conditions.gamma_c
    turboprop_conditions.core_exit_velocity
    
    Outputs:
    turboprop_conditions.thrust                           
    turboprop_conditions.thrust_specific_fuel_consumption 
    turboprop_conditions.non_dimensional_thrust           
    turboprop_conditions.core_mass_flow_rate              
    turboprop_conditions.fuel_flow_rate                   
    turboprop_conditions.power                            
    turboprop_conditions.specific_power                   
    turboprop_conditions.power_specific_fuel_consumption  
    turboprop_conditions.thermal_efficiency               
    turboprop_conditions.propulsive_efficiency               
    """       
    
    #compute dimensional mass flow rates 
    g                                              = conditions.freestream.gravity                                                                             # [m/s**2]
    Tref                                           = turboprop.reference_temperature                                                                           # [K]
    Pref                                           = turboprop.reference_pressure                                                                              # [Pa]
    total_temperature_reference                    = turboprop_conditions.total_temperature_reference                                                          # [K]
    total_pressure_reference                       = turboprop_conditions.total_pressure_reference                                                             # [Pa]
                                                                                                                                                                          
    #unpack from turboprop                                                                                                                                     
    fuel_to_air_ratio                              = turboprop_conditions.Comb.outputs.fuel_to_air_ratio                                                                    # [-]
    turbine_cp                                     = turboprop_conditions.lpt.outputs.cp                                                                                 # [J/kg*K]
    compressor_cp                                  = turboprop_conditions.lpc.outputs.cp                                                                                # [J/kg*K]   
    turbine_gas_constant                           = turboprop_conditions.lpt.outputs.gas_constant                                                                                 # [J/mol*K]    
    compressor_gas_constant                        = turboprop_conditions.lpc.outputs.gas_constant                                                                                  # [J/mol*K]
    core_exit_temperature                          = turboprop_conditions['core nozzle'].outputs.static_temperature                                                                                  # [K]
    core_exit_pressure                             = turboprop_conditions['core nozzle'].outputs.static_pressure                                                                                     # [Pa]     
    compressor_gamma                               = turboprop_conditions.lpc.outputs.gamma                                                                             # [-]
    core_exit_velocity                             = turboprop_conditions['core nozzle'].outputs.velocity                                                                                     # [Pa]     elocity                                                                   # [m/s]
    T0                                             = conditions.freestream.temperature                                                                         # [K]
    P0                                             = conditions.freestream.pressure                                                                            # [Pa]   
    M0                                             = conditions.freestream.mach_number                                                                         # [-]    
    V0                                             = conditions.freestream.velocity                                                                            # [m/s]
    a0                                             = conditions.freestream.speed_of_sound                                                                      # [m/s]
    Tt4                                            = turboprop.combustor.turbine_inlet_temperature                                                             # [K]     
    propeller_efficiency                           = turboprop.design_propeller_efficiency                                                                     # [-]
    gearbox_efficiency                             = turboprop.design_gearbox_efficiency                                                                       # [-]
    low_pressure_turbine_mechanical_efficiency     = turboprop.low_pressure_turbine.mechanical_efficiency                                                      # [-]
    lower_heating_value                            = turboprop.combustor.fuel_data.lower_heating_value                                                         # [J/kg]
    high_pressure_turbine_temperature_ratio        = (turboprop_conditions.hpt.outputs.stagnation_temperature/turboprop_conditions.hpt.inputs.stagnation_temperature)                            # [-]
    low_pressure_turbine_temperature_ratio         = (turboprop_conditions.lpt.outputs.stagnation_temperature/turboprop_conditions.lpt.inputs.stagnation_temperature)                            # [-]

    propeller_thrust_coefficient                   = propeller_efficiency*gearbox_efficiency*low_pressure_turbine_mechanical_efficiency*(1 + fuel_to_air_ratio)*(turbine_cp*Tt4)/(compressor_cp*T0)*high_pressure_turbine_temperature_ratio*(1 - low_pressure_turbine_temperature_ratio)                                    # [-]
    compressor_thrust_coefficient                 = (compressor_gamma - 1)*M0*((1 + fuel_to_air_ratio)*(core_exit_velocity/a0) - M0 + (1 + fuel_to_air_ratio)*(turbine_gas_constant/compressor_gas_constant)*((core_exit_temperature/T0)/((core_exit_velocity/a0)))*((1 - (P0/core_exit_pressure))/compressor_gamma))   # [-]
    total_thrust_coefficient                      = propeller_thrust_coefficient + compressor_thrust_coefficient                                                                                               # [-]
    Fsp                                            = (total_thrust_coefficient*compressor_cp*T0)/(V0)                                                                                      # [(N*s)/kg] 
    TSFC                                           = (fuel_to_air_ratio/(Fsp)) * Units.hour                                                                                    # [kg/(N*hr)] 
    W_dot_mdot0                                    = total_thrust_coefficient*compressor_cp*T0                                                                                             # [(W*s)/kg] 
    PSFC                                           = (fuel_to_air_ratio/(total_thrust_coefficient*compressor_cp*T0)) * Units.hour                                                                          # [kg/(W*hr)]
    eta_T                                          = total_thrust_coefficient/((fuel_to_air_ratio*lower_heating_value)/(compressor_cp*T0))                                                                                # [-]
    eta_P                                          = total_thrust_coefficient/((propeller_thrust_coefficient/propeller_efficiency) + ((compressor_gamma - 1)/2)*((1 + fuel_to_air_ratio)*((core_exit_velocity/a0))**2 - M0**2))                              # [-]   
    
    mdot_core                                      = turboprop.design_thrust*turboprop_conditions.throttle/(Fsp)                                               # [kg/s]
    mdhc                                           = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))                    # [kg/s]
    
    #computing the dimensional thrust
    FD2                                            = Fsp*mdot_core                                                                                             # [N]  

    #fuel flow rate
    a                                              = np.array([0.])                                                                                            # [-]     
    fuel_flow_rate                                 = np.fmax(FD2*TSFC/g,a)*1./Units.hour                                                                       # [kg/s]  

    #computing the power 
    power                                          = FD2*V0

    # pack outputs 
    turboprop_conditions.thrust                            = FD2 
    turboprop_conditions.thrust_specific_fuel_consumption  = TSFC
    turboprop_conditions.non_dimensional_thrust            = Fsp 
    turboprop_conditions.core_mass_flow_rate               = mdot_core
    turboprop_conditions.fuel_flow_rate                    = fuel_flow_rate    
    turboprop_conditions.power                             = power  
    turboprop_conditions.specific_power                    = W_dot_mdot0  
    turboprop_conditions.power_specific_fuel_consumption   = PSFC 
    turboprop_conditions.thermal_efficiency                = eta_T
    turboprop_conditions.propulsive_efficiency             = eta_P

    return 