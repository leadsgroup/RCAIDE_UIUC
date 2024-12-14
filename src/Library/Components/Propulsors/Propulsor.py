# RCAIDE/Library/Components/Propulsors/Propuslor.py
#  
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                   import Component 

# ----------------------------------------------------------------------------------------------------------------------
#  Propusor
# ---------------------------------------------------------------------------------------------------------------------- 
class Propulsor(Component):
    """  This controls the flow of energy into and from a battery-powered nework 
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    
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
        self.tag                          = 'propulsor' 
        self.active                       = True 
        self.wing_mounted                 = True 
        
    