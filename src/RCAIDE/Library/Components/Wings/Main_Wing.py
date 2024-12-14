# RCAIDE/Compoments/Wings/Main_Wing.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Wing import Wing
from RCAIDE.Framework.Core import Container 
from RCAIDE.Library.Components.Wings.Segment import Segment
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_wing_moment_of_inertia import  compute_wing_moment_of_inertia

# ---------------------------------------------------------------------------------------------------------------------- 
#  Main Wing 
# ----------------------------------------------------------------------------------------------------------------------  
class Main_Wing(Wing):
    """This class is used to define main wings RCAIDE

    Assumptions:Container()
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
        """This sets the default for main wings in RCAIDE.
    
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
        self.tag                 = 'main_wing'
        self.Segments            = Segment_Container()
         
    def moment_of_inertia(wing,center_of_gravity):
        I =  compute_wing_moment_of_inertia(wing,center_of_gravity) 
        return I 

class Segment_Container(Container):
    """ Container for wing segment
    
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

    def get_children(self):
        """ Returns the components that can go inside
        
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
        
        return [Segment] 
    
    def append(self,val):
        """Appends the value to the containers
          This overrides the basic data class append
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            self
    
            Outputs:
            N/A
    
            Properties Used:
            N/A
            """          
        
        
        # See if the component exists, if it does modify the name
        keys = self.keys()
        if val.tag in keys:
            string_of_keys = "".join(self.keys())
            n_comps = string_of_keys.count(val.tag)
            val.tag = val.tag + str(n_comps+1)    
            
        Container.append(self,val) 