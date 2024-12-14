# RCAIDE/Compoments/Landing_Gear/Landing_Gear.py
# 
# 
# Created:  Nov 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Library.Components import Component    
# ---------------------------------------------------------------------------------------------------------------------- 
#  Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------  
class Landing_Gear(Component):
    """ The Top Landing Gear Component Class
        
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
                
                Outputs:
                None
                
                Properties Used:
                N/A
        """
       
        self.tag            = 'landing_gear'   
        self.tire_diameter  = 0 
        self.strut_length   = 0 
        self.units          = 0 
        self.gear_extended  = False
        self.wheels         = 0     