# RCAIDE/Library/Compoments/Systems/System.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
# System
# ----------------------------------------------------------------------------------------------------------------------            
class System(Component):
    """A class representing an aircraft system/systems.
    
    Assumptions:
    None
    
    Source:
    N/A
    """  
    def __defaults__(self): 
        """ This sets the default values for the system.
        
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
        
        self.tag             = 'System'
        self.origin          = [[0.0,0.0,0.0]]
        self.control         = None
        self.accessories     = None 