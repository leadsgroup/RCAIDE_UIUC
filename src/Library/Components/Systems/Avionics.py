# RCAIDE/Library/Compoments/Systems/Avionics.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
from RCAIDE.Library.Methods.Propulsors.Common.append_avionics_conditions import append_avionics_conditions
 
# ----------------------------------------------------------------------------------------------------------------------
#  Avionics
# ----------------------------------------------------------------------------------------------------------------------            
class Avionics(Component):
    """A class representing avionics.
    
    Assumptions:
    None
    
    Source:
    N/A
    """        
    def __defaults__(self):
        """This sets the default power draw.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """                 
        self.power_draw = 0.0
        self.tag        = 'Avionics'

    def append_operating_conditions(self,segment,bus): 
        append_avionics_conditions(self,segment,bus)
        return
            
        
    def power(self):
        """This gives the power draw from avionics.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        self.outputs.power_draw          [Watts]
                                           
        Properties Used:
        self.power_draw    
        """                 
        self.inputs.power = self.power_draw
        
        return self.power_draw