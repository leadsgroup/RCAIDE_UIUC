# weights.py
import  RCAIDE
from RCAIDE.Framework.Core import Data  
# from RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups import Propulsion       as Propulsion
# from RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups import Transport        as Transport
# from RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups import Common           as Common
# from RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups import General_Aviation as General_Aviation
# from RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups import BWB              as BWB
# from RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups import UAV              as UAV
#from RCAIDE.Library.Methods.Mass_Properties.Physics_Based_Buildups import Electric       as Electric
from RCAIDE.Library.Plots import * 
from RCAIDE.load import load as load_results
from RCAIDE.save import save as save_results 

import numpy as  np 
import sys
import os

sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
# the analysis functions

from Boeing_737             import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup
from Boeing_BWB_450         import vehicle_setup as bwb_setup
from Stopped_Rotor_EVTOL    import vehicle_setup as evtol_setup
from Solar_UAV              import vehicle_setup as uav_setup
from Human_Powered_Glider   import vehicle_setup as hp_setup

def main():
    update_regression_values = False  # should be false unless code functionally changes
    show_figure              = False # leave false for regression
    
    Transport_Aircraft_Test(update_regression_values,show_figure)
    BWB_Aircraft_Test(update_regression_values,show_figure)
    General_Aviation_Test(update_regression_values,show_figure)
    EVTOL_Aircraft_Test(update_regression_values,show_figure)
    return


def Transport_Aircraft_Test(update_regression_values,show_figure):  
    method_types = ['FLOPS', 'FLOPS', 'Raymer']
    FLOPS_number = 0

    for method_type in method_types:
        print('Testing Method: '+method_type) 
        
        weight_analysis                               = RCAIDE.Framework.Analyses.Weights.Conventional()
        weight_analysis.vehicle                       = transport_setup() 
        weight_analysis.method                        = method_type 

        if ((method_type == 'FLOPS') and (FLOPS_number == 0)):
            FLOPS_number += 1
            weight_analysis.settings.FLOPS.complexity  = 'Simple' 
            method_type = 'FLOPS_Simple'
        elif ((method_type == 'FLOPS') and (FLOPS_number == 1)):
            FLOPS_number += 1
            weight_analysis.settings.FLOPS.complexity  = 'Complex' 
            method_type = 'FLOPS_Complex'
        weight                                        = weight_analysis.evaluate()
        plot_weight_breakdown(weight_analysis.vehicle, show_figure = show_figure) 
    
        if update_regression_values:
            save_results(weight, os.path.join(os.path.dirname(__file__), 'weights_'+method_type.replace(' ','_')+'.res'))
        old_weight = load_results(os.path.join(os.path.dirname(__file__), 'weights_'+method_type.replace(' ','_')+'.res'))
    
        check_list = [
            'payload.total',        
            'payload.passengers',             
            'payload.baggage',                                   
            'empty.structural.wings',            
            'empty.structural.fuselage',        
            'empty.propulsion.total',      
            'empty.structural.landing_gear',                    
            'empty.systems.total',          
            'empty.total',  
        ]
    
        # do the check
        for k in check_list:
            print(k) 
            old_val = old_weight.deep_get(k)
            new_val = weight.deep_get(k)
            err = (new_val-old_val)/old_val
            print('Error:' , err)
            assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     
    
            print('')
            
    return 

def General_Aviation_Test(update_regression_values,show_figure):
     
    weight_analysis          = RCAIDE.Framework.Analyses.Weights.Conventional()
    weight_analysis.vehicle  = general_aviation_setup()
    weight_analysis.aircraft_type = 'General_Aviation'
    weight_analysis.method   = 'FLOPS'
    weight                   = weight_analysis.evaluate()
    plot_weight_breakdown(weight_analysis.vehicle, show_figure = show_figure) 
    
    if update_regression_values:
        save_results(weight, os.path.join(os.path.dirname(__file__), 'weights_General_Aviation.res'))
    old_weight = load_results(os.path.join(os.path.dirname(__file__), 'weights_General_Aviation.res'))

    check_list = [
        'empty.total',
        'empty.structural.wings',
        'empty.structural.fuselage',
        'empty.structural.total',
        'empty.propulsion.total',   
        'empty.systems.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = old_weight.deep_get(k)
        new_val = weight.deep_get(k)
        err = (new_val-old_val)/old_val
        print('Error:' , err)
        assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        print('')
    return 
        
def BWB_Aircraft_Test(update_regression_values,show_figure):
    
    weight_analysis          = RCAIDE.Framework.Analyses.Weights.Conventional()
    weight_analysis.vehicle  = bwb_setup()
    weight_analysis.aircraft_type = 'BWB'
    weight                   = weight_analysis.evaluate()
    plot_weight_breakdown(weight_analysis.vehicle, show_figure = show_figure) 
    
    if update_regression_values:
        save_results(weight, os.path.join(os.path.dirname(__file__), 'weights_BWB.res'))
    old_weight = load_results(os.path.join(os.path.dirname(__file__), 'weights_BWB.res'))
    
    check_list = [
        'empty.total',
        'empty.structural.wings', 
        'empty.structural.total',
        'empty.propulsion.total',   
        'empty.systems.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = old_weight.deep_get(k)
        new_val = weight.deep_get(k)
        err = (new_val-old_val)/old_val
        print('Error:' , err)
        assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        print('')
        
    return

def EVTOL_Aircraft_Test(update_regression_values,show_figure): 
    weight_analysis          = RCAIDE.Framework.Analyses.Weights.Electric()
    weight_analysis.vehicle  = evtol_setup(update_regression_values) 
    weight_analysis.aircraft_type = 'VTOL'
    weight_analysis.method   = 'Physics_Based'
    weight_analysis.settings.safety_factor = 1.5    # CHECK THIS VALUE
    weight_analysis.settings.miscelleneous_weight_factor = 1.1 # CHECK THIS VALUE
    weight_analysis.settings.disk_area_factor = 1.15
    weight_analysis.settings.max_thrust_to_weight_ratio = 1.1
    weight_analysis.settings.max_g_load = 3.8
    weight                   = weight_analysis.evaluate()
    plot_weight_breakdown(weight_analysis.vehicle, show_figure = show_figure) 

    if update_regression_values:
        save_results(weight, os.path.join(os.path.dirname(__file__), 'weights_EVTOL.res'))
    old_weight = load_results(os.path.join(os.path.dirname(__file__), 'weights_EVTOL.res'))
    
    check_list = [
        'empty.total', 
        'empty.structural.total',
        'empty.propulsion.total',   
        'empty.systems.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = old_weight.deep_get(k)
        new_val = weight.deep_get(k)
        err = (new_val-old_val)/old_val
        print('Error:' , err)
        assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        print('')
     
    return


if __name__ == '__main__':
    main()
