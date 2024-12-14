# RCAIDE/Compoments/Fuselages/Tube_Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Fuselage import Fuselage
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_fuselage_moment_of_inertia import  compute_fuselage_moment_of_inertia
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Tube_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Tube_Fuselage(Fuselage):
    """ This is a standard fuselage for a tube and wing aircraft.
    
    Assumptions:
    Conventional fuselage
    
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
        self.tag                                    = 'tube_fuselage'
        
    def compute_moment_of_inertia(self, center_of_gravity): 
        I =  compute_fuselage_moment_of_inertia(self,center_of_gravity) 
        return I        
  