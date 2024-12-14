# RCAIDE/Energy/Thermal_Management/Batteries/Air_Cooled.py
# 
# 
# Created:  Jul 2023, M. Clarke
# Modified: Aug 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
  
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Thermal_Management.Batteries.Air_Cooled import append_air_cooled_conditions, air_cooled_performance, append_air_cooled_segment_conditions
from RCAIDE.Library.Attributes.Gases import Air
from RCAIDE.Library.Plots.Thermal_Management.plot_air_cooled_conditions import  plot_air_cooled_conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Air_Cooled_Heat_Acquisition_System
# ----------------------------------------------------------------------------------------------------------------------
class Air_Cooled(Component):
    """This provides output values for a direct convention heat acquisition of a bettery pack
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """                 
        self.tag                                      = 'air_cooled_heat_acquisition'
        self.cooling_fluid                            = Air()    
        self.cooling_fluid.flowspeed                  = 0.01                                          
        self.convective_heat_transfer_coefficient     = 35.     # [W/m^2K] 
        self.heat_transfer_efficiency                 = 1.0      
   
    
    def append_operating_conditions(self,segment,coolant_line):
        append_air_cooled_conditions(self,segment,coolant_line)
        return
    def append_segment_conditions(self, segment,coolant_line, conditions):
        append_air_cooled_segment_conditions(self, segment,coolant_line, conditions)
        return
    
    def compute_thermal_performance(self,battery,bus,coolant_line,Q_heat_gen,T_cell,state,delta_t,t_idx): 
        T_battery_current = air_cooled_performance(self,battery,bus,coolant_line, Q_heat_gen,T_cell,state,delta_t,t_idx)
        return T_battery_current

    def plot_operating_conditions(self, results, coolant_line,save_filename, save_figure,show_legend,file_type , width, height):
        plot_air_cooled_conditions(self, results, coolant_line,save_filename, save_figure,show_legend,file_type , width, height)
        return
        
