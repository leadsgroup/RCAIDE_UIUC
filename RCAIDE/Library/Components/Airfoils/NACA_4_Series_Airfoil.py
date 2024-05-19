## @ingroup Library-Components-Airfoils
# RCAIDE/Compoments/Airfoils/NACA_4_Series_Airfoil.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Airfoil import Airfoil
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Airfoil
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Airfoils 
class NACA_4_Series_Airfoil(Airfoil):
    """NACA 4-Series airfoil class."""
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """        
        self.tag                   = 'NACA_4_Series'
        self.NACA_4_Series_code    = '0012'
        return 
