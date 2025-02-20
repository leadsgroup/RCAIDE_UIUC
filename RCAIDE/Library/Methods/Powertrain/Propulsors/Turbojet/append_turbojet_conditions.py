# RCAIDE/Library/Methods/Powertrain/Propulsors/Turbojet_Propulsor/append_turbojet_conditions.py
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
#  append_turbojet_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turbojet_conditions(turbojet,segment):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[turbojet.tag]                               = Conditions()  
    segment.state.conditions.energy[turbojet.tag].throttle                      = 0. * ones_row(1)     
    segment.state.conditions.energy[turbojet.tag].commanded_thrust_vector_angle = 0. * ones_row(1)    
    segment.state.conditions.energy[turbojet.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[turbojet.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[turbojet.tag].moment                        = 0. * ones_row(3) 
    segment.state.conditions.energy[turbojet.tag].fuel_flow_rate                = 0. * ones_row(1)
    segment.state.conditions.energy[turbojet.tag].inputs                        = Conditions()
    segment.state.conditions.energy[turbojet.tag].outputs                       = Conditions() 
    segment.state.conditions.noise[turbojet.tag]                                = Conditions()  
    segment.state.conditions.noise[turbojet.tag].core_nozzle                    = Conditions()
    

    turbojet_conditions      = segment.state.conditions.energy[turbojet.tag]
    for tag, item in  turbojet.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,turbojet_conditions) 
            for sub_tag, sub_item in  item.items(): 
                if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                    item_conditions = turbojet_conditions[item.tag] 
                    sub_item.append_operating_conditions(segment,item_conditions)     
    return 