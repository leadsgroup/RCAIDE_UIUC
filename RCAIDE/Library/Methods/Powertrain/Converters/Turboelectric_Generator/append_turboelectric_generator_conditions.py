# RCAIDE/Library/Methods/Powertrain/Converters/Turboelectric_Generator/append_turboelectric_generator_conditions.py 
# 
# Created:  Feb 2025, M. Clarke  
import RCAIDE
from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turboelectric_generator_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turboelectric_generator_conditions(turboelectric_generator,segment,fuel_line):  

    ones_row    = segment.state.ones_row   

    fuel_line_results                              = segment.state.conditions.energy[fuel_line.tag] 
    fuel_line_results[turboelectric_generator.tag] = Conditions()

    fuel_line_results[turboelectric_generator.tag].throttle                                   = 0. * ones_row(1)     
    fuel_line_results[turboelectric_generator.tag].commanded_thrust_vector_angle              = 0. * ones_row(1)   
    fuel_line_results[turboelectric_generator.tag].power                                      = 0. * ones_row(1)
    fuel_line_results[turboelectric_generator.tag].fuel_flow_rate                             = 0. * ones_row(1)
    fuel_line_results[turboelectric_generator.tag].inputs                                     = Conditions()
    fuel_line_results[turboelectric_generator.tag].outputs                                    = Conditions() 

    # propulsor_conditions[turboelectric_generator.tag][turboelectric_generator.generator.tag]     = Conditions() 
    # propulsor_conditions[turboelectric_generator.tag][turboelectric_generator.turboshaft.tag]    = Conditions() 

    turboelectric_generator_conditions      = fuel_line_results[turboelectric_generator.tag]
    for tag, item in  turboelectric_generator.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Powertrain.Converters.Turboshaft):
            item.append_operating_conditions(segment,fuel_line,turboelectric_generator)   
        if issubclass(type(item), RCAIDE.Library.Components.Component) and not issubclass(type(item), RCAIDE.Library.Components.Powertrain.Converters.Turboshaft):
            item.append_operating_conditions(segment,fuel_line) 
            for _, sub_item in  item.items(): 
                if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                    item_conditions = turboelectric_generator_conditions[item.tag] 
                    sub_item.append_operating_conditions(segment,item_conditions) 
    return 