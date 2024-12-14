# RCAIDE/Library/Methods/Propulsors/Converters/Motor/append_motor_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_motor_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_motor_conditions(motor,segment,propulsor_conditions): 
    ones_row    = segment.state.ones_row 
    propulsor_conditions[motor.tag]            = Conditions()
    propulsor_conditions[motor.tag].inputs     = Conditions()
    propulsor_conditions[motor.tag].outputs    = Conditions()
    propulsor_conditions[motor.tag].torque     = 0. * ones_row(1) 
    propulsor_conditions[motor.tag].efficiency = 0. * ones_row(1) 
    
    return 
