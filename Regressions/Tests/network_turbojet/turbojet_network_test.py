# Regression/scripts/Tests/turbofan_network_test.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                          import Units , Data 
from RCAIDE.Library.Plots                           import *       
from RCAIDE.Library.Methods.Noise.Boom.lift_equivalent_area import lift_equivalent_area

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from Concorde    import vehicle_setup as vehicle_setup
from Concorde    import configs_setup as configs_setup 

# ----------------------------------------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------------------------------------

def main():
    

    # vehicle data
    vehicle  = vehicle_setup() 
    
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
    
    ## plt the old results
    plot_mission(results)   
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
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)
    
    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics                                       = RCAIDE.Framework.Analyses.Aerodynamics.Supersonic_VLM()
    aerodynamics.geometry                              = vehicle
    aerodynamics.settings.number_of_spanwise_vortices  = 5
    aerodynamics.settings.number_of_chordwise_vortices = 2       
    aerodynamics.settings.model_fuselage               = True
    aerodynamics.settings.drag_coefficient_increment   = 0.0000
    analyses.append(aerodynamics) 
    
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

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results):
    
    plot_altitude_sfc_weight(results) 
    
    plot_flight_conditions(results) 
    
    plot_aerodynamic_coefficients(results)  
    
    plot_aircraft_velocities(results)
    
    plot_drag_components(results)
    return

