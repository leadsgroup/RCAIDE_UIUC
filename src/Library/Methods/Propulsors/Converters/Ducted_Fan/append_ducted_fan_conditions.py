# RCAIDE/Library/Methods/Propulsors/Converters/Ducted_Fan/append_ducted_fan_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_motor_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_ducted_fan_conditions(ducted_fan,segment,energy_conditions): 
    ones_row    = segment.state.ones_row 
    energy_conditions[ducted_fan.tag]                               = Conditions()   
    energy_conditions[ducted_fan.tag].orientation                   = 0. * ones_row(3) 
    energy_conditions[ducted_fan.tag].commanded_thrust_vector_angle = 0. * ones_row(1) 
    energy_conditions[ducted_fan.tag].torque                        = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].throttle                      = ones_row(1)
    energy_conditions[ducted_fan.tag].thrust                        = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].rpm                           = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].omega                         = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].disc_loading                  = 0. * ones_row(1)                 
    energy_conditions[ducted_fan.tag].power_loading                 = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].tip_mach                      = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].efficiency                    = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].figure_of_merit               = 0. * ones_row(1)
    energy_conditions[ducted_fan.tag].power_coefficient             = 0. * ones_row(1)  
    return 
