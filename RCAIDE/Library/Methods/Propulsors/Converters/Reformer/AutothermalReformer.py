# RCAIDE/Library/Methods/Propulsors/Converters/DC_Motor/compute_PMSM_motor_performance.py

# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_PMSM_motor_performance
# ----------------------------------------------------------------------------------------------------------------------    
def AutothermalReformer(input):

    # Molar Feed Rates
    F_F = input['Q_F'] * input['rho_F'] / input['MW_F']                # [g-mol/hr] molar flow rate of Jet-A
    F_S = input['Q_S'] * input['rho_S'] / input['MW_S']                # [g-mol/hr] molar flow rate of steam
    F_A = (input['Q_A'] * 60) / 22414                                  # [g-mol/hr] molar flow rate of air
    F_C = input['Q_F'] * input['rho_F'] * input['x_C'] / input['MW_C'] # [g-mol/hr] molar flow rate of carbon

    # Effluent Gas Molar Flow Rate
    Q_R = (input['Q_F']/60) + (input['Q_S']/60)  + input['Q_A'] # [sccm] Reformer effluent gas feed rate
    F_R = Q_R * 60 / 22414                                  # [g-mol/hr] reformate effluent gas molar flow rate

    # Space Velocity
    GHSV = ((F_F + F_S + F_A) / input['V_cat']) * 22410 # [hr**-1] gas hourly space velocity
    LHSV = input['Q_F'] / input['V_cat']                # [hr**-1] liquid hourly space velocity

    # Steam to Carbon, Oxygen to Carbon and Equivalence Ratio 
    S_C = F_S / F_C                                                                                        # [mol_H20/mol_C] Steam-to-Carbon feed ratio
    O_C = 2 * 0.21 * F_A / F_C                                                                             # [mol_O/mol_C] Oxygen-to-Carbon feed ratio
    phi = input['A_F_st_Jet_A'] * (input['Q_F'] * input['rho_F']) / ((input['Q_A'] * 60) * input['rho_A']) # [-] Fuel to Air ratio

    # Reformer efficiency
    eta_ref = ((input['y_H2'] * input['LHV_H2'] + input['y_CO'] * input['LHV_CO']) * F_R / (input['Q_F'] * input['rho_F'] * input['LHV_F'])) * 100 # [-] Reformer efficiency

    # Hydrogen conversion efficiency
    X_H2 = ((input['y_H2'] * F_R)/ (((input['Q_F'] * input['rho_F'] * input['x_H'])/(input['MW_H2'])) + F_S)) * 100 # [-] Hydrogen conversion efficiency  

    return Q_R, eta_ref, X_H2, GHSV, LHSV, S_C, O_C, phi