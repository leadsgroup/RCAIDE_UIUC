# RCAIDE/Library/Compoments/Energy/Fuel_Tanks/Central_Fuel_Tank.py
# 
# 
# Created:  September 2024, A. Molloy and M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from .Fuel_Tank  import Fuel_Tank 
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Tanks.append_fuel_tank_conditions import append_fuel_tank_conditions 

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ---------------------------------------------------------------------------------------------------------------------    
class Central_Fuel_Tank(Fuel_Tank):
    """Central Fuel tank compoment.
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'Central_fuel_tank'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.length                      = 0.0
        self.width                       = 0.0
        self.height                      = 0.0
        self.fuel                        = None
         

    def append_operating_conditions(self,segment,fuel_line):  
        append_fuel_tank_conditions(self,segment, fuel_line)  
        return                                          