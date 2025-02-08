# RCAIDE/Library/Attributes/Solids/Copper.py
# 

# Created: Jan 2025 M. Clarke

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Solid import Solid
from RCAIDE.Framework.Core import Units  

#-------------------------------------------------------------------------------
# Copper Class
#------------------------------------------------------------------------------- 
class Copper(Solid): 
    """ Physical constants specific toCopper 
    """

    def __defaults__(self):
        """Sets material properties at instantiation. 

        Assumptions:
            None
    
        Source:
            Guo, Ruochen, et al. "Electrical Architecture of 90-seater Electric Aircraft: A Cable Perspective."
            IEEE Transactions on Transportation Electrification (2024).
        """
        self.density                              = 8960.0  * Units['kg/(m**3)']        
        self.electrical_conductivity              = 5.87E7  # [s/m]
        self.thermal_conductivity                 = 400     # [W/(m*K)]
        self.resistance_temperature_scale_factor  = 0.00394 # [/degree C] 
        self.fatigue_life_cycles                  = 300E6
        self.modulus_of_elasticity                = 110E9  * Units.Pa
        self.yield_tensile_strength               = 210E6  * Units.Pa
        self.eletrical_resistivity                = 1.77E-8  # [Ohm/m] at 20C
        
        return 