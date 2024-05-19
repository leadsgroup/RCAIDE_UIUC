## @ingroup Library-Energy-Methods-Thermal_Management-Common
# RCAIDE/Library/Methods/Energy/Thermal_Management/Common/Reservoir/No_Reservoir/compute_mixing_temperature.py


# Created:  Apr 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute resultant temperature of the reservoir
# ----------------------------------------------------------------------------------------------------------------------
def compute_mixing_temperature(RES,battery_conditions,state,dt,i):
    """
     Computes the resultant temperature of the reservoir at each time step with coolant pouring in from the HAS and the HEX 
          
          Inputs: 
                 HAS
                 HEX
                 battery_conditions
                 dt
                 i 
             
          Outputs:
                 RES.coolant.temperature
                 
          Assumptions: 
             N/A
        
          Source:

    
    """
    
    # Current Reservoir temperature
    T_current                = battery_conditions.thermal_management_system.RES.coolant_temperature[i,0]
   

    battery_conditions.thermal_management_system.RES.coolant_temperature[i+1,0] = T_current
    
    return 
