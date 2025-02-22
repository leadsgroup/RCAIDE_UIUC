# RCAIDE/Library/Methods/Powertrain/Propulsors/Internal_Combustion_Engine/append_internal_combustion_engine_conditions.py
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
#  append_internal_combustion_engine_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_internal_combustion_engine_conditions(internal_combustion_engine,segment):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[internal_combustion_engine.tag]                               = Conditions()  
    segment.state.conditions.energy[internal_combustion_engine.tag].throttle                      = 0. * ones_row(1)      
    segment.state.conditions.energy[internal_combustion_engine.tag].commanded_thrust_vector_angle = 0. * ones_row(1)  
    segment.state.conditions.energy[internal_combustion_engine.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[internal_combustion_engine.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[internal_combustion_engine.tag].moment                        = 0. * ones_row(3) 
    segment.state.conditions.energy[internal_combustion_engine.tag].fuel_flow_rate                = 0. * ones_row(1)
    segment.state.conditions.energy[internal_combustion_engine.tag].inputs                        = Conditions()
    segment.state.conditions.energy[internal_combustion_engine.tag].outputs                       = Conditions() 
    segment.state.conditions.noise[internal_combustion_engine.tag]                                = Conditions()  

    ICE_energy_conditions      = segment.state.conditions.energy[internal_combustion_engine.tag]
    ICE_noise_conditions       = segment.state.conditions.noise[internal_combustion_engine.tag]
    for tag, item in  internal_combustion_engine.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,ICE_energy_conditions,noise_conditions=ICE_noise_conditions) 
            for sub_tag, sub_item in  item.items(): 
                if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                    item_conditions = ICE_energy_conditions[item.tag] 
                    sub_item.append_operating_conditions(segment,item_conditions)                     
    return 