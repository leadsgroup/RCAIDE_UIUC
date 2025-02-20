# RCAIDE/Library/Methods/Powertrain/Converters/Turboshaft/append_turboshaft_conditions.py
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
#  append_turboshaft_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turboshaft_conditions(turboshaft,segment,propulsor_conditions):  
    ones_row    = segment.state.ones_row                  
    propulsor_conditions[turboshaft.tag]                               = Conditions()  
    propulsor_conditions[turboshaft.tag].throttle                      = 0. * ones_row(1)     
    propulsor_conditions[turboshaft.tag].commanded_thrust_vector_angle = 0. * ones_row(1)   
    propulsor_conditions[turboshaft.tag].shaft_power                   = 0. * ones_row(1)
    propulsor_conditions[turboshaft.tag].fuel_flow_rate                = 0. * ones_row(1)
    propulsor_conditions[turboshaft.tag].inputs                        = Conditions()
    propulsor_conditions[turboshaft.tag].outputs                       = Conditions()

    for tag, item in  turboshaft.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,turboshaft)     
    
    return 