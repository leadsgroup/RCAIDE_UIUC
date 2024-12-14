# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Aluminum_Air.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

 # RCAIDE imports
from RCAIDE.Framework.Core import Units
from .Generic_Battery_Module    import Generic_Battery_Module

# ----------------------------------------------------------------------------------------------------------------------
#  Aluminum_Air
# ----------------------------------------------------------------------------------------------------------------------   
class Aluminum_Air(Generic_Battery_Module):
    """ Aluminum-Air battery cell. Specifies discharge/specific energy characteristics specific to
    aluminum-air batteries. Also includes parameters related to consumption of aluminum, oxygen, and water
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """
        self.tag                         = 'Aluminum Air'
        self.cell.specific_energy        = 1300.*Units.Wh/Units.kg    # convert to Joules/kg
        self.cell.specific_power         = 0.2*Units.kW/Units.kg      # convert to W/kg
        self.mass_gain_factor            = 0.000110145*Units.kg/Units.Wh
        self.cell.water_mass_gain_factor = 0.000123913*Units.kg/Units.Wh
        self.cell.aluminum_mass_factor   = 0.000123828*Units.kg/Units.Wh # aluminum consumed per energy
        self.cell.ragone.const_1         = 0.8439*Units.kW/Units.kg
        self.cell.ragone.const_2         = -4.8647e-004/(Units.Wh/Units.kg)
        self.cell.ragone.lower_bound     = 1100.*Units.Wh/Units.kg
        self.cell.ragone.upper_bound     = 1600.*Units.Wh/Units.kg