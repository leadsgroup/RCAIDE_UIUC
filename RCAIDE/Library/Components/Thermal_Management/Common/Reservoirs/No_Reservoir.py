

## @ingroup Energy-Thermal_Management-Batteries-Reservoir
# RCAIDE/Energy/Thermal_Management/Batteries/Reservoir/Reservoir.py
# 
# 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
 
from RCAIDE.Energy.Energy_Component import Energy_Component   
from RCAIDE.Methods.Energy.Thermal_Management.Batteries.Reservoir.No_Reservoir import compute_mixing_temperature, compute_reservoir_temperature

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------
## @ingroup Attributes-Coolants
class No_Reservoir(Energy_Component):
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

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """
        self.tag                       = None
        self.material                  = None
        self.coolant                   = None
        self.length                    = 0.0                                      # [m]
        self.width                     = 0.0                                      # [m]
        self.height                    = 0.0                                      # [m]
        self.thickness                 = 0.0                                      # [m]  
        self.surface_area              = 2*(self.length*self.width+self.width*
                                            self.height+self.length*self.height)  # [m^2]
        self.volume                    = self.length*self.width*self.height       # [m^3]
        self.conductivity              = 0.0                                      # [W/m-K]
        self.emissivity                = 0.0                                      # [uniteless]
        self.specific_heat             = 0.0              

        return
    
    
    def compute_reservior_coolant_temperature(RES,battery_conditions,state,dt,i,remove_heat):
        compute_mixing_temperature(RES,battery_conditions,state,dt,i,remove_heat)   
        return
    
    def compute_reservior_heat_transfer(RES,battery_conditions,state,dt,i):
        
        compute_reservoir_temperature(RES,battery_conditions,state,dt,i)
        
        return
