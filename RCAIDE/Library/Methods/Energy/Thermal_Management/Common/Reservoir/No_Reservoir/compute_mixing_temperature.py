## @ingroup Energy-Thermal_Management-Batteries-Heat_Addition_Systems
# RCAIDE/Energy/Thermal_Management/Batteries/H
# 
# 
# Created:  Mar 2024, 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data  


# ----------------------------------------------------------------------------------------------------------------------
#  Compute Power Consumed by heating element
# ----------------------------------------------------------------------------------------------------------------------
def compute_mixing_temperature(RES,battery_conditions,state,dt,i,remove_heat):
    
    # Current Reservoir temperature
    T_current                = battery_conditions.thermal_management_system.RES.coolant_temperature[i,0]
   

    battery_conditions.thermal_management_system.RES.coolant_temperature[i+1,0] = T_current
    
    return 
