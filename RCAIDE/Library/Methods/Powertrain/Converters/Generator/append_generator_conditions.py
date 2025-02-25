# RCAIDE/Library/Methods/Powertrain/Converters/Generator/append_generator_conditions.py
# 
# Created:  Feb 2025, M. Guidotti
########## This file is rewritten needs to be checked later to maintain consistency
from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_generator_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_generator_conditions(generator,segment,fuel_line,converter):  
    ones_row    = segment.state.ones_row                 
    
    converter_results                              = segment.state.conditions.energy[fuel_line.tag][converter.tag] 
    converter_results[generator.tag]              = Conditions()

    # NEED TO CHANGe FROM PROPULSOR CONDITIONS MATTEO the inpurs need to change they are weird 

    ones_row    = segment.state.ones_row 
    converter_results[generator.tag]                         = Conditions()
    converter_results[generator.tag].inputs                  = Conditions()
    converter_results[generator.tag].outputs                 = Conditions()
    converter_results[generator.tag].torque                  = 0. * ones_row(1) 
    converter_results[generator.tag].current                 = 0. * ones_row(1) 
    converter_results[generator.tag].voltage                 = 0. * ones_row(1) 
    converter_results[generator.tag].inputs.shaft_power      = 0. * ones_row(1)
    converter_results[generator.tag].inputs.omega           = 0. * ones_row(1)
    
    return 

