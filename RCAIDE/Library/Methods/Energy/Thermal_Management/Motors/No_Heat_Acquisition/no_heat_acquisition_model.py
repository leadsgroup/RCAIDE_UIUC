## @ingroup Methods-Thermal_Management-Batteries-Heat_Acquisition_System-No_Heat_Acquisition
# RCAIDE/Methods/Thermal_Management/Batteries/Heat_Acquisition_System/No_Heat_Acquisition/direct_convection_model.py
# 
# 
# Created:  Jul 2023, M. Clarke
"""
*************** Subject to Change *****************************************
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Net Convected Heat 
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Thermal_Management-Batteries-Atmospheric_Air_Convection_Cooling 
def no_heat_acquisition_model(HAS,battery,Q_heat_gen,T_cell,state,dt,i):
    '''Computes no heat removed by heat acquisition system. Battery simply accumulated heat. 

    Assumptions:
        None
        
    Inputs:  
        battery. 
              h                         (heat transfer coefficient)  [W/(m^2*K)] 
              As_cell                   (battery cell surface area)  [meters^2]
              H_cell                    (battery cell height)        [meters]
              T_ambient                 (ambient temperature)        [Kelvin]
              T_current                 (pack temperature)           [Kelvin]
              T_cell                    (battery cell temperature)   [Kelvin] 
              heat_transfer_efficiency                               [unitless]
      
      Outputs:
        battery. 
             net_power                                               [Watts] 
 

    Properties Used:
    None 
    ''' 
    
    # battery properties           
    cell_mass                = battery.cell.mass    
    Cp                       = battery.cell.specific_heat_capacity    
    Nn                       = battery.module.geometrtic_configuration.normal_count            
    Np                       = battery.module.geometrtic_configuration.parallel_count    
    n_total_module           = Nn*Np    
    Q_convec                 = 0
    
    if n_total_module == 1:  
        Q_heat_gen_tot = Q_heat_gen  
    else: 
        Q_heat_gen_tot = Q_heat_gen*n_total_module 
     
    dT_dt                  = Q_heat_gen_tot /(cell_mass*n_total_module*Cp)
    T_current              = T_cell + dT_dt*dt   
    HAS_outputs            = Data(total_heat_generated = Q_heat_gen_tot, 
                                  total_heat_removed   = Q_convec,
                                  current_battery_temperature = T_current)
    
    return HAS_outputs