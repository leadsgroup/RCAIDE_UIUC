# RCAIDE/Framework/Analyses/Mission/Mission.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports        
from RCAIDE.Framework.Core import Container 

# ----------------------------------------------------------------------------------------------------------------------
#  Mission
# ----------------------------------------------------------------------------------------------------------------------  
class Missions(Container):
    """ Mission.py: Top-level mission class
    
        Assumptions:
        None
        
        Source:
        None
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
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
        self.tag      = 'missions'    

    def append_mission(self,mission): 
        
        self.append(mission)
        return        
    
     