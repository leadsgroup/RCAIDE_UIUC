# Regression/scripts/network_isolated_battery_cell/cell_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Core   import Units, Data   
from RCAIDE.Library.Plots    import *  
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Cell_Stacks.Generic  import  initialize_from_power, initialize_larminie_from_power



# package imports  
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.cm as cm

# local imports 
import sys 
import os
import numpy as np
import matplotlib.pyplot as plt 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Fuel_Cell   import vehicle_setup , configs_setup  

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  

def main():
    low_fidelity_simple_discharge_model()
    low_fidelity_larminie_discharge_model()
    medium_fidelity_discharge_model()
    
    return 
    
def low_fidelity_simple_discharge_model(): 
    power                         = np.array([200]) 
    fuel_cell_model = 'Simple'
    vehicle  = vehicle_setup(fuel_cell_model) 
    fuel_cell_stack   =  vehicle.networks.electric.busses.bus.fuel_cell_stacks.fuel_cell
    initialize_from_power(fuel_cell_stack, power)  

    # Step 28: Static Sea Level Thrust  
    planet                                            = RCAIDE.Library.Attributes.Planets.Earth()
    atmosphere_sls                                    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data                                         = atmosphere_sls.compute_values(0.0,0.0)
                                                      
    p                                                 = atmo_data.pressure          
    T                                                 = atmo_data.temperature       
    rho                                               = atmo_data.density          
    a                                                 = atmo_data.speed_of_sound    
    mu                                                = atmo_data.dynamic_viscosity     
                                                      
    conditions                                        = RCAIDE.Framework.Mission.Common.Results() 
    conditions.freestream.altitude                    = np.atleast_1d(0)
    conditions.freestream.mach_number                 = np.atleast_1d(0.01)
    conditions.freestream.pressure                    = np.atleast_1d(p)
    conditions.freestream.temperature                 = np.atleast_1d(T)
    conditions.freestream.density                     = np.atleast_1d(rho)
    conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
    conditions.freestream.gravity                     = np.atleast_2d(planet.sea_level_gravity) 
    conditions.freestream.speed_of_sound              = np.atleast_1d(a)
    conditions.freestream.velocity                    = np.atleast_1d(a*0.01)   
 
    # setup conditions   
    segment                                           = RCAIDE.Framework.Mission.Segments.Segment()  
    segment.state.conditions                          = conditions

    bus  = vehicle.networks.electric.busses.bus
    bus.append_operating_conditions(segment)      
    for fuel_cell_stack in  bus.fuel_cell_stacks: 
        fuel_cell_stack.append_operating_conditions(segment,bus) 
    segment.state.conditions.energy[bus.tag].power_draw = np.array([[100]])  
    coolant_lines = vehicle.networks.electric.coolant_lines
    t_idx         =  0
    delta_t       =  0
    
    _,_         = fuel_cell_stack.energy_calc(segment.state,bus,coolant_lines, t_idx, delta_t)
    mdot0       =  conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.fuel_mass_flow_rate[t_idx]
    mdot0_truth = 1.0844928369248122e-06
    m0          = fuel_cell_stack.mass_properties.mass
    m0_truth    = 0.09615384615384616
    err_mdot0   = (mdot0 - mdot0_truth)/mdot0_truth
    err_m0      = (m0 - m0_truth)/m0_truth

    err       = Data()
    err.fuel_cell_mass_error          = err_m0
    err.fuel_cell_fidelity_zero_error = err_mdot0 
    for k,v in list(err.items()):
        assert(np.abs(v)<1E-6)    
    return  
    
    
