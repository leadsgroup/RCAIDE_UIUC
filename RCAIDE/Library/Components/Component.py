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
    """
    Base class for all physical components in an aircraft configuration.

    Attributes
    ----------
    tag : str
        Unique identifier for the component, defaults to 'Component'
        
    mass_properties : Mass_Properties
        Mass and inertia properties, initialized empty
        
    origin : ndarray
        3D coordinates [x, y, z] defining component's reference point, 
        defaults to [0.0, 0.0, 0.0]

    Notes
    -----
    The Component class serves as the foundation for all physical parts in RCAIDE. 
    It provides:
    
    * Basic geometric positioning
    * Mass properties tracking
    * Container functionality for sub-components

    See Also
    --------
    RCAIDE.Library.Components.Mass_Properties
        Class containing mass and inertia data
    RCAIDE.Framework.Core.Data
        Parent class providing data structure functionality
    """
    def __defaults__(self):
        """
        Sets default values for the component attributes.
        """         
        self.tag             = 'Component' 
        self.mass_properties = Mass_Properties()
        self.origin          = np.array([[0.0,0.0,0.0]])
    
        
# ----------------------------------------------------------------------------------------------------------------------
#  Component Container
# ----------------------------------------------------------------------------------------------------------------------     
class Container(ContainerBase):
    """
    Container class for managing collections of components.

    Notes
    -----
    The Container class provides organization and mass calculation functionality 
    for groups of components. Key features include:
    
    * Recursive mass summation
    * Moment calculation about reference points
    * Component hierarchy management

    See Also
    --------
    RCAIDE.Framework.Core.Container
        Parent class providing base container functionality
    """
    pass 
 
    def sum_mass(self):
        """
        Recursively calculates total mass of all contained components.

        Returns
        -------
        float
            Total mass in kg

        Notes
        -----
        Traverses the component tree and sums mass_properties.mass values from:
        
        * Individual components
        * Nested component containers (recursive)
        """   
        total = 0.0
        for key,Comp in self.items():
            if isinstance(Comp,Component.Container):
                total += Comp.sum_mass() # recursive!
            elif isinstance(Comp,Component):
                total += Comp.mass_properties.mass
                
        return total
    
    def total_moment(self):
        """
        Recursively calculates total moment of all contained components.

        Returns
        -------
        ndarray
            Total moment vector [kg*m] about the origin

        Notes
        -----
        Calculates moments considering:
        * Component masses
        * Component origins
        * Component centers of gravity
        * Nested containers (recursive)
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
