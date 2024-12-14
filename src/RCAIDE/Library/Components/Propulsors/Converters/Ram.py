# RCAIDE/Library/Components/Propulsors/Converters/Ram.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Components                      import Component  
from RCAIDE.Library.Methods.Propulsors.Converters.Ram.append_ram_conditions import append_ram_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ----------------------------------------------------------------------------------------------------------------------
class Ram(Component):
    """This represent the compression of incoming air flow. 
    """

    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/ 
        """
        #set the deafult values
        self.tag                      = 'Ram' 
        self.working_fluid            = Data()


    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_ram_conditions(self,segment,propulsor_conditions)
        return                         