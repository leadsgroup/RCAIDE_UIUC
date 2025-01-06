# Regression/scripts/Tests/analysis_weights/cg_and_moi_test.py
# 
# Created:  Oct 2024, A. Molloy
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# cg_and_moi_test.py

from RCAIDE.Framework.Core                                                   import Units,  Data  
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_aircraft_moment_of_inertia import compute_aircraft_moment_of_inertia
from RCAIDE.Library.Methods.Weights.Center_of_Gravity                        import compute_vehicle_center_of_gravity
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia                        import compute_cuboid_moment_of_inertia

import numpy as  np
import RCAIDE
import sys   
import os

sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))

# the analysis functions
from Lockheed_C5a           import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup
from Stopped_Rotor_EVTOL    import vehicle_setup as EVTOL_setup

def main(): 
    # make true only when resizing aircraft. should be left false for regression
    update_regression_values = False    
    Transport_Aircraft_Test()
    General_Aviation_Test()
    EVTOL_Aircraft_Test(update_regression_values)
    return

def Transport_Aircraft_Test():
    vehicle = transport_setup()
    
    # update fuel weight to 60%
    vehicle.networks.fuel.fuel_lines.fuel_line.fuel_tanks.wing_fuel_tank.fuel.mass_properties.mass = 0.6 * vehicle.networks.fuel.fuel_lines.fuel_line.fuel_tanks.wing_fuel_tank.fuel.mass_properties.mass

    # ------------------------------------------------------------------
    #   Weight Breakdown 
    # ------------------------------------------------------------------  
    weight_analysis                               = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weight_analysis.vehicle                       = vehicle
    weight_analysis.method                        = 'Raymer'
    weight_analysis.settings.use_max_fuel_weight  = False  
    results                                       = weight_analysis.evaluate() 
    
    # ------------------------------------------------------------------
    #   CG Location
    # ------------------------------------------------------------------    
    CG_location, _ = compute_vehicle_center_of_gravity( weight_analysis.vehicle)  
    
    # ------------------------------------------------------------------
    #   Operating Aircraft MOI
    # ------------------------------------------------------------------    
    MOI, total_mass = compute_aircraft_moment_of_inertia(weight_analysis.vehicle, CG_location)

    # ------------------------------------------------------------------
    #   Payload MOI
    # ------------------------------------------------------------------    
    Cargo_MOI, mass =  compute_cuboid_moment_of_inertia(CG_location, 99790*Units.kg, 36.0, 3.66, 3, 0, 0, 0, CG_location)
    MOI             += Cargo_MOI
    total_mass      += mass
    
    print(weight_analysis.vehicle.tag + ' Moment of Intertia')
    print(MOI) 
    accepted  = np.array([[32501492.04259999, 2589698.27591836, 3358696.7542382],
                          [2589698.2759183585, 41119945.59273668, 1.4551915228366852e-11],
                          [3358696.7542382046, 1.4551915228366852e-11, 60277432.14411559]]) 
    MOI_error     = MOI - accepted

    # Check the errors
    error = Data()
    error.Ixx   = MOI_error[0, 0]
    error.Iyy   = MOI_error[1, 1]
    error.Izz   = MOI_error[2, 2]
    error.Ixz   = MOI_error[2, 0]
    error.Ixy   = MOI_error[1, 0]

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6) 
    
    return  
 

def General_Aviation_Test(): 
    # ------------------------------------------------------------------
    #   Weight Breakdown 
    # ------------------------------------------------------------------  
    weight_analysis           = RCAIDE.Framework.Analyses.Weights.Weights_General_Aviation()
    weight_analysis.vehicle   = general_aviation_setup() 
    results                   = weight_analysis.evaluate() 
    
    # ------------------------------------------------------------------
    #   CG Location
    # ------------------------------------------------------------------    
    CG_location, _ = compute_vehicle_center_of_gravity(weight_analysis.vehicle)  
    
    # ------------------------------------------------------------------
    #   Operating Aircraft MOI
    # ------------------------------------------------------------------    
    MOI, total_mass = compute_aircraft_moment_of_inertia(weight_analysis.vehicle, CG_location) 

    print(weight_analysis.vehicle.tag + ' Moment of Intertia')
    print(MOI)
     
    accepted  = np.array([[3100.453417318488, 9.410206211118789, -12.357610137252777],
                          [  9.410206211118789, 4302.514821394567,    0.        ],
                          [ -12.357610137252777,    0.        , 3745.1500603319455]])
    
    MOI_error     = MOI - accepted

    # Check the errors
    error       = Data()
    error.Ixx   = MOI_error[0, 0]
    error.Iyy   = MOI_error[1, 1]
    error.Izz   = MOI_error[2, 2]
    error.Ixz   = MOI_error[2, 0]
    error.Ixy   = MOI_error[1, 0]

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)   
    
    return

def EVTOL_Aircraft_Test(update_regression_values):
    vehicle = EVTOL_setup(update_regression_values)
    
    # ------------------------------------------------------------------
    #   Weight Breakdown 
    # ------------------------------------------------------------------  
    weight_analysis          = RCAIDE.Framework.Analyses.Weights.Weights_EVTOL()
    weight_analysis.vehicle  = vehicle
    results                  = weight_analysis.evaluate() 
    
    # ------------------------------------------------------------------
    #   CG Location
    # ------------------------------------------------------------------    
    CG_location, _ =  compute_vehicle_center_of_gravity( weight_analysis.vehicle)  
    
    # ------------------------------------------------------------------
    #   Operating Aircraft MOI
    # ------------------------------------------------------------------    
    MOI, total_mass = compute_aircraft_moment_of_inertia(weight_analysis.vehicle, CG_location)
    
    print(weight_analysis.vehicle.tag + ' Moment of Intertia')
    print(MOI) 
    accepted  = np.array([[6165.3741424348045,-599.5553934443328, -727.0671702223518],
                          [-599.5553934443328, 9530.162546879752,  -96.17454446468206],
                          [ -727.0671702223518,  -96.17454446468206, 14313.643487247744]])
    MOI_error     = MOI - accepted

    # Check the errors
    error = Data()
    error.Ixx   = MOI_error[0, 0]
    error.Iyy   = MOI_error[1, 1]
    error.Izz   = MOI_error[2, 2]
    error.Ixz   = MOI_error[2, 0]
    error.Ixy   = MOI_error[1, 0]

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-5) 
    
    return  

if __name__ == '__main__':
    main()