def simple_sizing(configs):
    
    base = configs.base
    base.pull_base()
    
    # zero fuel weight
    base.mass_properties.max_zero_fuel = 0.9 * base.mass_properties.max_takeoff 
    
    # fuselage seats
    base.fuselages['fuselage'].number_coach_seats = base.passengers
    
    # diff the new data
    base.store_diff()
    
    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------
    landing = configs.landing
    
    # make sure base data is current
    landing.pull_base()
    
    # landing weight
    landing.mass_properties.landing = 0.85 * base.mass_properties.takeoff
    
    # diff the new data
    landing.store_diff()
    
    # done!
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
    
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1" 
    segment.analyses.extend( analyses.climb ) 
    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 4000. * Units.ft
    segment.airpseed       = 250.  * Units.kts
    segment.climb_rate     = 4000. * Units['ft/min']
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                   
      
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------    
    
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end = 8000. * Units.ft
    segment.airpseed     = 250.  * Units.kts
    segment.climb_rate   = 2000. * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------    
    
    segment = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "climb_2" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end        = 33000. * Units.ft
    segment.mach_number_start   = .45
    segment.mach_number_end     = 0.95
    segment.climb_rate          = 3000. * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                 
    
    mission.append_segment(segment)    

    # ------------------------------------------------------------------
    #   Third Climb Segment: linear Mach, constant segment angle 
    # ------------------------------------------------------------------    
      
    segment = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "climb_3" 
    segment.analyses.extend( analyses.climb ) 
    segment.altitude_end        = 34000. * Units.ft
    segment.mach_number_start   = 0.95
    segment.mach_number_end     = 1.1
    segment.climb_rate          = 2000.  * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment) 

    # ------------------------------------------------------------------
    #   Third Climb Segment: linear Mach, constant segment angle 
    # ------------------------------------------------------------------   
    segment     = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "climb_4" 
    segment.analyses.extend( analyses.climb ) 
    segment.altitude_end        = 40000. * Units.ft
    segment.mach_number_start   = 1.1
    segment.mach_number_end     = 1.7
    segment.climb_rate          = 1750.  * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                 
    
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------
    #   Fourth Climb Segment: linear Mach, constant segment angle 
    # ------------------------------------------------------------------  
    segment = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "climb_5" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end        = 50000. * Units.ft
    segment.mach_number_start   = 1.7
    segment.mach_number_end     = 2.02
    segment.climb_rate          = 750.  * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                  
    
    mission.append_segment(segment)     
    

    # ------------------------------------------------------------------
    #   Fourth Climb Segment: linear Mach, constant segment angle 
    # ------------------------------------------------------------------  
    segment = Segments.Climb.Constant_Mach_Constant_Rate(base_segment)
    segment.tag = "climbing_cruise" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end                                  = 56500. * Units.ft
    segment.mach_number                                   = 2.02
    segment.climb_rate                                    = 50.  * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed 
    # ------------------------------------------------------------------    
    segment     = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag = "level_cruise" 
    segment.analyses.extend( analyses.cruise ) 
    segment.mach_number                                   = 2.02
    segment.distance                                      = 10. * Units.nmi
    segment.state.numerics.number_control_points          = 4  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)    
    
    # ------------------------------------------------------------------
    #   First Descent Segment: decceleration
    # ------------------------------------------------------------------    
    segment     = Segments.Cruise.Constant_Acceleration_Constant_Altitude(base_segment)
    segment.tag = "decel_1" 
    segment.analyses.extend( analyses.cruise )
    segment.acceleration                                  = -.5  * Units['m/s/s']
    segment.air_speed_end                                 = 1.5*573.  * Units.kts 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                 
     
    mission.append_segment(segment)   
    
    # ------------------------------------------------------------------
    #   First Descent Segment
    # ------------------------------------------------------------------  
    segment     = Segments.Descent.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "descent_1" 
    segment.analyses.extend( analyses.cruise )
    segment.altitude_end      = 41000. * Units.ft
    segment.mach_number_end   = 1.3
    segment.descent_rate      = 2000. * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)     
    
    # ------------------------------------------------------------------
    #   First Descent Segment: decceleration
    # ------------------------------------------------------------------   
    segment     = Segments.Cruise.Constant_Acceleration_Constant_Altitude(base_segment)
    segment.tag = "decel_2" 
    segment.analyses.extend( analyses.cruise )
    segment.acceleration      = -.5  * Units['m/s/s']
    segment.air_speed_end     = 0.95*573.  * Units.kts  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                   
    
    mission.append_segment(segment)     
    
    # ------------------------------------------------------------------
    #   First Descent Segment
    # ------------------------------------------------------------------    
      
    segment = Segments.Descent.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "descent_2" 
    segment.analyses.extend( analyses.cruise )
    segment.altitude_end      = 10000. * Units.ft
    segment.mach_number_end   = 250./638. 
    segment.descent_rate      = 2000. * Units['ft/min']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)     
    
    # ------------------------------------------------------------------
    #   First Descent Segment
    # ------------------------------------------------------------------     
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3" 
    segment.analyses.extend( analyses.cruise )
    segment.altitude_end = 0. * Units.ft
    segment.air_speed    = 250. * Units.kts
    segment.descent_rate = 1000. * Units['ft/min']    
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['inner_right_turbojet','outer_right_turbojet','outer_left_turbojet','inner_left_turbojet']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)      
    
    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    return mission

def missions_setup(mission):

    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
    
    # done!
    return missions  
    
def check_results(new_results,old_results):

    # check segment values
    check_list = [
        'segments.climbing_cruise.conditions.aerodynamics.angles.alpha',
        'segments.climbing_cruise.conditions.aerodynamics.coefficients.drag',
        'segments.climbing_cruise.conditions.aerodynamics.coefficients.lift', 
        'segments.climbing_cruise.conditions.weights.vehicle_mass_rate', 
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = np.max( old_results.deep_get(k) )
        new_val = np.max( new_results.deep_get(k) )
        err = (new_val-old_val)/old_val
        print('Error at Max:' , err)
        assert np.abs(err) < 1e-6 , 'Max Check Failed : %s' % k

        old_val = np.min( old_results.deep_get(k) )
        new_val = np.min( new_results.deep_get(k) )
        err = (new_val-old_val)/old_val
        print('Error at Min:' , err)
        assert np.abs(err) < 1e-6 , 'Min Check Failed : %s' % k        

        print('') 

    return 

if __name__ == '__main__': 
    main()    
    plt.show()
        
