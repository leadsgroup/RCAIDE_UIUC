# RCAIDE/Library/Methods/Powertrain/Propulsors/Electric_Rotor_Propulsor/append_electric_ducted_fan_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Mission.Common                             import Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append electric ducted fan network conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_electric_ducted_fan_conditions(propulsor,segment):
    '''
    MATTEO
    
    '''
    ones_row    = segment.state.ones_row
                
    segment.state.conditions.energy[propulsor.tag]                               = Conditions()  
    segment.state.conditions.energy[propulsor.tag].throttle                      = 0. * ones_row(1)      
    segment.state.conditions.energy[propulsor.tag].commanded_thrust_vector_angle = 0. * ones_row(1)  
    segment.state.conditions.energy[propulsor.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[propulsor.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[propulsor.tag].moment                        = 0. * ones_row(3)
    

    propulsor_conditions      = segment.state.conditions.energy[propulsor.tag]
    for tag, item in  propulsor.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,propulsor_conditions) 
            for sub_tag, sub_item in  item.items(): 
                if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                    item_conditions = propulsor_conditions[item.tag] 
                    sub_item.append_operating_conditions(segment,item_conditions)          
    return