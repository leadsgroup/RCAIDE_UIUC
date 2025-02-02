  
# Regression/scripts/Tests/network_ducted_fan/electric_ducted_fan_netowrk.py
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                          import Units , Data 
from RCAIDE.Library.Plots                           import *        

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  
import os

# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from NASA_X48    import vehicle_setup as vehicle_setup
from NASA_X48    import configs_setup as configs_setup 

# ----------------------------------------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------------------------------------

def main():

    regression_flag = False # Keep true for regression on Appveyor
    ducted_fan_type  = ['Blade_Element_Momentum_Theory', 'Rankine_Froude_Momentum_Theory']
    
    # truth values 
    thrust_truth         = [36.455819245889195,37.653244590335106] # CORRECT MATTEO 
    efficiency_truth     = [145.0992694988849,145.7740091588354]  # CORRECT MATTEO 
    current_truth        = [73.5454727365098,73.0]  # CORRECT MATTEO  
 
    for i in range(len(ducted_fan_type)):  
        # vehicle data
        vehicle  = vehicle_setup(regression_flag, ducted_fan_type[i]) 
        
        # Set up vehicle configs
        configs  = configs_setup(vehicle)
    
        # create analyses
        analyses = analyses_setup(configs)
    
        # mission analyses 
        mission = mission_setup(analyses)
        
        # create mission instances (for multiple types of missions)
        missions = missions_setup(mission) 
         
        # mission analysis 
        results = missions.base_mission.evaluate()   
        
        
        if ducted_fan_type[i] ==  'Blade_Element_Momentum_Theory':  
            if regression_flag: # if regression skip test since we cannot run DFDC 
                error = Data()
                error.current     = 0
                error.efficiency  = 0
                error.current     = 0 
            else:  
                thurst      =  np.linalg.norm(results.segments.cruise.conditions.energy['center_propulsor'].thrust, axis=1)
                efficiency  =  results.segments.cruise.conditions.conditions.energy['electric_ducted_fan']['ducted_fan'].efficiency
                current     =  results.segments.cruise.conditions.conditions.energy['electric_ducted_fan']['motor'].current
                
                error = Data()
                error.current     = np.max(np.abs(thrust_truth[i]   - thurst[0][0]  ))
                error.efficiency  = np.max(np.abs(efficiency_truth[i]  - efficiency[0][0] ))
                error.current     = np.max(np.abs(current_truth[i] - current[0][0]))                 
                
        elif ducted_fan_type[i] ==  'Rankine_Froude_Momentum_Theory':  
            thurst      =  np.linalg.norm(results.segments.cruise.conditions.conditions.energy['electric_ducted_fan'].thrust, axis=1)
            efficiency  =  results.segments.cruise.conditions.conditions.energy['electric_ducted_fan']['ducted_fan'].efficiency
            current     =  results.segments.cruise.conditions.conditions.energy['electric_ducted_fan']['motor'].current
                
            error = Data()
            error.current       = np.max(np.abs(thrust_truth[i]   - thurst[0][0]  ))
            error.efficiency    = np.max(np.abs(efficiency_truth[i]  - efficiency[0][0] ))
            error.current       = np.max(np.abs(current_truth[i] - current[0][0]))          
        
        
        print('Errors:')
        print(error)
        
        for k,v in list(error.items()):
            assert(np.abs(v)<1e-6) 
    return 

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):
    
    analyses = RCAIDE.Framework.Analyses.Analysis.Container()
    
    # build a base analysis for each config
    for tag,config in list(configs.items()):
        analysis = base_analysis(config)
        analyses[tag] = analysis
    
    return analyses

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_UAV()
    weights.vehicle = vehicle
    analyses.append(weights)
    
    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics                                       = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics.vehicle                               = vehicle
    aerodynamics.settings.number_of_spanwise_vortices  = 25
    aerodynamics.settings.number_of_chordwise_vortices = 5       
    aerodynamics.settings.model_fuselage               = False
    aerodynamics.settings.drag_coefficient_increment   = 0.0000
    analyses.append(aerodynamics)
 
  
    # ------------------------------------------------------------------
    #  Energy
    energy= RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)
    
    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)
    
    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
    
    # done!
    return analyses    

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results):
      
    
    # Plot Electric Motor and Propeller Efficiencies 
    plot_electric_propulsor_efficiencies(results)
    
        
    return 

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
    
def mission_setup(analyses):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    
    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
     
    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments 
    base_segment = Segments.Segment()
    
    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------
    
    segment = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude       = 1000 * Units.feet
    segment.mach_number    = 0.2   * Units.kts
    segment.distance       = 1000 * Units.feet  
    segment.initial_battery_state_of_charge                          = 1.0 
                
    # define flight dynamics to model             
    segment.flight_dynamics.force_x                                  = True  
    segment.flight_dynamics.force_z                                  = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['center_propulsor','starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                   
      
    mission.append_segment(segment) 
    return mission

def missions_setup(mission):

    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
    
    # done!
    return missions


if __name__ == '__main__': 
    main()    
    plt.show()
        
    
        
