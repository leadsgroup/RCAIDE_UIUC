# RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network_Method/evaluate_CRN_emission_indices.py
#  
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.evaluate_cantera import evaluate_cantera 
 
# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  evaluate_correlation_emissions_indices
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate_CRN_emission_indices_no_surrogate(segment,settings,vehicle):
  
    # unpack
    state     = segment.state
    I         = state.numerics.time.integrate
    
    CO2_total = 0 * state.ones_row(1)  
    CO_total  = 0 * state.ones_row(1) 
    H2O_total = 0 * state.ones_row(1) 
    NO_total  = 0 * state.ones_row(1) 
    NO2_total = 0 * state.ones_row(1) 

    for network in vehicle.networks:  
        for fuel_line in network.fuel_lines:
            if fuel_line.active:  
                for p_i ,  propulsor in enumerate(network.propulsors):
                    if propulsor.active == True: 
                        if (type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbofan) or \
                            type(propulsor) == RCAIDE.Library.Components.Propulsors.Turboshaft or \
                            type(propulsor) == RCAIDE.Library.Components.Propulsors.Turboprop or \
                            type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbojet:    
                        
                            combustor = propulsor.combustor
                        
                            # unpack component conditions
                            n_cp                 = state.numerics.number_of_control_points 
                            propulsor_conditions = state.conditions.energy[propulsor.tag] 
                            combustor_conditions = propulsor_conditions[combustor.tag]  

                            
                            T    = combustor_conditions.inputs.stagnation_temperature
                            P    = combustor_conditions.inputs.stagnation_pressure 
                            mdot = propulsor_conditions.core_mass_flow_rate 
                            FAR  = combustor_conditions.outputs.fuel_to_air_ratio 

                            EI_CO2_comb   = 0 * state.ones_row(1)   
                            EI_CO_comb    = 0 * state.ones_row(1)  
                            EI_H2O_comb   = 0 * state.ones_row(1)  
                            EI_NO_comb    = 0 * state.ones_row(1)  
                            EI_NO2_comb   = 0 * state.ones_row(1)                              
                            if network.identical_propulsors == True and p_i != 0:
                                EI_CO2_comb = EI_CO2_prev
                                EI_CO_comb  = EI_CO_prev
                                EI_H2O_comb = EI_H2O_prev
                                EI_NO_comb  = EI_NO_prev
                                EI_NO2_comb = EI_NO2_prev 
                                
                            else:     
                                for t_idx in range(n_cp):
                                    # Call cantera 
                                    results = evaluate_cantera(combustor,T[t_idx,0],P[t_idx,0],mdot[t_idx,0],FAR[t_idx,0])
                                    
                                    EI_CO2_comb[t_idx,0] = results.EI_CO2
                                    EI_CO_comb[t_idx,0]  = results.EI_CO 
                                    EI_H2O_comb[t_idx,0] = results.EI_H2O
                                    EI_NO_comb[t_idx,0]  = results.EI_NO 
                                    EI_NO2_comb[t_idx,0] = results.EI_NO2
                                    
                                    EI_CO2_prev = EI_CO2_comb 
                                    EI_CO_prev  =  EI_CO_comb  
                                    EI_H2O_prev = EI_H2O_comb 
                                    EI_NO_prev  =  EI_NO_comb  
                                    EI_NO2_prev = EI_NO2_comb 
                                
                            CO2_total  += np.dot(I,mdot*EI_CO2_comb)
                            CO_total   += np.dot(I,mdot *EI_CO_comb )
                            H2O_total  += np.dot(I,mdot*EI_H2O_comb)
                            NO_total   += np.dot(I,mdot *EI_NO_comb ) 
                            NO2_total  += np.dot(I,mdot *EI_NO2_comb)

    emissions                 = Data()
    emissions.total           = Data()
    emissions.index           = Data() 
    emissions.total.CO2       = CO2_total  * combustor.fuel_data.global_warming_potential_100.CO2 
    emissions.total.H2O       = H2O_total  * combustor.fuel_data.global_warming_potential_100.H2O  
    emissions.total.NOx       = (NO_total + NO2_total) * combustor.fuel_data.global_warming_potential_100.NOx 
    emissions.index.CO2       = EI_CO2_comb
    emissions.index.CO        = EI_CO_comb 
    emissions.index.H2O       = EI_H2O_comb
    emissions.index.NO        = EI_NO_comb 
    emissions.index.NO2       = EI_NO2_comb 
    
    state.conditions.emissions =  emissions
    return    
    

def evaluate_CRN_emission_indices_surrogate(segment,settings,vehicle): 
  
    I          = segment.state.numerics.time.integrate
    surrogates = segment.analyses.emissions.surrogates
    
    CO2_total = 0 * segment.state.ones_row(1)  
    CO_total  = 0 * segment.state.ones_row(1) 
    H2O_total = 0 * segment.state.ones_row(1) 
    NO_total  = 0 * segment.state.ones_row(1) 
    NO2_total = 0 * segment.state.ones_row(1) 

    for network in vehicle.networks:    
        for propulsor in network.propulsors:
            if propulsor.active == True:
                if (type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbofan) or \
                    type(propulsor) == RCAIDE.Library.Components.Propulsors.Turboprop or \
                    type(propulsor) == RCAIDE.Library.Components.Propulsors.Turboshaft or \
                    type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbojet:    
                
                    combustor = propulsor.combustor
                
                    # unpack component conditions
                    propulsor_conditions = segment.state.conditions.energy[propulsor.tag] 
                    combustor_conditions = propulsor_conditions[combustor.tag]  

                    T    = combustor_conditions.inputs.stagnation_temperature
                    P    = combustor_conditions.inputs.stagnation_pressure 
                    mdot = propulsor_conditions.core_mass_flow_rate 
                    FAR  = combustor_conditions.outputs.fuel_to_air_ratio 
                    
                    pts = np.hstack((T,P,mdot,FAR )) 

                    EI_CO2_comb  = np.atleast_2d(surrogates.EI_CO2(pts)).T
                    EI_CO_comb   = np.atleast_2d(surrogates.EI_CO(pts)).T 
                    EI_H2O_comb  = np.atleast_2d(surrogates.EI_H2O(pts)).T 
                    EI_NO_comb   = np.atleast_2d(surrogates.EI_NO(pts)).T 
                    EI_NO2_comb  = np.atleast_2d(surrogates.EI_NO2(pts)).T        
                          
                    CO2_total += np.dot(I,mdot*EI_CO2_comb)
                    CO_total  += np.dot(I,mdot *EI_CO_comb )
                    H2O_total += np.dot(I,mdot*EI_H2O_comb)
                    NO_total  += np.dot(I,mdot *EI_NO_comb ) 
                    NO2_total += np.dot(I,mdot *EI_NO2_comb)

    emissions                 = Data()
    emissions.total           = Data()
    emissions.index           = Data() 
    emissions.total.CO2       = CO2_total * combustor.fuel_data.global_warming_potential_100.CO2 
    emissions.total.H2O       = H2O_total * combustor.fuel_data.global_warming_potential_100.H2O  
    emissions.total.NOx       = (NO_total + NO2_total) * combustor.fuel_data.global_warming_potential_100.NOx 
    emissions.index.CO2       = EI_CO2_comb
    emissions.index.CO        = EI_CO_comb 
    emissions.index.H2O       = EI_H2O_comb
    emissions.index.NO        = EI_NO_comb 
    emissions.index.NO2       = EI_NO2_comb 
 
    segment.state.conditions.emissions =  emissions
    return   

     