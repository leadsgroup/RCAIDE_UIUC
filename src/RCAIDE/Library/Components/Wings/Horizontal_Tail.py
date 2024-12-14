# RCAIDE/Compoments/Wings/Horizontal_Tail.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Wing import Wing 
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_wing_moment_of_inertia import  compute_wing_moment_of_inertia

# ---------------------------------------------------------------------------------------------------------------------- 
#  Main Wing 
# ----------------------------------------------------------------------------------------------------------------------    
class Horizontal_Tail(Wing):
    """ This is the horizontal stabilizer class  
    
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

    def __defaults__(self):
        """This sets the default for horizontal tails.
    
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
        self.tag = 'horizontal_tail'
    
    def moment_of_inertia(wing,center_of_gravity):
        I =  compute_wing_moment_of_inertia(wing,center_of_gravity) 
        return I 
    