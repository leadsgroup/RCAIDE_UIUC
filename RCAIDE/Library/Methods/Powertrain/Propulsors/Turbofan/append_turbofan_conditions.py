# RCAIDE/Library/Methods/Powertrain/Propulsors/Turbofan_Propulsor/append_turbofan_conditions.py
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
#  append_turbofan_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turbofan_conditions(turbofan,segment):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[turbofan.tag]                               = Conditions()  
    segment.state.conditions.energy[turbofan.tag].throttle                      = 0. * ones_row(1)      
    segment.state.conditions.energy[turbofan.tag].commanded_thrust_vector_angle = 0. * ones_row(1)  
    segment.state.conditions.energy[turbofan.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[turbofan.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[turbofan.tag].moment                        = 0. * ones_row(3) 
    segment.state.conditions.energy[turbofan.tag].fuel_flow_rate                = 0. * ones_row(1)
    segment.state.conditions.energy[turbofan.tag].inputs                        = Conditions()
    segment.state.conditions.energy[turbofan.tag].outputs                       = Conditions() 
    segment.state.conditions.noise[turbofan.tag]                                = Conditions()  
    segment.state.conditions.noise[turbofan.tag].core_nozzle                    = Conditions() 
    segment.state.conditions.noise[turbofan.tag].fan_nozzle                     = Conditions() 
    segment.state.conditions.noise[turbofan.tag].fan                            = Conditions()

    turbofan_conditions      = segment.state.conditions.energy[turbofan.tag]
    for tag, item in  turbofan.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,turbofan_conditions) 
            for sub_tag, sub_item in  item.items(): 
                if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                    item_conditions = turbofan_conditions[item.tag] 
                    sub_item.append_operating_conditions(segment,item_conditions)    
    return 