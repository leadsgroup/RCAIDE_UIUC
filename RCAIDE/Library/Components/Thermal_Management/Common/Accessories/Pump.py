## @ingroup Energy-Thermal_Management-Batteries-Accessories
# RCAIDE/Energy/Thermal_Management/Batteries/Accessories/Pump.py
# 
# 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from RCAIDE.Core import Data

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------
## @ingroup Attributes-Coolants
class Pump(Data):
    """Holds values for a coolant reservoir

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
        Values commonly available

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """
        self.tag                       = 'Pump'
        self.efficiency                = 1.0
        
        return
   
    def compute_power_consumed (pressure_differerntial, density, mass_flow_rate,efficiency):
        return mass_flow_rate*pressure_differerntial/(density*efficiency)
    
    