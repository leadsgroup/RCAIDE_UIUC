# RCAIDE/Library/Methods/Propulsors/Converters/Scramjet/compute_scramjet_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_scramjet_performance
# ----------------------------------------------------------------------------------------------------------------------    
def compute_scramjet_performance(scramjet,scramjet_conditions,conditions): 
    """This computes exit conditions of a scramjet. 
    
    Assumptions: 
    Fixed output Cp and Gamma 
    
    Source: 
    Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M.,  
    "Hypersonic Airbreathing Propulsion", 1994  
    Chapter 4 - pgs. 175-180
    
    Inputs:  
    conditions.freestream.  
       isentropic_expansion_factor         [-]  
       specific_heat_at_constant_pressure  [J/(kg K)]  
       pressure                            [Pa]  
       stagnation_pressure                 [Pa]  
       stagnation_temperature              [K]  
       gas_specific_constant               [J/(kg K)]  
       mach_number                         [-]  
    
    scramjet_conditions.inputs.  
       stagnation_temperature              [K]  
       stagnation_pressure                 [Pa]  
    
    Outputs:  
    scramjet_conditions.outputs.  
       stagnation_temperature              [K]    
       stagnation_pressure                 [Pa]  
       stagnation_enthalpy                 [J/kg]  
       mach_number                         [-]  
       static_temperature                  [K]  
       static_enthalpy                     [J/kg]  
       velocity                            [m/s]  
       static_pressure                     [Pa]  
       area_ratio                          [-]  
    
    Properties Used:  
    self.  
       polytropic_efficiency               [-]  
       pressure_expansion_ratio            [-]                    
    """  
    
    # unpack values  
    
    # unpack from conditions 
    Po         = conditions.freestream.pressure   
    Vo         = conditions.freestream.velocity 
    To         = conditions.freestream.temperature 
    R          = conditions.freestream.gas_specific_constant 
    
    # unpack from inputs 
    Tt_in      = scramjet_conditions.inputs.stagnation_temperature 
    Pt_in      = scramjet_conditions.inputs.stagnation_pressure 
    T_in       = scramjet_conditions.inputs.static_temperature 
    P_in       = scramjet_conditions.inputs.static_pressure 
    u_in       = scramjet_conditions.inputs.velocity 
    f          = scramjet_conditions.inputs.fuel_to_air_ratio   
    Cpe        = scramjet_conditions.inputs.specific_heat_constant_pressure 
    gamma      = scramjet_conditions.inputs.isentropic_expansion_factor                 

    # unpack from self 
    eta        = scramjet.polytropic_efficiency 
    p10_p0     = scramjet.pressure_expansion_ratio
    
    # compute output properties 
    P_out      = Po*p10_p0
    T_out      = T_in*(1.-eta*(1.-((P_out/Po)*(Po/P_in))**(R/Cpe))) 
    u_out      = np.sqrt(u_in*u_in+2.*Cpe*(T_in-T_out)) 
    A_ratio    = (1.+f)*(Po/P_out)*(T_out/To)*(Vo/u_out) 
    M_out      = u_out/np.sqrt(gamma*R*T_out) 
    
    #pack computed quantities into outputs          
    scramjet_conditions.outputs.stagnation_temperature  = Tt_in  
    scramjet_conditions.outputs.stagnation_pressure     = Pt_in        
    scramjet_conditions.outputs.temperature             = T_out         
    scramjet_conditions.outputs.pressure                = P_out      
    scramjet_conditions.outputs.velocity                = u_out   
    scramjet_conditions.outputs.static_pressure         = P_out     
    scramjet_conditions.outputs.area_ratio              = A_ratio  
    scramjet_conditions.outputs.mach_number             = M_out
    
    return 