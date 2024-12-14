# RCAIDE/Library/Compoments/Energy/Fuel_Tanks/Fuel_Tank.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Library.Components          import Component
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Tanks.append_fuel_tank_conditions import append_fuel_tank_conditions 

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ---------------------------------------------------------------------------------------------------------------------     
class Fuel_Tank(Component):
    """Fuel tank compoment.
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'fuel_tank'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.fuel                        = None
         

    def append_operating_conditions(self,segment,fuel_line):  
        append_fuel_tank_conditions(self,segment, fuel_line)  
        return                                          