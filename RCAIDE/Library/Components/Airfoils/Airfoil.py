## @ingroup Library-Components-Airfoils
# RCAIDE/Compoments/Airfoils/Airfoil.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Library.Components   import Component 
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Airfoil
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Airfoils 
class Airfoil(Component):
    """Generic airfoil class."""
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """         
        
        self.tag                        = 'Airfoil' 
        self.coordinate_file            = None     
        self.geometry                   = None
        self.polar_files                = None
        self.polars                     = None
        self.prev                       = None
        self.next                       = None
        self.number_of_points           = 201
       