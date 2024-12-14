# RCAIDE/Library/Components/Thermal_Management/Heat_Exchangers/Cross_flow_Heat_Exchanger.py
# 
# Created:  Apr 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports
from RCAIDE.Framework.Core                                                                import Data, Units 
from RCAIDE.Library.Components                                                            import Component  
from RCAIDE.Library.Attributes.Coolants.Glycol_Water                                      import Glycol_Water  
from RCAIDE.Library.Attributes.Gases                                                      import Air
from RCAIDE.Library.Methods.Thermal_Management.Heat_Exchangers.Cross_Flow_Heat_Exchanger  import  cross_flow_hex_rating_model, append_cross_flow_heat_exchanger_conditions, append_cross_flow_hex_segment_conditions
from RCAIDE.Library.Plots.Thermal_Management.plot_cross_flow_heat_exchanger_conditions    import plot_cross_flow_heat_exchanger_conditions 

import os
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Cross Flow Heat Exchanger 
# ----------------------------------------------------------------------------------------------------------------------  
class Cross_Flow_Heat_Exchanger(Component):
    """ This provides outlet fluid properties from a cross flow heat exchanger
    Assumptions:
         Coolant being used is Glycol Water 50-50
         Assume a constant Kc and Kp 

    Source: N/A
   
    """

    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        Surface Designation of 1/8-19.86 with strip fins. 

        Source:
        Kays, W.M. and London, A.L. (1998) Compact Heat Exchangers. 3rd Edition, McGraw-Hill, New York.
        
       
        """         

        self.tag                                                    = 'cross_flow_heat_exchanger'
        self.coolant                                                = Glycol_Water() 
        self.air                                                    = Air() 
        self.design_heat_removed                                    = 0.0
        self.minimum_air_speed                                      = 105 * Units.knots 
        
        # heat exchanger: thermophysical properties                        
        self.heat_exchanger_efficiency                              = 0.8381
        self.density                                                = 8440   # kg/m^3
        self.thermal_conductivity                                   = 121    # W/m.K
        self.specific_heat_capacity                                 = 871    # J/kg.K 


        self.stack_length                                           = 1
        self.stack_width                                            = 1
        self.stack_height                                           = 1
                         
        self.design_air_flow_rate                                   = None 
        self.design_air_inlet_pressure                              = None 
        self.design_coolant_inlet_pressure                          = None 

        # heat exchanger: geometric properties      
        # Plate thickness                       
        self.t_w                                                    = 5e-4   # m

        # Fin Thickness
        self.t_f                                                    = 1e-4   # m

        self.fin_spacing_cold                                       = 2.54e-3 #m
        self.fin_spacing_hot                                        = 2.54e-3 #m

        # Fin metal thickness
        self.fin_metal_thickness_hot                                = 0.102e-3 #m
        self.fin_metal_thickness_cold                               = 0.102e-3 #m

        # Strip edge exposed 
        self.fin_exposed_strip_edge_hot                             = 3.175e-3 #m
        self.fin_exposed_strip_edge_cold                            = 3.175e-3 #m

        # Finned area density 
        self.fin_area_density_hot                                   = 2254 # m^2/m^3 
        self.fin_area_density_cold                                  = 2254 # m^2/m^3 

        # Ratio of finned area to total area 
        self.finned_area_to_total_area_hot                          = 0.785
        self.finned_area_to_total_area_cold                         = 0.785

        # Hydraullic Diameter
        self.coolant_hydraulic_diameter                             = 1.54e-3  #m
        self.air_hydraulic_diameter                                 = 1.54e-3  #m

        # Fin and wall Conductivity 
        self.fin_conductivity                                        = 121    # W/m.K
        self.wall_conductivity                                       = 121    # W/m.K        

        # Fan
        self.fan                                                    = Data() # Replace with RCAIDE Fan 
        self.fan.efficiency                                         = 0.7
        self.fan.active                                             = True 
        
        # Pump 
        self.pump                                                   = Data() # Replace with RCAIDE Fan 
        self.pump.efficiency                                        = 0.7 

        # Operating Conditions 
        self.percent_operation                                      = 1.0
        self.atmospheric_air_inlet_to_outlet_area_ratio             = 0.5 
        self.duct_losses                                            = 0.98 # Inlet, Duct and Nozzle Losses
        self.fan_operation                                          = True


        # Limiting Pressure Drop
        self.pressure_drop_hot                                      = 9.05e3 #Pa 
        self.pressure_drop_cold                                     = 8.79e3 #Pa 


        # Enterance and Exit pressure loss coefficients  
        self.kc_values                                              = load_kc_values()
        self.ke_values                                              = load_ke_values()
        return  

    def append_operating_conditions(self,segment,coolant_line):
        append_cross_flow_heat_exchanger_conditions(self,segment,coolant_line)
        return
  
    def append_segment_conditions(self,segment,bus,coolant_line,conditions):
        append_cross_flow_hex_segment_conditions(self,segment,bus,coolant_line,conditions)
        return
       
    def compute_heat_exchanger_performance(self,state,bus,coolant_line, delta_t,t_idx):
        cross_flow_hex_rating_model(self,state,bus,coolant_line, delta_t,t_idx)
        return
    def plot_operating_conditions(self,results, coolant_line,save_filename,save_figure,show_legend,file_type ,width, height):
        plot_cross_flow_heat_exchanger_conditions(self,results,coolant_line,save_filename,save_figure,show_legend,file_type,width,height)     
        return    

    def load_kc_values(): 
        ospath    = os.path.abspath(__file__)
        separator = os.path.sep
        rel_path  = os.path.dirname(ospath) + separator   
        x         = np.loadtxt(rel_path + 'rectangular_passage_Kc.csv', dtype=float, delimiter=',', comments='Kc') 
        return x 
    
    def load_ke_values():  
        ospath    = os.path.abspath(__file__)
        separator = os.path.sep
        rel_path  = os.path.dirname(ospath) + separator 
        x         = np.loadtxt(rel_path +'rectangular_passage_Ke.csv', dtype=float, delimiter=',', comments='Ke')
        return x 