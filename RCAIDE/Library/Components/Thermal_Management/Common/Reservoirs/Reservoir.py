## @ingroup Energy-Thermal_Management-Batteries-Reservoir
# RCAIDE/Energy/Thermal_Management/Batteries/Reservoir/Reservoir.py
# 
# 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
 
from RCAIDE.Energy.Energy_Component                                         import Energy_Component   
from RCAIDE.Attributes.Coolants.Glycol_Water                                import Glycol_Water
from RCAIDE.Attributes.Materials.Polyetherimide                             import Polyetherimide
from RCAIDE.Methods.Energy.Thermal_Management.Batteries.Reservoir.Reservoir import compute_mixing_temperature, compute_reservoir_temperature


# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------
## @ingroup Attributes-Coolants
class Reservoir(Energy_Component):
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