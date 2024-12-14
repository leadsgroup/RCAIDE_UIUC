# RCAIDE/Compoments/Landing_Gear/Nose_Landing_Gear.py
# 
# 
# Created:  Nov 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Landing_Gear import Landing_Gear

# ---------------------------------------------------------------------------------------------------------------------- 
#  Nose_Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------   
class Nose_Landing_Gear(Landing_Gear):
    """ Nose Landing Gear Component
          
            Assumptions:
            None
            
            Source:
            N/A        
    """

    def __defaults__(self): 
        
        """ This sets the default values for the component attributes.
        
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Output:
                None
                
                Properties Used:
                N/A
        """
        self.tag           = 'nose_gear'
        self.tire_diameter = 0.    
        self.strut_length  = 0.    
        self.units         = 0. # number of nose landing gear    
        self.wheels        = 0. # number of wheels on the nose landing gear 