# RCAIDE/Library/Compoments/Energy/Sources/Battery_Modules/Generic_Battery_Module.py
# 
# 
# Created:  Mar 2024, M. Clarke
# Modified: Sep 2024, S. Shekar
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
from RCAIDE.Framework.Core        import Data
from RCAIDE.Library.Components    import Component   
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Common.append_battery_conditions import append_battery_conditions, append_battery_segment_conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Battery
# ----------------------------------------------------------------------------------------------------------------------      
class Generic_Battery_Module(Component):
    """Default battery module class."""
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """
      
       
        self.energy_density                                    = 0.0
        self.current_energy                                    = 0.0
        self.current_capacitor_charge                          = 0.0
        self.capacity                                          = 0.0
            
        self.length                                            = 0.0
        self.width                                             = 0.0
        self.height                                            = 0.0
        self.volume_packaging_factor                           = 1.05
        self.BMS_additional_weight_factor                      = 1.42
                 
        self.orientation_euler_angles                          = [0.,0.,0.]  # vector of angles defining default orientation of rotor        
                     
        self.cell                                              = Data()
        self.cell.chemistry                                    = None                             
        self.cell.discharge_performance_map                    = None  
        self.cell.ragone                                       = Data()
        self.cell.ragone.const_1                               = 0.0     # used for ragone functions; 
        self.cell.ragone.const_2                               = 0.0     # specific_power=ragone_const_1*10^(specific_energy*ragone_const_2)
        self.cell.ragone.lower_bound                           = 0.0     # lower bound specific energy for which ragone curves no longer make sense
        self.cell.ragone.i                                     = 0.0 
 
        self.electrical_configuration                          = Data()
        self.electrical_configuration.series                   = 1
        self.electrical_configuration.parallel                 = 1   
        
        self.geometrtic_configuration                          = Data() 
        self.geometrtic_configuration.normal_count             = 1
        self.geometrtic_configuration.parallel_count           = 1
        self.geometrtic_configuration.normal_spacing           = 0.02
        self.geometrtic_configuration.stacking_rows            = 3
        self.geometrtic_configuration.parallel_spacing         = 0.02                
 
    def append_operating_conditions(self,segment,bus):  
        append_battery_conditions(self,segment,bus)  
        return
    
    def append_battery_segment_conditions(self,bus, conditions, segment):
        append_battery_segment_conditions(self,bus, conditions, segment)
        return