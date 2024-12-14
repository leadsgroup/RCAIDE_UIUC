# RCAIDE/Compoments/Wings/Stabilator.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Horizontal_Tail    import Horizontal_Tail
from .All_Moving_Surface import All_Moving_Surface
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_wing_moment_of_inertia import  compute_wing_moment_of_inertia

# ---------------------------------------------------------------------------------------------------------------------- 
#  Stabilator
# ----------------------------------------------------------------------------------------------------------------------     
class Stabilator(Horizontal_Tail, All_Moving_Surface):
    """ This class is used to define stabilators in RCAIDE. Note that it 
    inherits from both Horizontal_Tail and All_Moving_Surface
    
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
        """This sets the default for stabilators in RCAIDE.
        
        See All_Moving_Surface().__defaults__ and Wing().__defaults__ for 
        an explanation of attributes
    
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
        self.tag                = 'stabilator'
        self.sign_duplicate     = 1.0

    def moment_of_inertia(wing,center_of_gravity):
        
        I =  compute_wing_moment_of_inertia(wing,center_of_gravity) 
        return I  