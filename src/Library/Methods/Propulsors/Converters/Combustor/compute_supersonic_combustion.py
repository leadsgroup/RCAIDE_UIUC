# RCAIDE/Library/Methods/Propulsors/Converters/Combustor/compute_supersonic_combustion.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
# calculate_power_from_throttle
# ----------------------------------------------------------------------------------------------------------------------    
def compute_supersonic_combustion(combustor,combustor_conditions,conditions): 
    """ This function computes the output values for supersonic combustion (Scramjet).
    This will be done using stream thrust analysis. The following properties are computed. 
    combustor_conditions.outputs. 
       stagnation_temperature               (numpy.ndarray) : [K] 
       stagnation_pressure                  (numpy.ndarray) : [Pa] 
       stagnation_enthalpy                  (numpy.ndarray) : [J/kg] 
       fuel_to_air_ratio                    (numpy.ndarray) : [unitless] 
       static_temperature                   (numpy.ndarray) : [K] 
       static_pressure                      (numpy.ndarray) : [Pa] 
       velocity                             (numpy.ndarray) : [m/s] 
       mach_number                          (numpy.ndarray) : [unitless]   
    
    
    Assumptions: 
        1. Constant Pressure Combustion      
        2. Flow is in axial direction at all times 
        3. Flow properities at exit are 1-Da averages 

    Source: 
        Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
        "Hypersonic Airbreathing Propulsion", 1994 
        Chapter 4 - pgs. 175-180
    
    Args: 
        conditions.freestream. 
           isentropic_expansion_factor              (numpy.ndarray): [unitless] 
           specific_heat_at_constant_pressure       (numpy.ndarray): [J/(kg K)] 
           temperature                              (numpy.ndarray): [K] 
           stagnation_temperature                   (numpy.ndarray): [K]
           universal_gas_constant                   (numpy.ndarray): [J/(kg K)]  
        combustor_conditions.inputs.     
           stagnation_temperature                   (numpy.ndarray): [K] 
           stagnation_pressure                      (numpy.ndarray): [Pa] 
           inlet_nozzle                             (numpy.ndarray): [unitless] 
          combustor.fuel_data.specific_energy       (numpy.ndarray): [J/kg] 
          combustor.efficiency                              (float): [unitless]
          combustor.axial_fuel_velocity_ratio               (float): [unitless] 
          combustor.fuel_velocity_ratio                     (float): [unitless] 
          combustor.burner_drag_coefficient                 (float): [unitless] 
          combustor.temperature_reference                   (float): [K] 
          combustor.absolute_sensible_enthalpy              (float): [J/kg] 
          combustor.specific_heat_constant_pressure         (float): [J/(kg K)] 

    Returns:  
      """  
    # unpacking conditions 
    R      = conditions.freestream.gas_specific_constant 
    Tref   = conditions.freestream.temperature
    
    # unpacking properties of combustor 
    nozzle  = combustor_conditions.inputs.inlet_nozzle 
    Pt_in   = combustor_conditions.inputs.stagnation_pressure 
    Cp_c    = nozzle.specific_heat_at_constant_pressure 
    htf     = combustor.fuel_data.specific_energy 
    eta_b   = combustor.efficiency 
    Vfx_V3  = combustor.axial_fuel_velocity_ratio 
    Vf_V3   = combustor.fuel_velocity_ratio 
    Cfb     = combustor.burner_drag_coefficient 
    hf      = combustor.absolute_sensible_enthalpy 
    phi     = combustor.fuel_equivalency_ratio
    
    # compute gamma and Cp over burner 
    Cpb     = 1.45 * Cp_c         
    gamma_b = (Cpb/R)/(Cpb/R-1.)  
    
    # unpack nozzle input values 
    T_in = nozzle.static_temperature 
    V_in = nozzle.velocity 
    P_in = nozzle.static_pressure 
    
    # setting stoichiometric fuel-to-air   
    f    = phi*combustor.fuel_data.stoichiometric_fuel_to_air
    
    # compute output velocity, mach and temperature 
    V_out  = V_in*(((1.+f*Vfx_V3)/(1.+f))-(Cfb/(2.*(1.+f)))) 
    T_out  = ((T_in/(1.+f))*(1.+(1./(Cpb*T_in ))*(eta_b*f*htf+f*hf+f*Cpb*Tref+(1.+f*Vf_V3*Vf_V3)*V_in*V_in/2.))) - V_out*V_out/(2.*Cpb) 
    M_out  = V_out/(np.sqrt(gamma_b*R*T_out)) 
    Tt_out = T_out*(1.+(gamma_b-1.)/2.)*M_out*M_out
    
    # compute the exity static and stagnation conditions 
    ht_out = Cpb*Tt_out 
    P_out  = P_in 
    Pt_out = Pt_in*((((gamma_b+1.)*(M_out**2.))/((gamma_b-1.)*M_out**2.+2.))**(gamma_b/(gamma_b-1.)))*((gamma_b+1.)/(2.*gamma_b*M_out**2.-(gamma_b-1.)))**(1./(gamma_b-1.))  
    
    # pack results   
    combustor_conditions.outputs.stagnation_temperature          = Tt_out  
    combustor_conditions.outputs.stagnation_pressure             = Pt_out        
    combustor_conditions.outputs.stagnation_enthalpy             = ht_out        
    combustor_conditions.outputs.fuel_to_air_ratio               = f        
    combustor_conditions.outputs.static_temperature              = T_out  
    combustor_conditions.outputs.static_pressure                 = P_out         
    combustor_conditions.outputs.velocity                        = V_out  
    combustor_conditions.outputs.mach_number                     = M_out 
    combustor_conditions.outputs.specific_heat_constant_pressure = Cpb
    combustor_conditions.outputs.isentropic_expansion_factor     = gamma_b
    return 

