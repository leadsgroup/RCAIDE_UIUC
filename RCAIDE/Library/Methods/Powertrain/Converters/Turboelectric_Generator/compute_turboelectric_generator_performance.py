# RCAIDE/Methods/Library/Methods/Powertrain/Converters/compute_turboelectric_generator_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports      
from RCAIDE.Framework.Core import Data    
from RCAIDE.Library.Methods.Powertrain.Converters.Turboshaft         import compute_turboshaft_performance
from RCAIDE.Library.Methods.Powertrain.Converters.Generator          import compute_generator_performance 
 
# python imports 
from copy import deepcopy 
# ----------------------------------------------------------------------------------------------------------------------
# compute_turboelectric_generator_performance
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_turboelectric_generator_performance(turboelectric_generator,state,fuel_line,bus):    
    ''' Computes the perfomrance of one turboelectric_generator
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions               - operating conditions data structure                  [-]  
    fuel_line                - fuel+line                                            [-] 
    turboelectric_generator  - turboelectric_generator data structure               [-] 
    total_power              - power of turboelectric_generator group               [W] 

    Outputs:  
    total_power              - power of turboelectric_generator group               [W] 
    stored_results_flag      - boolean for stored results                           [-]     
    stored_propulsor_tag     - name of turboelectric_generator with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''

    conditions        = state.conditions
    generator         = turboelectric_generator.generator
    turboshaft        = turboelectric_generator.turboshaft

    turboelectric_generator_conditions = conditions.energy[turboelectric_generator.tag] 
    generator_conditions               = turboelectric_generator_conditions[generator.tag]
    turboshaft_conditions              = turboelectric_generator_conditions[turboshaft.tag]    
    
    compute_turboshaft_performance(turboshaft,turboshaft_conditions,conditions) 
    P_mech  = turboelectric_generator_conditions.turboshaft.power  
    shaft_omega  = turboelectric_generator_conditions.turboshaft.omega
 
    generator_conditions.power     = P_mech # gearbox 
    generator_conditions.omega     = shaft_omega # gearbox 
    compute_generator_performance(generator,generator_conditions,conditions)   
    P_elec                         =  generator_conditions.power
    
    conditions.energy[bus.tag].power_draw =  generator_conditions.power 
    
    # Pack results      
    stored_results_flag    = True
    stored_propulsor_tag   = turboelectric_generator.tag
    
    return P_mech, P_elec,stored_results_flag,stored_propulsor_tag

def reuse_stored_turboelectric_generator_data(turboelectric_generator,state,network,fuel_line,bus,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one turboelectric_generator for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure     [-]  
    fuel_line            - fuelline                                [-] 
    turboelectric_generator           - turboelectric_generator data structure              [-] 
    total_power          - power of turboelectric_generator group               [W] 

    Outputs:  
    total_power          - power of turboelectric_generator group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                         = state.conditions   
    conditions.energy[turboelectric_generator.tag]  = deepcopy(conditions.energy[stored_propulsor_tag])
    conditions.noise[turboelectric_generator.tag]   = deepcopy(conditions.noise[stored_propulsor_tag])
      
    P_mech   = 0 # NEED TO CORRECT conditions.energy[turboelectric_generator.tag].power  
    P_elec   = 0 # NEED TO CORRECT conditions.energy[turboelectric_generator.tag].power   
    return  P_mech, P_elec