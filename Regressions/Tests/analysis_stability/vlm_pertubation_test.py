# vlm_pertubation_test.py
# 
# Created: May 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE 
from RCAIDE.Framework.Core import Units     
from RCAIDE.Library.Plots       import *  

# python imports  
import pylab as plt
import numpy as np 


# local imports 
import sys 
sys.path.append('../../Vehicles')
from Navion    import vehicle_setup, configs_setup     
# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(): 
    
    # vehicle data
    vehicle  = vehicle_setup() 

    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(analyses) 

    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 

    # mission analysis 
    results = missions.base_mission.evaluate() 

    elevator_deflection        = results.segments.climb.conditions.control_surfaces.elevator.deflection[0,0] / Units.deg  
    elevator_deflection_true   = -3.1111958662603465
    elevator_deflection_diff   = np.abs(elevator_deflection - elevator_deflection_true)
    print('Error: ',elevator_deflection_diff)
    assert np.abs(elevator_deflection_diff/elevator_deflection_true) < 1e-3
    

    aileron_deflection        = results.segments.climb.conditions.control_surfaces.aileron.deflection[0,0] / Units.deg  
    aileron_deflection_true   = -2.1598531533493865
    aileron_deflection_diff   = np.abs(aileron_deflection - aileron_deflection_true)
    print('Error: ',aileron_deflection_diff)
    assert np.abs(aileron_deflection_diff/aileron_deflection_true) < 1e-3
    

    rudder_deflection        = results.segments.climb.conditions.control_surfaces.rudder.deflection[0,0] / Units.deg  
    rudder_deflection_true   = -3.4170973783633762
    rudder_deflection_diff   = np.abs(rudder_deflection - rudder_deflection_true)
    print('Error: ',rudder_deflection_diff)
    assert np.abs(rudder_deflection_diff/rudder_deflection_true) < 1e-3    
    

    # plt results
    plot_mission(results)


    return  
# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config, configs)
        analyses[tag] = analysis

    return analyses


def base_analysis(vehicle, configs):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 

    # ------------------------------------------------------------------
    #  Weights
    weights = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = RCAIDE.Framework.Analyses.Aerodynamics.Subsonic_VLM() 
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.number_spanwise_vortices   = 30
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics) 
      
    stability                                   = RCAIDE.Framework.Analyses.Stability.VLM_Perturbation_Method() 
    stability.settings.discretize_control_surfaces  = True
    stability.settings.model_fuselage               = True                
    stability.settings.model_nacelle                = True
        
    stability.configuration                         = configs
    stability.geometry                              = vehicle
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Energy
    energy= RCAIDE.Framework.Analyses.Energy.Energy()
    energy.networks = vehicle.networks  
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses  

def plot_mission(results): 

    # Plot Aircraft Stability 
    plot_longitudinal_stability(results)  
    
    plot_lateral_stability(results) 
    
    plot_flight_forces_and_moments(results) 
      
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

    # base segment
    base_segment = Segments.Segment() 

    # ------------------------------------------------------------------
    #   Climb Segment : Constant Speed Constant Rate
    # ------------------------------------------------------------------ 
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment) 
    segment.tag = "climb"        
    segment.analyses.extend( analyses.base )      
    segment.altitude_start                                = 0.0 * Units.feet
    segment.altitude_end                                  = 12000 * Units.feet
    segment.air_speed                                     = 120 * Units['mph']
    segment.climb_rate                                    = 1000* Units['ft/min']
    segment.sideslip_angle                                = 1 * Units.degrees
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True    
    segment.flight_dynamics.force_z                       = True    
                
    # define flight controls              
    segment.flight_controls.RPM.active                               = True           
    segment.flight_controls.RPM.assigned_propulsors                  = [['ice_propeller']]
    segment.flight_controls.RPM.initial_guess                        = True 
    segment.flight_controls.RPM.initial_guess_values                 = [[2500]] 
    segment.flight_controls.throttle.active                          = True           
    segment.flight_controls.throttle.assigned_propulsors             = [['ice_propeller']]    
    segment.flight_controls.body_angle.active                        = True   
    
    # Longidinal Flight Mechanics
    segment.flight_dynamics.moment_y                                 = True 
    segment.flight_controls.elevator_deflection.active               = True    
    segment.flight_controls.elevator_deflection.assigned_surfaces    = [['elevator']]
    segment.flight_controls.elevator_deflection.initial_guess_values = [[0]]     
   
    # Lateral Flight Mechanics 
    segment.flight_dynamics.force_y                                  = True     
    segment.flight_dynamics.moment_x                                 = True
    segment.flight_dynamics.moment_z                                 = True 
    segment.flight_controls.aileron_deflection.active                = True    
    segment.flight_controls.aileron_deflection.assigned_surfaces     = [['aileron']]
    segment.flight_controls.aileron_deflection.initial_guess_values  = [[0]] 
    segment.flight_controls.rudder_deflection.active                 = True    
    segment.flight_controls.rudder_deflection.assigned_surfaces      = [['rudder']]
    segment.flight_controls.rudder_deflection.initial_guess_values   = [[0]]
    segment.flight_controls.bank_angle.active                        = True    
    segment.flight_controls.bank_angle.initial_guess_values          = [[0]]  
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