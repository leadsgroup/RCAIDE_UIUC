## @ingroup Methods-Energy-Sources-Battery-Lithium_Ion_NMC
# RCAIDE/Methods/Energy/Sources/Battery/Lithium_Ion_NMC/compute_nmc_cell_performance.py
# 
# 
# Created:  Feb 2024, M. Clarke,
# Modified: Mar 2024 S S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core                       import Units 
from RCAIDE.Library.Methods.Energy.Sources.Battery.Common import compute_thermal_performance
import numpy as np  
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_nmc_cell_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Sources-Batteries-Lithium_Ion_NMC 
def compute_nmc_cell_performance(battery,state,bus,battery_discharge_flag): 
    '''This is an electric cycle model for 18650 lithium-nickel-manganese-cobalt-oxide
       battery cells. The model uses experimental data performed
       by the Automotive Industrial Systems Company of Panasonic Group 

       Sources:  
       Internal Resistance Model:
       Zou, Y., Hu, X., Ma, H., and Li, S. E., "Combined State of Charge and State of
       Health estimation over lithium-ion battery cellcycle lifespan for electric 
       vehicles,"Journal of Power Sources, Vol. 273, 2015, pp. 793-803.
       doi:10.1016/j.jpowsour.2014.09.146,URLhttp://dx.doi.org/10.1016/j.jpowsour.2014.09.146. 

       Battery Heat Generation Model and  Entropy Model:
       Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical lithium ion 
       battery during discharge cycle." Energy Conversion and Management 52.8-9 (2011): 
       2973-2981. 

       Assumtions:
       1) All battery modules exhibit the same themal behaviour. 

       Inputs:
         battery.
               I_bat             (maximum_energy)                      [Joules]
               cell_mass         (battery cell mass)                   [kilograms]
               Cp                (battery cell specific heat capacity) [J/(K kg)] 
               t                 (battery age in days)                 [days] 
               T_ambient         (ambient temperature)                 [Kelvin]
               T_current         (pack temperature)                    [Kelvin]
               T_cell            (battery cell temperature)            [Kelvin]
               E_max             (max energy)                          [Joules]
               E_current         (current energy)                      [Joules]
               Q_prior           (charge throughput)                   [Amp-hrs]
               R_growth_factor   (internal resistance growth factor)   [unitless]

         inputs.
               I_bat             (current)                             [amps]
               P_bat             (power)                               [Watts]

       Outputs:
         battery.
              current_energy                                           [Joules]
              temperature                                              [Kelvin]
              heat_energy_generated                                    [Watts]
              load_power                                               [Watts]
              current                                                  [Amps]
              battery_voltage_open_circuit                             [Volts]
              charge_throughput                                        [Amp-hrs]
              internal_resistance                                      [Ohms]
              battery_state_of_charge                                  [unitless]
              depth_of_discharge                                       [unitless]
              battery_voltage_under_load                               [Volts]

    ''' 

    # Unpack varibles 
    battery            = battery  
    battery_conditions = state.conditions.energy[bus.tag][battery.tag]    
    btms               = battery.thermal_management_system 
    HAS                = btms.heat_acquisition_system
    HEX                = btms.heat_exchanger_system
    RES                = btms.reservoir
    electrode_area     = battery.cell.electrode_area 
    As_cell            = battery.cell.surface_area           
    battery_data       = battery.discharge_performance_map  
    I_bat              = battery.outputs.current
    P_bat              = battery.outputs.power      
    E_max              = battery_conditions.pack.maximum_initial_energy * battery_conditions.cell.capacity_fade_factor
    E_pack             = battery_conditions.pack.energy    
    I_pack             = battery_conditions.pack.current                         
    V_oc_pack          = battery_conditions.pack.voltage_open_circuit            
    V_ul_pack          = battery_conditions.pack.voltage_under_load              
    P_pack             = battery_conditions.pack.power                           
    T_pack             = battery_conditions.pack.temperature                     
    Q_heat_pack        = battery_conditions.pack.heat_energy_generated           
    R_0                = battery_conditions.pack.internal_resistance             
    Q_heat_cell        = battery_conditions.cell.heat_energy_generated           
    SOC                = battery_conditions.cell.state_of_charge                 
    P_cell             = battery_conditions.cell.power                           
    E_cell             = battery_conditions.cell.energy                          
    V_ul               = battery_conditions.cell.voltage_under_load              
    V_oc               = battery_conditions.cell.voltage_open_circuit            
    I_cell             = battery_conditions.cell.current                         
    T_cell             = battery_conditions.cell.temperature                     
    Q_cell             = battery_conditions.cell.charge_throughput               
    DOD_cell           = battery_conditions.cell.depth_of_discharge  
    time               = state.conditions.frames.inertial.time[:,0] 
     
    # Calculate the current going into one cell  
    n_series          = battery.pack.electrical_configuration.series  
    n_parallel        = battery.pack.electrical_configuration.parallel 
    n_total           = battery.pack.electrical_configuration.total   
    
    delta_t           = np.diff(time)
    for t_idx in range(state.numerics.number_of_control_points):   
       
        # Current State  
        I_cell[t_idx]            = I_bat[t_idx]/n_parallel   
 
        # Compute battery cell temperature  
        R_0[t_idx]               =  0.01483*(SOC[t_idx]**2) - 0.02518*SOC[t_idx] + 0.1036  
        R_0[t_idx][R_0[t_idx]<0] = 0. 
        
        # Determine temperature increase         
        sigma                 = 139 # Electrical conductivity
        n                     = 1
        F                     = 96485 # C/mol Faraday constant    
        delta_S               = -496.66*(SOC[t_idx])**6 +  1729.4*(SOC[t_idx])**5 + -2278 *(SOC[t_idx])**4 +  1382.2 *(SOC[t_idx])**3 + \
                                -380.47*(SOC[t_idx])**2 +  46.508*(SOC[t_idx])    + -10.692  
        
        i_cell                = I_cell[t_idx]/electrode_area # current intensity 
        q_dot_entropy         = -(T_cell[t_idx])*delta_S*i_cell/(n*F)       
        q_dot_joule           = (i_cell**2)/sigma                   
        Q_heat_cell[t_idx]    = (q_dot_joule + q_dot_entropy)*As_cell 
        Q_heat_pack[t_idx]    = Q_heat_cell[t_idx]*n_total  
              
        V_ul[t_idx]           = compute_nmc_cell_state(battery_data,SOC[t_idx],T_cell[t_idx],I_cell[t_idx]) 
        
        V_oc[t_idx]           = V_ul[t_idx] + (I_cell[t_idx] * R_0[t_idx])              
        
        # Effective Power flowing through battery  
        P_pack[t_idx]         = P_bat[t_idx] + battery_conditions.thermal_management_system.power[t_idx] - np.abs(Q_heat_pack[t_idx]) 
            
        # store remaining variables 
        I_pack[t_idx]         = I_bat[t_idx]  
        V_oc_pack[t_idx]      = V_oc[t_idx]*n_series 
        V_ul_pack[t_idx]      = V_ul[t_idx]*n_series  
        T_pack[t_idx]         = T_cell[t_idx] 
        P_cell[t_idx]         = P_pack[t_idx]/n_total  
        E_cell[t_idx]         = E_pack[t_idx]/n_total  

        # ---------------------------------------------------------------------------------------------------
        # Current State 
        # --------------------------------------------------------------------------------------------------- 
        if t_idx != state.numerics.number_of_control_points-1:   
            
            # Compute cell temperature   
            compute_thermal_performance(HAS,HEX,RES,battery_conditions,battery,Q_heat_cell,state,delta_t,t_idx)   
            
            # Temperature 
            T_cell[t_idx+1]  =  battery_conditions.cell.temperature[t_idx+1] 
                     
            # Compute state of charge and depth of discarge of the battery
            E_pack[t_idx+1]                          = E_pack[t_idx] -P_pack[t_idx]*delta_t[t_idx] 
            E_pack[t_idx+1][E_pack[t_idx+1] > E_max] = E_max
            SOC[t_idx+1]                             = E_pack[t_idx+1]/E_max 
            SOC[t_idx+1][SOC[t_idx+1]>1]             = 1.
            SOC[t_idx+1][SOC[t_idx+1]<0]             = 0. 
            DOD_cell[t_idx+1]                        = 1 - SOC[t_idx+1]  
            
            # Determine new charge throughput (the amount of charge gone through the battery)
            Q_cell[t_idx+1]    = Q_cell[t_idx] + I_cell[t_idx]*delta_t[t_idx]/Units.hr   
 
    return battery    

## @ingroup Methods-Energy-Sources-Lithium_Ion_NMC
def compute_nmc_cell_state(battery_data,SOC,T,I):
    """This computes the electrical state variables of a lithium ion 
    battery cell with a  lithium-nickel-cobalt-aluminum oxide cathode 
    chemistry from look-up tables 
     
    Assumtions: 
    N/A
    
    Source:  
    N/A 
     
    Inputs:
        SOC           - state of charge of cell     [unitless]
        battery_data  - look-up data structure      [unitless]
        T             - battery cell temperature    [Kelvin]
        I             - battery cell current        [Amperes]
    
    Outputs:  
        V_ul          - under-load voltage          [Volts] 
        
    """  
    SOC[SOC < 0.]   = 0.  
    SOC[SOC > 1.]   = 1.    
    DOD             = 1 - SOC   
    pts             = np.hstack((np.hstack((I, T)),DOD  )) # amps, temp, SOC   
    V_ul            = np.atleast_2d(battery_data.Voltage(pts)[:,1]).T  
    
    return V_ul