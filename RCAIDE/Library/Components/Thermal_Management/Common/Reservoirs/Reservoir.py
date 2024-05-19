## @ingroup Library-Compoments-Thermal_Management-Common-Reservoirs
# RCAIDE/Library/Compoments/Thermal_Management/Common/Reservoirs/Reservoir.py
# 
# 
# Created:  Mar 2024, S S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Library.Components import Component 
from RCAIDE.Library.Attributes.Coolants.Glycol_Water                                import Glycol_Water
from RCAIDE.Library.Attributes.Materials.Polyetherimide                             import Polyetherimide
from RCAIDE.Library.Methods.Energy.Thermal_Management.Common.Reservoir.Reservoir import compute_mixing_temperature, compute_reservoir_temperature


# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------
## @ingroup Attributes-Coolants
class Reservoir(Component):
    """Holds values for a coolant reservoir

    Assumptions:
    Thermally Insulated coolant storage device.

    Source:
    None
    """

    def __defaults__(self):
        """This sets the default values.

        Assumptions:
        None

        Source:
        Values commonly available  
        """
        self.tag                       = 'Coolant Reservoir'
        self.material                  = Polyetherimide()
        self.coolant                   = Glycol_Water()
        self.length                    = 0.3                                      # [m]
        self.width                     = 0.3                                      # [m]
        self.height                    = 0.3                                      # [m]
        self.thickness                 = 5e-3                                     # [m]  
        self.surface_area              = 2*(self.length*self.width+self.width*
                                            self.height+self.length*self.height)  # [m^2]
        self.volume                    = self.length*self.width*self.height       # [m^3]

        return

    def compute_reservior_coolant_temperature(RES,battery_conditions,state,dt,i,remove_heat):
        '''
      COMMENTS SAI 
      '''
        compute_mixing_temperature(RES,battery_conditions,state,dt,i,remove_heat)   
        return
    
    def compute_reservior_heat_transfer(RES,battery_conditions,state,dt,i):
        '''
      COMMENTS SAI 
      '''
        
        compute_reservoir_temperature(RES,battery_conditions,state,dt,i)
        
        return