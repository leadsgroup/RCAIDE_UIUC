# Regressions/automatic_regression.py
# 

""" RCAIDE Regressions
"""
# Created:  Jun M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Framework.Core import DataOrdered
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import sys, os, traceback, time 
 
modules = [ 
    # ----------------------- Regression List --------------------------
    'Tests/analysis_aerodynamics/airfoil_panel_method_test.py',  
    'Tests/analysis_noise/digital_elevation_test.py',  
    'Tests/analysis_noise/frequency_domain_test.py', 
    'Tests/analysis_noise/empirical_jet_noise_test.py',     
    'Tests/analysis_noise/noise_hemisphere_test.py', 
    'Tests/analysis_stability/vlm_pertubation_test.py', 
    'Tests/geometry_airfoils/airfoil_import_test.py', 
    'Tests/geometry_airfoils/airfoil_interpolation_test.py',    
    'Tests/mission_segments/segment_test.py',    
    'Tests/network_all_electric/all_electric_rotor_test.py',  
    'Tests/network_turbofan/turbofan_network_test.py',
    'Tests/network_turbojet/turbojet_network_test.py',
    'Tests/network_internal_combustion_engine/ICE_test.py',
    'Tests/network_internal_combustion_engine/ICE_constant_speed_test.py',
    'Tests/network_isolated_battery_cell/cell_test.py', 
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

    home_dir = os.getcwd()
    test_dir, module_name = os.path.split( os.path.abspath(module_path) )

    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('# Start Test: %s \n' % module_path)
    sys.stdout.flush()

    tic = time.time()

    # try the test
    try:

        # see if file exists
        os.chdir(test_dir)
        if not os.path.exists(module_name) and not os.path.isfile(module_name):
            raise ImportError('file %s does not exist' % module_name)

        # add module directory
        sys.path.append(test_dir)

        # do the import
        name = os.path.splitext(module_name)[0]
        module = __import__(name)

        # run main function
        module.main()

        passed = True

    # catch an error
    except Exception as exc:

        # print traceback
        sys.stderr.write( 'Test Failed: \n' )
        sys.stderr.write( traceback.format_exc() )
        sys.stderr.write( '\n' )
        sys.stderr.flush()

        passed = False

    # final result
    if passed:
        sys.stdout.write('# Passed: %s \n' % module_name)
    else:
        sys.stdout.write('# FAILED: %s \n' % module_name)
    sys.stdout.write('# Test Duration: %.4f min \n' % ((time.time()-tic)/60) )
    sys.stdout.write('\n')

    # cleanup
    plt.close('all')
    os.chdir(home_dir)

    # make sure to write to stdout
    sys.stdout.flush()
    sys.stderr.flush()

    return passed
 

if __name__ == '__main__':
    regressions()