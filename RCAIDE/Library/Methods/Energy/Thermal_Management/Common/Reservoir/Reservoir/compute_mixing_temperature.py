## @ingroup Library-Energy-Methods-Thermal_Management-Common
# RCAIDE/Library/Methods/Energy/Thermal_Management/Common/Reservoir/No_Reservoir/compute_mixing_temperature.py


# Created:  Apr 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute resultant temperature of the reservoir
# ----------------------------------------------------------------------------------------------------------------------
def compute_mixing_temperature(RES,battery_conditions,state,dt,i,remove_heat):
    
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
    
    # Reservior Properties
    coolant                  = RES.coolant 
    rho_coolant              = coolant.compute_density(T_current)    
    volume                     = RES.volume
    mass_coolant               = rho_coolant*volume
    
    
    # Inputs frm HAS and HEX
    mass_flow_HAS            =  battery_conditions.thermal_management_system.HAS.coolant_mass_flow_rate[i+1]    
    T_HAS                    =  battery_conditions.thermal_management_system.HAS.outlet_coolant_temperature[i+1] 
    
    if remove_heat == True: 
        mass_flow_HEX        =  battery_conditions.thermal_management_system.HEX.coolant_mass_flow_rate[i+1]  
        T_HEX                =  battery_conditions.thermal_management_system.HEX.outlet_coolant_temperature[i+1]   
    else:
        mass_flow_HEX        = 0
        T_HEX                = 0
    
     #Coolant Properties
    
    
    # Calculate mass coming into reservoir.
    mass_HAS                = mass_flow_HAS*dt
    mass_HEX                = mass_flow_HEX*dt
    mass_RES                = mass_coolant-mass_HAS-mass_HEX
    
    Cp_HAS                   = coolant.compute_cp(T_HAS)
    Cp_HEX                   = coolant.compute_cp(T_HEX)
    Cp_RES                   = coolant.compute_cp(T_current)
    
    # Calculate the final temperature 
    T_final                 = (mass_HAS*Cp_HAS*T_HAS+mass_HEX*Cp_HEX*T_HEX+mass_RES*Cp_RES*T_current)/(mass_coolant*Cp_RES)
    
    battery_conditions.thermal_management_system.RES.coolant_temperature[i+1,0] = T_final
    
    return 
