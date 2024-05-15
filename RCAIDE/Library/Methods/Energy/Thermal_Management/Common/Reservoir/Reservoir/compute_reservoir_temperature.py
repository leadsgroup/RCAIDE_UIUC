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
    
    # properties of Reservoir
    A_surface                  = RES.surface_area
    volume                     = RES.volume
    T_current                  = battery_conditions.thermal_management_system.RES.coolant_temperature[i+1,0]
    thickness                  = RES.thickness
    conductivity               = RES.material.conductivity
    emissivity_res             = RES.material.emissivity
    
    #Coolant Properties
    coolant                    = RES.coolant 
    Cp                         = coolant.compute_cp(T_current)
    rho_coolant                = coolant.compute_density(T_current)

    # Heat Transfer properties
    conductivity               = RES.material.conductivity
    sigma                       = 5.69e-8   #Stefan Boltzman Constant
    h                           = 10       #[W/m^2-k]
    emissivity_air              = 0.9
    

    # Heat Transfer due to conduction. 
    dQ_dt_cond                  = conductivity*A_surface*(T_current-T_ambient)/(thickness)

    # Heat Transfer dur to natural convention 
    dQ_dt_conv                  = h*A_surface*(T_current-T_ambient)

    # Heat Transfer due to radiation 
    dQ_dt_rad                   = sigma*A_surface*((emissivity_res*T_current**4)-(emissivity_air*T_ambient**4)) 

    dQ_dt                       = (dQ_dt_cond+dQ_dt_conv+dQ_dt_rad)
    
    # Compute mass of coolant present in the reservoir
    mass_coolant               = rho_coolant*volume
    
    dT_dt                       = dQ_dt/(mass_coolant*Cp)
    T_current                   = T_current - dT_dt*dt
    
    # Update the reservoir temperaure. 
    battery_conditions.thermal_management_system.RES.coolant_temperature[i+1,0] = T_current

    return