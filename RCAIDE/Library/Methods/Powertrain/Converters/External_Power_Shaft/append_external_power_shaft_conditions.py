# RCAIDE/Library/Methods/Powertrain/Converters/external_power_shaft/append_external_power_shaft_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_ram_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_external_power_shaft_conditions(external_power_shaft,segment,energy_conditions): 
    energy_conditions[external_power_shaft.tag]                              = Conditions() 
    energy_conditions[external_power_shaft.tag].inputs                       = Conditions() 
    energy_conditions[external_power_shaft.tag].outputs                      = Conditions() 
    return 