## @ingroup Energy-Thermal_Management-Batteries-Accessories
# RCAIDE/Energy/Thermal_Management/Batteries/Accessories/Fan.py
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
class Fan(Data):
    """Holds values for a coolant reservoir

    Assumptions:
   Power 

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
        self.tag                       = 'Fan'
        self.efficiency                = 1.0
        
        return
   
    def compute_power_consumed (pressure_differerntial, density, mass_flow_rate,efficiency):
        return mass_flow_rate*pressure_differerntial/(density*efficiency)
    
