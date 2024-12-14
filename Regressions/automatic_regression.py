# Regressions/automatic_regression.py
# 

""" RCAIDE Regressions
"""
# Created:  Jun M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import sys, os, traceback, time
from src.Framework.Core import DataOrdered

sys.path.append(os.path.join(sys.path[0], 'Vehicles'))
sys.path.append(os.path.join(sys.path[0], 'Vehicles' + os.sep + 'Rotors' )) 

modules = [ 
    # ----------------------- Regression List --------------------------
    'Tests/analysis_aerodynamics/airfoil_panel_method_test.py',    
    'Tests/analysis_aerodynamics/airfoil_panel_method_convergence.py',
    'Tests/analysis_aerodynamics/VLM_control_surface_test.py',    
    'Tests/analysis_aerodynamics/VLM_moving_surface_test.py',    
    'Tests/atmosphere/atmosphere.py',
    'Tests/atmosphere/constant_temperature.py',
    'Tests/analysis_emissions/emissions_test.py',   
    'Tests/analysis_noise/digital_elevation_test.py',  
    'Tests/analysis_noise/frequency_domain_test.py', 
    'Tests/analysis_noise/empirical_jet_noise_test.py',    
    'Tests/analysis_stability/trimmed_flight_test.py', 
    'Tests/analysis_stability/untrimmed_flight_test.py', 
    'Tests/analysis_weights/operating_empty_weight_test.py',
    'Tests/analysis_weights/cg_and_moi_test.py',
    'Tests/energy_sources/cell_test.py',
    'Tests/geometry/airfoil_import_test.py', 
    'Tests/geometry/airfoil_interpolation_test.py',    
    'Tests/geometry/wing_volume_test.py',
    'Tests/geometry/wing_fuel_volume_compute.py',
    'Tests/geometry/fuselage_planform_compute.py',    
    'Tests/mission_segments/transition_segment_test.py', 
    'Tests/network_electric/electric_btms_test.py', 
    'Tests/network_ducted_fan/electric_ducted_fan_network_test.py',
    'Tests/network_turbofan/turbofan_network_test.py',
    'Tests/network_turbojet/turbojet_network_test.py',
    'Tests/network_turboprop/turboprop_network_test.py',
    'Tests/network_turboshaft/turboshaft_network_test.py',
    'Tests/network_internal_combustion_engine/ICE_test.py',
    'Tests/network_internal_combustion_engine/ICE_constant_speed_test.py',
    'Tests/optimization/optimization_packages.py',
    'Tests/performance/landing_field_length.py',
    'Tests/performance/payload_range_test.py',
    'Tests/performance/take_off_field_length.py',
    'Tests/performance/take_off_weight_from_tofl.py',    
]

def regressions():
     
    # preallocate test results
    results = DataOrdered()
    for module in modules:
        results[module] = 'Untested'

    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('#   RCAIDE-UIUC Automatic Regression \n')
    sys.stdout.write('#   %s \n' % time.strftime("%B %d, %Y - %H:%M:%S", time.gmtime()) )
    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write(' \n')

    # run tests
    all_pass = True
    for module in modules:
        passed = test_module(module)
        if passed:
            results[module] = '  Passed'
        else:
            results[module] = '* FAILED'
            all_pass = False

    # final report
    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('Final Results \n')
    for module,result in list(results.items()):
        sys.stdout.write('%s - %s\n' % (result,module))

    if all_pass:
        sys.exit(0)
    else:
        sys.exit(1)
        
    return pass_fail 
 
# ----------------------------------------------------------------------
#   Module Tester
# ----------------------------------------------------------------------

def test_module(module_path):
    original_dir = os.getcwd()
    
    try:
        # Get regression directory (where this script is)
        regression_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(regression_dir)
        
        # Convert module_path to full path from regression directory
        full_module_path = os.path.join(regression_dir, module_path)
        test_dir = os.path.dirname(full_module_path)
        module_name = os.path.basename(module_path)
        
        sys.stdout.write('# --------------------------------------------------------------------- \n')
        sys.stdout.write('# Start Test: %s \n' % full_module_path)
        sys.stdout.flush()
        
        tic = time.time()
        
        # Check if file exists
        if not os.path.exists(full_module_path):
            raise ImportError(f'file {full_module_path} does not exist')
        
        # Add test directory to Python path and change to it
        if test_dir:
            sys.path.append(test_dir)
            os.chdir(test_dir)
        
        # Import and run the test
        name = os.path.splitext(module_name)[0]
        module = __import__(name)
        module.main()
        
        passed = True
        
    except Exception as exc:
        sys.stderr.write('Test Failed: \n')
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write('\n')
        sys.stderr.flush()
        passed = False
        
    finally:
        # Cleanup
        plt.close('all')
        os.chdir(original_dir)
        
        # Log results
        if passed:
            sys.stdout.write('# Passed: %s \n' % module_name)
        else:
            sys.stdout.write('# FAILED: %s \n' % module_name)
        sys.stdout.write('# Test Duration: %.4f min \n' % ((time.time()-tic)/60))
        sys.stdout.write('\n')
        
        # Ensure output is written
        sys.stdout.flush()
        sys.stderr.flush()
        
    return passed
 

if __name__ == '__main__':
    regressions()