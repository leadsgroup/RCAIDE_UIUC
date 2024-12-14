# RCAIDE/Library/Components/Propulsors/Converters/Fan.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  
from RCAIDE.Library.Methods.Propulsors.Converters.Fan.append_fan_conditions import append_fan_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan  
# ----------------------------------------------------------------------------------------------------------------------
class Fan(Component):
    """This is a fan component typically used in a turbofan. 
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            Pressure ratio and efficiency do not change with varying conditions.

        Source:
            https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/ 
        """         
        #set the default values
        self.tag                            = 'Fan'
        self.polytropic_efficiency          = 1.0
        self.pressure_ratio                 = 1.0
        self.angular_velocity               = 0


    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_fan_conditions(self,segment,propulsor_conditions)
        return                                