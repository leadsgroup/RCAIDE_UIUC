# RCAIDE/Library/Components/Propulsors/Converters/Shaft_Power_Offtake.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  
from RCAIDE.Library.Methods.Propulsors.Converters.Offtake_Shaft.append_offtake_shaft_conditions import append_offtake_shaft_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
# Shaft_Power_Offtake
# ---------------------------------------------------------------------------------------------------------------------- 
class Offtake_Shaft(Component):
    """This is a component representing the power draw from the shaft. 
    """ 
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None 
        """          
        self.power_draw            = 0.0
        self.reference_temperature = 288.15
        self.reference_pressure    = 1.01325 * 10 ** 5 

    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_offtake_shaft_conditions(self,segment,propulsor_conditions)
        return                         