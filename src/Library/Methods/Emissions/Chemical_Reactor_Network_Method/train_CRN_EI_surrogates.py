#  RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network_Method/train_CRN_EI_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE 
from RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.evaluate_cantera import evaluate_cantera 

# package imports    
import numpy    as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Train Cantera Model 
# ----------------------------------------------------------------------------------------------------------------------
def train_CRN_EI_surrogates(emissions): 
    
    # unpack data 
    P              = emissions.training.pressure         
    T              = emissions.training.temperature      
    mdot           = emissions.training.air_mass_flowrate
    FAR            = emissions.training.fuel_to_air_ratio
    
    vehicle        = emissions.vehicle
    for network in vehicle.networks:   
        for propulsor in  network.propulsors:
            if  isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turbofan) or \
                isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turbojet) or \
                isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turboshaft) or \
                isinstance(propulsor,RCAIDE.Library.Components.Propulsors.ICE_Propeller):            
                combustor = propulsor.combustor              
            else:
                combustor = False 
            
    len_P    = len(P)
    len_T    = len(T)
    len_mdot = len(mdot)
    len_far  = len(FAR) 
    
    EI_CO2 = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_CO  = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_H2O = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_NO2 = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_NO  = np.zeros((len_P,len_T,len_mdot,len_far))  
    
    if combustor == False:
        emissions.no_combustor = True
        return 
    
    for p_i in range(len_P):
        for t_i in range(len_T):
            for mdot_i in  range(len_mdot):
                for far_i in  range(len_far):
                    
                    # Call cantera 
                    results = evaluate_cantera(combustor,T[t_i],P[p_i],mdot[mdot_i],FAR[far_i]) 
                    
                    EI_CO2[p_i, t_i, mdot_i,far_i] = results.EI_CO2
                    EI_CO [p_i, t_i, mdot_i,far_i] = results.EI_CO 
                    EI_H2O[p_i, t_i, mdot_i,far_i] = results.EI_H2O
                    EI_NO [p_i, t_i, mdot_i,far_i] = results.EI_NO 
                    EI_NO2[p_i, t_i, mdot_i,far_i] = results.EI_NO2
    
    emissions.training.EI_CO2 = EI_CO2
    emissions.training.EI_CO =  EI_CO
    emissions.training.EI_H2O = EI_H2O
    emissions.training.EI_NO =  EI_NO
    emissions.training.EI_NO2 = EI_NO2
    
    return 