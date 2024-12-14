# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Air.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import Units
from .Generic_Battery_Module import Generic_Battery_Module  

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Air
# ----------------------------------------------------------------------------------------------------------------------   
class Lithium_Air(Generic_Battery_Module):
    """Lithium-Air battery cell.Specifies specific energy characteristics specific to
    lithium-air batteries. Also includes parameters related to consumption of oxygen
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """      
        self.cell.specific_energy  = 2000.     *Units.Wh/Units.kg    # convert to Joules/kg
        self.cell.specific_power   = 0.66      *Units.kW/Units.kg    # convert to W/kg
        self.cell.mass_gain_factor = (1.92E-4) /Units.Wh