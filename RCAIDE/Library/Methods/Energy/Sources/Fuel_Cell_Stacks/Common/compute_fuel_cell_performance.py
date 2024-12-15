# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Cell_Stacks.Generic   import find_voltage_larminie, find_power_diff_larminie

import numpy as np
import scipy as sp
# ----------------------------------------------------------------------
#  Larminie
# ----------------------------------------------------------------------


def compute_fuel_cell_performance(fuel_cell_stack,state,bus,coolant_lines,t_idx,delta_t):
    '''
    function that determines the fuel cell voltage based on an input
    current density and some semi-empirical values to describe the voltage
    drop off with current

    Assumptions:
    voltage curve is a function of current density of the form
    v = Eoc-r*i1-A1*np.log(i1)-m*np.exp(n*i1)

    Inputs:
    current_density           [A/m**2]
    fuel_cell.
        r                     [Ohms*m**2]
        A1                    [V]
        m                     [V]
        n                     [m**2/A]
        Eoc                   [V]

    Outputs:
        V                     [V] 
    '''
    # ---------------------------------------------------------------------------------    
    # fuel cell properties
    # ---------------------------------------------------------------------------------  
    fuel_cell  = fuel_cell_stack.fuel_cell
    
    # ---------------------------------------------------------------------------------
    # Compute Bus electrical properties 
    # ---------------------------------------------------------------------------------    
    bus_conditions              = state.conditions.energy[bus.tag] 
    P_bus                       = bus_conditions.power_draw 


    if fuel_cell.discharge_model == 'Simple': 
        # ---------------------------------------------------------------------------------
        # Compute fuel_cell_stack Conditions
        # -------------------------------------------------------------------------    
        fuel_cell_stack_conditions = state.conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag] 


        #mass flow rate of the fuel  
        mdot        = P_bus[t_idx]/(fuel_cell.propellant.specific_energy*fuel_cell.efficiency) 

        fuel_cell_stack_conditions.fuel_cell.inputs.fuel_mass_flow_rate[t_idx]        = mdot 

    else: # use  Larminie

        power           = fuel_cell.inputs.power_in  
        lb              = .1*Units.mA/(Units.cm**2.)    #lower bound on fuel cell current density
        ub              = 1200.0*Units.mA/(Units.cm**2.)
        current_density = np.zeros_like(power)

        for i in range(len(power)):
            current_density[i] = sp.optimize.fminbound(find_power_diff_larminie, lb, ub, args=(fuel_cell, power[i]))

        v          = find_voltage_larminie(fuel_cell,current_density)    
        efficiency = np.divide(v, fuel_cell.ideal_voltage)
        mdot       = np.divide(power,np.multiply(fuel_cell.propellant.specific_energy,efficiency))        
        fuel_cell_stack_conditions.fuel_cell.inputs.fuel_mass_flow_rate[t_idx]        = mdot
        
    stored_results_flag            = True
    stored_fuel_cell_stack_tag     = fuel_cell_stack.tag  

    return  stored_results_flag, stored_fuel_cell_stack_tag


