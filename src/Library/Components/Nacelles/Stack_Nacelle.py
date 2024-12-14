# RCAIDE/Compoments/Nacelles/Stack_Nacelle.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data, Container  
from .Nacelle import Nacelle
  
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Stack_Nacelle(Nacelle):
    """ This is a stacked nacelle for a generic aircraft.
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
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
        
        self.tag                       = 'stack_nacelle'  
        self.Segments                  = Container() 
        
    def append_segment(self,segment):
        """ Adds a segment to the nacelle. 
    
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

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return  
