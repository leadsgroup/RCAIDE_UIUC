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
from Hydrogen_Fuel_Cell_Twin_Otter   import vehicle_setup , configs_setup  

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  

def main(): 
    low_fidelity_discharge_model()
    medium_fidelity_discharge_model()
    
    return 
      
def low_fidelity_discharge_model(): 
 
    mdot_H2_true        = 0.05853883881516223
    fuel_cell_model     = 'Larminie'
    
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
    mdot_H2       = results.segments[0].conditions.energy.bus.fuel_cell_stacks['fuel_cell'].fuel_cell.inputs.fuel_mass_flow_rate[0,0]
    print('Mass Flow Rate: ' + str(mdot_H2))
    mdot_H2_diff   = np.abs(mdot_H2 - mdot_H2_true) 
    print(mdot_H2_diff) 
    assert np.abs((mdot_H2_diff)/mdot_H2_true) < 1e-6  
        
    return

def medium_fidelity_discharge_model():
    
    mdot_H2_true        = 2.2805644236790175e-10
    fuel_cell_model     = 'PEM'
    
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