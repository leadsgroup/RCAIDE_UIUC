# RCAIDE/Library/Methods/Propulsors/Low_Fidelity_Ducted_Fan/append_low_fidelity_ducted_fan_conditions.py
# 
# Created:  Jan 2025, M. Guidotti  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_low_fidelity_ducted_fan_conditions
# ----------------------------------------------------------------------------------------------------------------------    

def append_low_fidelity_ducted_fan_conditions(low_fidelity_ducted_fan,segment):  
    ones_row                                                                                       = segment.state.ones_row                  
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag]                                   = Conditions()  
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].throttle                          = 0. * ones_row(1)      
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].commanded_thrust_vector_angle     = 0. * ones_row(1)  
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].thrust                            = 0. * ones_row(3) 
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].power                             = 0. * ones_row(1) 
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].moment                            = 0. * ones_row(3) 
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].inputs                            = Conditions()
    segment.state.conditions.energy[low_fidelity_ducted_fan.tag].outputs                           = Conditions() 
    segment.state.conditions.noise[low_fidelity_ducted_fan.tag]                                    = Conditions() 
    segment.state.conditions.noise[low_fidelity_ducted_fan.tag].low_fidelity_ducted_fan            = Conditions() 
    segment.state.conditions.noise[low_fidelity_ducted_fan.tag].low_fidelity_ducted_fan.fan_nozzle = Conditions() 
    segment.state.conditions.noise[low_fidelity_ducted_fan.tag].low_fidelity_ducted_fan.fan        = Conditions()  
    return 