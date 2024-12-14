# RCAIDE/Library/Methods/Propulsors/Converters/supersonic_nozzle/compute_limited_geometry.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np
from RCAIDE.Library.Methods.Gas_Dynamics.fm_id import fm_id
from RCAIDE.Library.Methods.Gas_Dynamics.nozzle_calculations import  pressure_ratio_isentropic, pressure_ratio_shock_in_nozzle


# ---------------------------------------------------------------------------------------------------------------------- 
# compute_limited_geometry
# ----------------------------------------------------------------------------------------------------------------------
def compute_limited_geometry(supersonic_nozzle, s_nozzle_conditions,conditions): 
    
    #unpack from conditions
    gamma    = conditions.freestream.isentropic_expansion_factor
    Cp       = conditions.freestream.specific_heat_at_constant_pressure
    Po       = conditions.freestream.pressure 
    R        = conditions.freestream.gas_specific_constant 
    
    #unpack from inputs
    Tt_in    = s_nozzle_conditions.inputs.stagnation_temperature
    Pt_in    = s_nozzle_conditions.inputs.stagnation_pressure                
    
    #unpack from self
    pid             = supersonic_nozzle.pressure_ratio
    etapold         = supersonic_nozzle.polytropic_efficiency
    max_area_ratio  = supersonic_nozzle.max_area_ratio
    min_area_ratio  = supersonic_nozzle.min_area_ratio
    
    
    # Method for computing the nozzle properties
    #--Getting the output stagnation quantities
    Pt_out   = Pt_in*pid
    Tt_out   = Tt_in*pid**((gamma-1.)/(gamma)*etapold)
    ht_out   = Cp*Tt_out

    # Method for computing the nozzle properties
    #-- Initial estimate for exit area
    area_ratio = (max_area_ratio + min_area_ratio)/2.
    
    #-- Compute limits of each possible flow condition       
    subsonic_pressure_ratio     = pressure_ratio_isentropic(area_ratio, gamma, True)
    nozzle_shock_pressure_ratio = pressure_ratio_shock_in_nozzle(area_ratio, gamma) 
    supersonic_max_Area         = pressure_ratio_isentropic(max_area_ratio, gamma, False)
    supersonic_min_Area         = pressure_ratio_isentropic(min_area_ratio, gamma, False)

    #-- Compute the output Mach number guess with freestream pressure
    #-- Initializing arrays
    P_out       = np.ones_like(Pt_out)
    A_ratio     = area_ratio*np.ones_like(Pt_out)
    M_out       = np.ones_like(Pt_out)

    # Establishing a correspondence between real pressure ratio and limits of each flow condition
    
    # Determine if flow is within subsonic/sonic range
    i_sub               = Po/Pt_out >= subsonic_pressure_ratio 
    
    # Detemine if there is a shock in nozzle
    i2                  = Po/Pt_out < subsonic_pressure_ratio
    i3                  = Po/Pt_out >= nozzle_shock_pressure_ratio
    i_shock             = np.logical_and(i2,i3)      
    
    # Determine if flow is overexpanded
    i4                  = Po/Pt_out < nozzle_shock_pressure_ratio
    i5                  = Po/Pt_out > supersonic_min_Area
    i_over              = np.logical_and(i4,i5)  
    
    # Determine if flow is supersonic
    i6                  = Po/Pt_out <= supersonic_min_Area
    i7                  = Po/Pt_out >= supersonic_max_Area
    i_sup               = np.logical_and(i6,i7) 
    
    # Determine if flow is underexpanded
    i_und               = Po/Pt_out < supersonic_max_Area
    
    #-- Subsonic and sonic flow
    P_out[i_sub]        = Po[i_sub]
    M_out[i_sub]        = np.sqrt((((Pt_out[i_sub]/P_out[i_sub])**((gamma[i_sub]-1.)/gamma[i_sub]))-1.)*2./(gamma[i_sub]-1.))
    A_ratio[i_sub]      = 1./fm_id(M_out[i_sub],gamma[i_sub])
    
    #-- Shock inside nozzle
    P_out[i_shock]      = Po[i_shock]
    M_out[i_shock]      = np.sqrt((((Pt_out[i_shock]/P_out[i_shock])**((gamma[i_shock]-1.)/gamma[i_shock]))-1.)*2./(gamma[i_shock]-1.))   
    A_ratio[i_shock]    = 1./fm_id(M_out[i_shock],gamma[i_shock])
    
    #-- Overexpanded flow
    P_out[i_over]       = supersonic_min_Area[i_over]*Pt_out[i_over] 
    M_out[i_over]       = np.sqrt((((Pt_out[i_over]/P_out[i_over])**((gamma[i_over]-1.)/gamma[i_over]))-1.)*2./(gamma[i_over]-1.))
    A_ratio[i_over]     = 1./fm_id(M_out[i_over],gamma[i_over])
    
    #-- Isentropic supersonic flow, with variable area adjustments
    P_out[i_sup]        = Po[i_sup]
    M_out[i_sup]        = np.sqrt((((Pt_out[i_sup]/P_out[i_sup])**((gamma[i_sup]-1.)/gamma[i_sup]))-1.)*2./(gamma[i_sup]-1.))    
    A_ratio[i_sup]      = 1./fm_id(M_out[i_sup],gamma[i_sup])
    
    #-- Underexpanded flow
    P_out[i_und]        = supersonic_max_Area[i_und]*Pt_out[i_und] 
    M_out[i_und]        = np.sqrt((((Pt_out[i_und]/P_out[i_und])**((gamma[i_und]-1.)/gamma[i_und]))-1.)*2./(gamma[i_und]-1.))
    A_ratio[i_und]      = 1./fm_id(M_out[i_und],gamma[i_und])
    
    #-- Calculate other flow properties
    T_out   = Tt_out/(1.+(gamma-1.)/2.*M_out*M_out)
    h_out   = Cp*T_out
    u_out   = M_out*np.sqrt(gamma*R*T_out)
    rho_out = P_out/(R*T_out)

    #pack computed quantities into outputs
    s_nozzle_conditions.outputs.stagnation_temperature  = Tt_out
    s_nozzle_conditions.outputs.stagnation_pressure     = Pt_out
    s_nozzle_conditions.outputs.stagnation_enthalpy     = ht_out
    s_nozzle_conditions.outputs.mach_number             = M_out
    s_nozzle_conditions.outputs.static_temperature      = T_out
    s_nozzle_conditions.outputs.rho                     = rho_out
    s_nozzle_conditions.outputs.static_enthalpy         = h_out
    s_nozzle_conditions.outputs.velocity                = u_out
    s_nozzle_conditions.outputs.static_pressure         = P_out
    s_nozzle_conditions.outputs.area_ratio              = A_ratio

    return 
    

