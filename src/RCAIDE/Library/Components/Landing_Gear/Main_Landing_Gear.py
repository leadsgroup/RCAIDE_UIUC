# RCAIDE/Compoments/Landing_Gear/Main_Landing_Gear.py
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
class Main_Landing_Gear(Landing_Gear):
    """ Main Landing Gear Component
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
        self.tag           = 'main_gear'
        self.units         = 0. # number of main landing gear units        
        self.strut_length  = 0.
        self.tire_diameter = 0. 
        self.wheels        = 0. # number of wheels on the main landing gear 