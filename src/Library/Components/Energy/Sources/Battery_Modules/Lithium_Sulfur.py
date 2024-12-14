# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Sulfur.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# package imports
from RCAIDE.Framework.Core import Units
from .Generic_Battery_Module import Generic_Battery_Module

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Sulfur
# ----------------------------------------------------------------------------------------------------------------------  
class Lithium_Sulfur(Generic_Battery_Module):
    """Lithium-Sulphur battery.
    """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """   
        self.cell.specific_energy    = 500     *Units.Wh/Units.kg
        self.cell.specific_power     = 1       *Units.kW/Units.kg
        self.cell.ragone.const_1     = 245.848 *Units.kW/Units.kg
        self.cell.ragone.const_2     = -.00478 /(Units.Wh/Units.kg)
        self.cell.ragone.lower_bound = 300     *Units.Wh/Units.kg
        self.cell.ragone.upper_bound = 700     *Units.Wh/Units.kg