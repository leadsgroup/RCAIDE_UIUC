## @ingroup Methods-Energy-Thermal_Management-Batteries-Heat_Acquisition_Systems
# RCAIDE/Methods/Energy/Thermal_Management/Batteries/Heat_Acquisition_Systems/wavy_channel_rating_model.py
# 
# 
# Created:  Apr 2024, M. Clarke, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Data  
from RCAIDE.Library.Components.Thermal_Management.Common.Accessories import Pump  

# python package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Wavy Channel Rating Model
# ----------------------------------------------------------------------------------------------------------------------
def  wavy_channel_rating_model(HAS,battery_conditions,battery,Q_heat_cell,state,dt,i):
    """ 
          
          Inputs: 
          HAS.
             channel_side_thicknes
             channel_width        
             channel_contact_angle
             channel_top_thickness
             channel
             heat_transfer_efficiency
             coolant  
             coolant_flow_rate
          battery.
                  cell.diameter
                  cell.height  
                  module.geometrtic_configuration.parallel_count
                  module.geometrtic_configuration.series_count
                  pack.number_of_modules 
                  cell.specific_heat_capacity
          battery_conditions.
                             thermal_management_system.RES.coolant_temperature 
                             thermal_management_system.percent_operation
                             cell.temperature
                             
          Outputs:
                battery_conditions.
                                   thermal_management_system.heat_generated                 
                                   thermal_management_system.HAS.heat_removed               
                                   thermal_management_system.HAS.outlet_coolant_temperature
                                   thermal_management_system.HAS.coolant_mass_flow_rate     
                                   thermal_management_system.HAS.power 
                                   thermal_management_system.HAS.effectiveness              
                                   cell.temperature                            
          Assumptions: 
             The wavy channel extracts from the battery pack considering it to be a lumped mass.  
        
          Source:
            Zhao, C., Clarke, M., Kellermann H., Verstraete D., “Design of a Liquid Cooling System for Lithium-Ion Battery Packs for eVTOL Aircraft" 
    """        
 
    # Inlet Properties from mission solver. 
    T_inlet                  = battery_conditions.thermal_management_system.RES.coolant_temperature[i,0] 
    turndown_ratio           = battery_conditions.thermal_management_system.percent_operation[i,0] 
    T_cell                   = battery_conditions.cell.temperature[i,0]  
    heat_transfer_efficiency = HAS.heat_transfer_efficiency   

    # Coolant Properties
    opt_coolant                 = compute_coolant_properties(HAS,T_inlet,state,dt,i)
    m_coolant                   = opt_coolant.flowrate*turndown_ratio
    T_i                         = T_inlet
    rho                         = opt_coolant.inlet_density    
    mu                          = opt_coolant.inlet_visc       
    cp                          = opt_coolant.inlet_Cp         
    Pr                          = opt_coolant.inlet_Pr         
    k                           = opt_coolant.inlet_thermal_cond
    
    # Battery Properties
    d_cell                      = battery.cell.diameter                    
    h_cell                      = battery.cell.height                      
    A_cell                      = np.pi*d_cell*h_cell 
    N_cells                     = battery.module.geometrtic_configuration.parallel_count*battery.module.geometrtic_configuration.normal_count  # these are the number of cells in a given module right?  
    cell_mass                   = battery.cell.mass
    T_bat                       = T_cell
    Nn_module_cells             = battery.module.geometrtic_configuration.normal_count            
    Np_module_cells             = battery.module.geometrtic_configuration.parallel_count    
    number_of_modules           = battery.pack.number_of_modules 
    number_of_cells_in_module   = Nn_module_cells*Np_module_cells  
    N_mod                       = battery.pack.number_of_modules 
    Q_module                    = Q_heat_cell*number_of_cells_in_module
    Q_pack                      = Q_module*number_of_modules 
    Cp_bat                      = battery.cell.specific_heat_capacity 

    # Channel Properties
    b         = HAS.channel_side_thickness                
    d         = HAS.channel_width                         
    theta     = HAS.channel_contact_angle    
    c         = battery.cell.height 
    a         = HAS.channel_top_thickness  
    channel   = HAS.channel
    AR        = d/c    
    k_chan    = channel.thermal_conductivity    
    n_pump    = 0.7 # replace with pump class  SAI 

    # Considering a lumped mass model   
    N_cells  = battery.module.geometrtic_configuration.parallel_count*battery.module.geometrtic_configuration.normal_count
    
    # Contact Surface area of the channel 
    A_chan   = 2*N_cells*(theta)*A_cell  

    #Length of Channel   
    L_extra  = battery.module.geometrtic_configuration.parallel_count*d_cell
    L_chan   = (N_cells*d_cell)+L_extra 

    # Hydraulic diameter    
    dh   = (4*c*d)/(2*(c+d))   
    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant

    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu

    # fanning friction factor (eq 32),  Nusselt Number (eq 12)   
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*(AR**2))-(1.7012*(AR**3))+(0.9564*(AR**4))-(0.2537*(AR**5)))/Re
        Nu = 8.235*(1-(2.0421*AR)+(3.0853*(AR**2))-(2.4765*(AR**3))+(1.0578*(AR**4))-(0.1861*(AR**5)))   
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)
        Nu = ((f/2)*(Re-1000)*Pr)/(1+(12.7*((f/2)**0.5)*(Pr**(2/3)-1)))   

    # Calculate the pressure drop in the channel 
    dp     = 2*f*rho*v*v*L_chan/dh	 
    
    # heat transfer coefficient of the channeled coolant (eq 11)
    h = k*Nu/dh

    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(b/k_chan))

    # Calculate NTU
    NTU = U_total*A_chan/(m_coolant*cp)
    
    # Effectiveness of the Channel 
    eff_HAS = 1 - np.exp(-NTU)

    # Calculate Outlet Temparture To ( eq 8)
    T_o = ((T_bat-T_i)*(1-np.exp(-NTU)))+T_i   # SAI - THE ISSUE STARTS HERE T_bat >T_i

    # Calculate the Log mean temperature 
    T_lm = ((T_bat-T_i)-(T_bat-T_o))/(np.log((T_bat-T_i)/(T_bat-T_o)))
    
    # Calculated Heat Convected 
    Q_convec = U_total*A_chan*T_lm*eff_HAS     
    
    # check the wavy channel effectiveness
    heat_transfer_efficiency_new      = (T_o - T_i) / (T_cell - T_i)
    delta_eff_WavyChan                = np.abs(heat_transfer_efficiency - heat_transfer_efficiency_new) #Possible Regression check point  SAI 

    # check the heat generated  
    Q_conv_check            = m_coolant * cp * (T_o - T_i)
    delta_Q_conv            = np.abs(Q_convec - Q_conv_check) #Possible Regression check point  SAI 
    
    # Calculate the Power consumed
    Power   = N_mod*Pump.compute_power_consumed(dp, rho, m_coolant, n_pump) 
    
    # Update temperature of Battery Pack
    P_net                   = Q_module - Q_convec
    dT_dt                   = P_net/(cell_mass*N_cells*Cp_bat)
    T_current               = T_bat + dT_dt*dt 

    battery_conditions.thermal_management_system.heat_generated[i+1]                    = Q_pack
    battery_conditions.thermal_management_system.HAS.heat_removed[i+1]                  = Q_convec*N_mod 
    battery_conditions.thermal_management_system.HAS.outlet_coolant_temperature[i+1]    = T_o
    battery_conditions.thermal_management_system.HAS.coolant_mass_flow_rate[i+1]        = m_coolant
    battery_conditions.thermal_management_system.HAS.power[i+1]                         = Power
    battery_conditions.thermal_management_system.HAS.effectiveness[i+1]                 = heat_transfer_efficiency_new
    battery_conditions.cell.temperature[i+1]                                            = T_current     

    return  



def compute_coolant_properties(HAS,T_i,state,dt,i):
    
    coolant    = HAS.coolant  
    m_coolant  = HAS.coolant_flow_rate 
    rho        = coolant.compute_density(T_i) # Keep track of units
    mu         = coolant.compute_absolute_viscosity(T_i)  
    cp         = coolant.compute_cp(T_i)
    Pr         = coolant.compute_prandtl_number(T_i) 
    k          = coolant.compute_thermal_conductivity(T_i)         
        
    opt_coolant_properties = Data(flowrate             =m_coolant,
                                  inlet_temperature    =T_i,
                                  inlet_density        =rho,
                                  inlet_visc           =mu,
                                  inlet_Cp             =cp,
                                  inlet_Pr             =Pr,
                                  inlet_thermal_cond   =k)


    return opt_coolant_properties






