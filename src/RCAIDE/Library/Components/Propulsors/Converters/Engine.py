# RCAIDE/Library/Components/Propulsors/Converters/Engine.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Library.Components                      import Component   
from RCAIDE.Library.Methods.Propulsors.Converters.Engine.append_engine_conditions import append_engine_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Engine Class
# ----------------------------------------------------------------------------------------------------------------------  
class Engine(Component):
    """This is an internal combustion engine component. 
    """           
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None 
        """      
        self.tag                             = 'internal_combustion_engine' 
        self.sea_level_power                 = 0.0
        self.flat_rate_altitude              = 0.0
        self.rated_speed                     = 0.0  
        self.power_split_ratio               = 0.0
        self.power_specific_fuel_consumption = 0.36

    def append_operating_conditions(self,segment,propulsor):  
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag] 
        append_engine_conditions(self,segment,propulsor_conditions) 
        return                

