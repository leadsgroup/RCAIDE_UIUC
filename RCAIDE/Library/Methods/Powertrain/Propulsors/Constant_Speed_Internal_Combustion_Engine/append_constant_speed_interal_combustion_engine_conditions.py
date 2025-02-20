# RCAIDE/Library/Methods/Powertrain/Propulsors/Constant_Speed_ICE_Propulsor/append_constant_speed_interal_combustion_engine_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_constant_speed_interal_combustion_engine_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_constant_speed_interal_combustion_engine_conditions(propulsor,segment):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[propulsor.tag]                               = Conditions()  
    segment.state.conditions.energy[propulsor.tag].throttle                      = 0. * ones_row(1)      
    segment.state.conditions.energy[propulsor.tag].commanded_thrust_vector_angle = 0. * ones_row(1)  
    segment.state.conditions.energy[propulsor.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[propulsor.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[propulsor.tag].moment                        = 0. * ones_row(3) 
    segment.state.conditions.energy[propulsor.tag].fuel_flow_rate                = 0. * ones_row(1)
    segment.state.conditions.energy[propulsor.tag].rpm                           = segment.state.conditions.energy.rpm * ones_row(1)      
    segment.state.conditions.energy[propulsor.tag].inputs                        = Conditions()
    segment.state.conditions.energy[propulsor.tag].outputs                       = Conditions() 
    segment.state.conditions.noise[propulsor.tag]                                = Conditions()

    propulsor_conditions      = segment.state.conditions.energy[propulsor.tag]
    for tag, item in  propulsor.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,propulsor_conditions) 
            for sub_tag, sub_item in  item.items(): 
                if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                    item_conditions = propulsor_conditions[item.tag] 
                    sub_item.append_operating_conditions(segment,item_conditions)     
    return 