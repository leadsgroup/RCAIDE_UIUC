# RCAIDE/Compoments/Fuselages/Blended_Wing_Body_Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Fuselage import Fuselage

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Blended_Wing_Body_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Blended_Wing_Body_Fuselage(Fuselage):
    """ This is a blended wing body fuselage class 
    
    Assumptions: 
    
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
          
        self.tag                   = 'bwb_fuselage'
        self.aft_centerbody_area   = 0.0
        self.aft_centerbody_taper  = 0.0
        self.cabin_area            = 0.0
        
    def compute_moment_of_inertia(self, center_of_gravity): 
        I =  np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) 
        return I        