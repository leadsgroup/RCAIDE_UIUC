# RCAIDE/Library/Compoments/Thermal_Management/Reservoirs/Reservoir.py
# 
# 
# Created:  Mar 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Library.Components                                                      import Component 
from RCAIDE.Library.Attributes.Coolants.Glycol_Water                                import Glycol_Water
from RCAIDE.Library.Attributes.Materials.Polyetherimide                             import Polyetherimide
from RCAIDE.Library.Methods.Thermal_Management.Reservoirs.Reservoir_Tank            import compute_mixing_temperature, append_reservoir_conditions, append_reservoir_segment_conditions
from RCAIDE.Library.Plots.Thermal_Management.plot_reservoir_conditions              import plot_reservoir_conditions

# ----------------------------------------------------------------------
#  Reservoir
# ---------------------------------------------------------------------- 
class Reservoir(Component):
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
        """
        self.tag                          = 'coolant_reservoir'
        self.material                     = Polyetherimide()
        self.coolant                      = Glycol_Water()
        self.length                       = 0.3                                      # [m]
        self.width                        = 0.3                                      # [m]
        self.height                       = 0.3                                      # [m]
        self.thickness                    = 5e-3                                     # [m] 
        self.surface_area                 = 2*(self.length*self.width+self.width*
                                               self.height+self.length*self.height)  # [m^2]
        self.volume                       = self.length*self.width*self.height       # [m^3]
        self.mass_properties.mass         = self.coolant.density*self.volume

        return
    
    def append_operating_conditions(self,segment,coolant_line):
        append_reservoir_conditions(self,segment,coolant_line)
        return
    
    def append_segment_conditions(self,segment,coolant_line,conditions):
        append_reservoir_segment_conditions(self,segment,coolant_line,conditions)
        return    

    def compute_reservior_coolant_temperature(self,state,coolant_line,delta_t,t_idx):
        compute_mixing_temperature(self,state,coolant_line,delta_t,t_idx)
        return
    
    def plot_operating_conditions(self,results, coolant_line,save_filename, save_figure,show_legend,file_type,width, height):
        plot_reservoir_conditions(self, results, coolant_line,save_filename,save_figure,show_legend,file_type,width, height)
        return    
