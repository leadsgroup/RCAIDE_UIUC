## @ingroup Energy-Thermal_Management-Batteries-Heat_Acquisition_Systems
# RCAIDE/Energy/Thermal_Management/Batteries/Heat_Acquisition_Systems/No_Removal_System.py 

# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
  
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Energy.Thermal_Management.Common.Heat_Exchanger_Systems.No_Heat_Exchanger import no_heat_exchanger_model

# ----------------------------------------------------------------------------------------------------------------------
#  No_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries-Heat_Acquisition_Systems
class No_Heat_Exchanger(Component):
    """This provides output values for a direct convention heat exchanger of a bettery pack
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):  
        self.tag                           = 'No_Heat_Exchanger'
        self.design_air_inlet_pressure     = 0 
        self.design_coolant_inlet_pressure = 0 
        self.design_air_mass_flow_rate     = 0
        self.design_coolant_mass_flow_rate = 0   
        return
    
    def compute_heat_removed(HEX,battery_conditions,state,dt,i): 
        '''Computes the heat removed to the atmosphwere with no heat exchanger system
        
        Assumtions:
        None
        
        Source
        None 
        
        Inputs:
        HEX                   - heat exchanger   system                        [-]
        battery_conditions    - battery pack conditions                        [-]  
        state                 - conditions of system                           [-]
        dt                    - time step                                      [s]
        i                     - control point                                  [-]
        
        Outputs  
        '''  
             
        HEX_results = no_heat_exchanger_model(HEX,battery_conditions,state, dt, i)
              
        return HEX_results
     
    
        
