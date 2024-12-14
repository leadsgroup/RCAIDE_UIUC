# RCAIDE/Library/Components/Propulsors/Modulators/Electronic_Speed_Controller.py
#  
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components import Component 
from RCAIDE.Library.Methods.Propulsors.Modulators.Electronic_Speed_Controller.append_esc_conditions   import append_esc_conditions 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Electronic Speed Controller Class
# ---------------------------------------------------------------------------------------------------------------------- 
class Electronic_Speed_Controller(Component):
    
    def __defaults__(self):
        """ This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
            """         

        self.tag              = 'electronic_speed_controller'  
        self.efficiency       = 0.0 

    def append_operating_conditions(self,segment,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_esc_conditions(self,segment,propulsor_conditions)
        return 