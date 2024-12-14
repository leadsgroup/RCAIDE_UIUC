# RCAIDE/Energy/Peripherals/Payload.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Propulsors.Common.append_payload_conditions import append_payload_conditions
 
# ----------------------------------------------------------------------------------------------------------------------
#  Avionics
# ----------------------------------------------------------------------------------------------------------------------              
class Payload(Component):
    """A class representing a payload.
    
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
        self.tag        = 'payload' 
        self.power_draw = 0.0
         
    def append_operating_conditions(self,segment,bus): 
        append_payload_conditions(self,segment,bus)
        return 
        
    def power(self):
        """This gives the power draw from a payload.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        self.outputs.power_draw         [Watts]

        Properties Used:
        self.power_draw
        """          
        self.inputs.power = self.power_draw
        
        return self.power_draw 