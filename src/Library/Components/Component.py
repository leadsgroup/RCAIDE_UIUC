# RCAIDE/Library/Compoments/Component.py
#  
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Container as ContainerBase
from RCAIDE.Framework.Core import Data
from .Mass_Properties import Mass_Properties

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Component
# ----------------------------------------------------------------------------------------------------------------------         
class Component(Data):
    """ the base component class
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
        self.tag             = 'Component' 
        self.mass_properties = Mass_Properties()
        self.origin          = np.array([[0.0,0.0,0.0]])
    
        
# ----------------------------------------------------------------------------------------------------------------------
#  Component Container
# ----------------------------------------------------------------------------------------------------------------------     
class Container(ContainerBase):
    """ the base component container class
    
        Assumptions:
        None
        
        Source:
        None
    """
    pass 
 
    def sum_mass(self):
        """ will recursively search the data tree and sum
            any Comp.Mass_Properties.mass, and return the total sum
            
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            mass  [kg]
    
            Properties Used:
            None
        """   
        total = 0.0
        for key,Comp in self.items():
            if isinstance(Comp,Component.Container):
                total += Comp.sum_mass() # recursive!
            elif isinstance(Comp,Component):
                total += Comp.mass_properties.mass
                
        return total
    
    def total_moment(self):
        """ will recursively search the data tree and sum
            any Comp.Mass_Properties.mass, and return the total sum of moments
            
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            total moment [kg*m]
    
            Properties Used:
            None
        """   
        total = np.array([[0.0,0.0,0.0]])
        for key,Comp in self.items():
            if isinstance(Comp,Component.Container):
                total += Comp.total_moment()  
            elif isinstance(Comp,Component):
                total += Comp.mass_properties.mass*(np.sum(np.array(Comp.origin),axis=0)/len(Comp.origin)+Comp.mass_properties.center_of_gravity)

        return total  
    
# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------

Component.Container = Container
