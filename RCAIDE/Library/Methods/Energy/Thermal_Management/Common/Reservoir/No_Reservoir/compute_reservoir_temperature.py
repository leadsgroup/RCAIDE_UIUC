## @ingroup Library-Energy-Methods-Thermal_Management-Common
# RCAIDE/Library/Methods/Energy/Thermal_Management/Common/Reservoir/No_Reservoir/compute_reservoir_temperature.py


# Created:  Apr 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute heat loss to environment 
# ----------------------------------------------------------------------------------------------------------------------

def compute_reservoir_temperature(RES,battery_conditions,state,dt,i):
    """
     Computes the resultant temperature of the reservoir at each time step with coolant loosing heat to the environment
          
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
    # Ambient Air Temperature 
    T_ambient                   = state.conditions.freestream.temperature[i,0] 
    
    battery_conditions.thermal_management_system.RES.coolant_temperature[i+1,0] = T_ambient

    return 
