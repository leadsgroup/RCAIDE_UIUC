# reformer_test.py
# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

#----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core                              import Units, Data
from RCAIDE.Library.Plots                               import *     
from RCAIDE.Framework.Mission.Common import Conditions, Results, Residuals
from RCAIDE.Library.Methods.Propulsors.Converters import Reformer
from RCAIDE.Library.Methods.Propulsors.Converters.Reformer.compute_reformer_performance import compute_reformer_performance

import os
import numpy as np 
import matplotlib.pyplot as plt

# python imports 
import numpy as np
import pylab as plt 
import sys
import os

 
def main(): 

    Q_R_truth     = [541.1430179999999]    
    eta_ref_truth = [84.71907896694455]
    X_H2_truth    = [34.39020112581373]   
    GHSV_truth    = [7188.869229234659]   
    LHSV_truth    = [1.5104112711074276]   
    S_C_truth     = [3.5173918343579538]    
    O_C_truth     = [0.011870136164444744]    
    phi_truth     = [4.13667981438515]    

    reformer = design_test_reformer()

    # set up conditions  
    ctrl_pts = 1

    reformer_conditions = RCAIDE.Framework.Mission.Common.Conditions()

    reformer_conditions.fuel_volume_flow_rate  = np.ones((ctrl_pts,1)) * reformer.eta * 4.5e-9       # [m**3/s]        Jet-A feed rate
    reformer_conditions.steam_volume_flow_rate = np.ones((ctrl_pts,1)) * reformer.eta * 1.6667e-8    # [m**3/s]        Deionized water feed rate
    reformer_conditions.air_volume_flow_rate   = np.ones((ctrl_pts,1)) * reformer.eta * 1e-5         # [m**3/s]        Air feed rate

    compute_reformer_performance(reformer,reformer_conditions)

    Q_R     =  reformer_conditions.effluent_gas_flow_rate  
    eta_ref =  reformer_conditions.reformer_efficiency 
    X_H2    =  reformer_conditions.hydrogen_conversion_efficiency 
    GHSV    =  reformer_conditions.space_velocity 
    LHSV    =  reformer_conditions.liquid_space_velocity 
    S_C     =  reformer_conditions.steam_to_carbon_feed_ratio 
    O_C     =  reformer_conditions.oxygen_to_carbon_feed_ratio 
    phi     =  reformer_conditions.fuel_to_air_ratio 

    # Truth values 
    error = Data()
    error.Q_R_test     = np.max(np.abs(Q_R_truth     - Q_R[0][0]  ))
    error.eta_ref_test = np.max(np.abs(eta_ref_truth - eta_ref[0][0]))
    error.X_H2_test    = np.max(np.abs(X_H2_truth    - X_H2[0][0]))
    error.GHSV_test    = np.max(np.abs(GHSV_truth    - GHSV[0][0]))
    error.LHSV_test    = np.max(np.abs(LHSV_truth    - LHSV[0][0]))
    error.S_C_test     = np.max(np.abs(S_C_truth     - S_C[0][0]))
    error.O_C_test     = np.max(np.abs(O_C_truth     - O_C[0][0]))
    error.phi_test     = np.max(np.abs(phi_truth     - phi[0][0]))

    print('Errors:')
    print(error)
    
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6) 
               
    return

def design_test_reformer():

    reformer = RCAIDE.Library.Components.Propulsors.Converters.Reformer()

    reformer.tag          = 'reformer'  
    # Jet-A parameters
    reformer.x_H          = 0.1348   # [-]               mass fraction of hydrogen content in Jet-A
    reformer.x_C          = 0.8637   # [-]               mass fraction of carbon content in Jet-A
        
    # Reformate parameters
    reformer.y_H2         = 0.9      # [mol]             mole fraction of hydrogen content in reformate
    reformer.y_CO         = 0.3      # [mol]             mole fraxtion of carbon monoxide content in reformate
    
    # Reformer parameters
    reformer.rho_F        = 0.813    # [g/cm**3]         Density of Jet-A
    reformer.rho_S        = 1        # [g/cm**3]         Density of water
    reformer.rho_A        = 0.001293 # [g/cm**3]         Density of air
    reformer.MW_F         = 160      # [g/g-mol]         Average molecular weight of Jet-A    
    reformer.MW_S         = 18.01    # [g/g-mol]         Average molecular weight of steam
    reformer.MW_C         = 12.01    # [g/g-mol]         Average molecular weight of carbon
    reformer.MW_H2        = 2.016    # [g/g-mol]         Average molecular weight of hydrogen
    reformer.A_F_st_Jet_A = 14.62    # [lb_Air/lb_Jet_A] Stoichiometric air-to-fuel mass ratio 
    reformer.theta        = 0.074    # [sec**-1]         Contact time
    reformer.LHV_F        = 43.435   # [kJ/g-mol]        Lower heating value of Jet-A
    reformer.LHV_H2       = 240.2    # [kJ/g-mol]        Lower heating value of Hydrogen
    reformer.LHV_CO       = 283.1    # [kJ/g-mol]        Lower heating value of Carbon Monoxide
    reformer.V_cat        = 9.653    # [cm**3]           Catalyst bed volume
    reformer.eta          = 0.9      # [-]               Efficiency

    return reformer

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()