def low_fidelity_larminie_discharge_model():

    power                         = np.array([200]) 
    fuel_cell_model = 'Larminie'
    vehicle  = vehicle_setup(fuel_cell_model) 
    fuel_cell_stack   =  vehicle.networks.electric.busses.bus.fuel_cell_stacks.fuel_cell
    initialize_from_power(fuel_cell_stack, power)  

    # Step 28: Static Sea Level Thrust  
    planet                                            = RCAIDE.Library.Attributes.Planets.Earth()
    atmosphere_sls                                    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data                                         = atmosphere_sls.compute_values(0.0,0.0)
                                                      
    p                                                 = atmo_data.pressure          
    T                                                 = atmo_data.temperature       
    rho                                               = atmo_data.density          
    a                                                 = atmo_data.speed_of_sound    
    mu                                                = atmo_data.dynamic_viscosity     
                                                      
    conditions                                        = RCAIDE.Framework.Mission.Common.Results() 
    conditions.freestream.altitude                    = np.atleast_1d(0)
    conditions.freestream.mach_number                 = np.atleast_1d(0.01)
    conditions.freestream.pressure                    = np.atleast_1d(p)
    conditions.freestream.temperature                 = np.atleast_1d(T)
    conditions.freestream.density                     = np.atleast_1d(rho)
    conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
    conditions.freestream.gravity                     = np.atleast_2d(planet.sea_level_gravity) 
    conditions.freestream.speed_of_sound              = np.atleast_1d(a)
    conditions.freestream.velocity                    = np.atleast_1d(a*0.01)   
 
    # setup conditions   
    segment                                           = RCAIDE.Framework.Mission.Segments.Segment()  
    segment.state.conditions                          = conditions

    bus  = vehicle.networks.electric.busses.bus
    bus.append_operating_conditions(segment)      
    for fuel_cell_stack in  bus.fuel_cell_stacks: 
        fuel_cell_stack.append_operating_conditions(segment,bus) 
    segment.state.conditions.energy[bus.tag].power_draw = np.array([[100]])  
    coolant_lines = vehicle.networks.electric.coolant_lines
    t_idx         =  0
    delta_t       =  0
        
    _,_            = fuel_cell_stack.energy_calc(segment.state,bus,coolant_lines, t_idx, delta_t)
    mdot1          = conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag].fuel_cell.inputs.fuel_mass_flow_rate[t_idx,0]
    mdot1_truth    = 1.0844928369248122e-06
    err_mdot1      = (mdot1 - mdot1_truth)/mdot1_truth 
    
    err       = Data() 
    err.fuel_cell_larminie_error      = err_mdot1
    for k,v in list(err.items()):
        assert(np.abs(v)<1E-6)
        
    return 

def medium_fidelity_discharge_model():
    
 
    mdot_H2_true        = 5.182152666217547e-13
    fuel_cell_model     =  'PEM'
    
    vehicle  = vehicle_setup(fuel_cell_model) 
    
    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(analyses,configs) 
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 
     
    # mission analysis 
    results = missions.base_mission.evaluate()  
    
    # Voltage Cell Regression
    mdot_H2       = results.segments[0].conditions.energy.bus.fuel_cell_stacks['pem_fuel_cell'].fuel_cell.inputs.fuel_mass_flow_rate[0,0]
    print('Mass Flow Rate: ' + str(mdot_H2))
    mdot_H2_diff   = np.abs(mdot_H2 - mdot_H2_true) 
    print(mdot_H2_diff) 
    assert np.abs((mdot_H2_diff)/mdot_H2_true) < 1e-6  
        
    return  
 
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):    
    #   Initialize the Analyses     
    analyses = RCAIDE.Framework.Analyses.Vehicle()  
    
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)
 
    #  Planet Analysis
    planet  = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)
 
    #  Atmosphere Analysis
    atmosphere                 = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses     

def mission_setup(analyses,vehicle):
 
    #   Initialize the Mission 
    mission            = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag        = 'fuel_cell_cycle_test'   
    Segments           = RCAIDE.Framework.Mission.Segments 
    base_segment       = Segments.Segment()    

    # Charge Segment 
    segment                                 = Segments.Ground.Discharge(base_segment)      
    segment.analyses.extend(analyses.base)
    segment.throttle =  1.0 
    segment.tag                             = 'Discharge' 
    mission.append_segment(segment)    
     
    
    return mission 

def missions_setup(mission): 
 
    missions         = RCAIDE.Framework.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  
 
if __name__ == '__main__':
    main()
    plt.show()