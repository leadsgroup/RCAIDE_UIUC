# RCAIDE/Compoments/Propulsors/Converters/Reformer.py
# 
# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core              import Data
from RCAIDE.Library.Components          import Component 
from RCAIDE.Library.Methods.Propulsors.Converters.Ducted_Fan.append_ducted_fan_conditions import  append_ducted_fan_conditions
import numpy as np
import scipy as sp
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Reformer(Component):
    """
 
    """
    
    def __defaults__(self):
        """ 
        """      
        
        self.tag   = 'reformer'  
        # Jet-A parameters
        self.x_H          = 0.1348   # [-]               mass fraction of hydrogen content in Jet-A
        self.x_C          = 0.8637   # [-]               mass fraction of carbon content in Jet-A
        
        # Reformate parameters
        self.y_H2         = 0.9      # [mol]             mole fraction of hydrogen content in reformate
        self.y_CO         = 0.3      # [mol]             mole fraxtion of carbon monoxide content in reformate
    
        # Reformer parameters
        self.rho_F        = 0.813    # [g/cm**3]         Density of Jet-A
        self.rho_S        = 1        # [g/cm**3]         Density of water
        self.rho_A        = 0.001293 # [g/cm**3]         Density of air
        self.MW_F         = 160      # [g/g-mol]         Average molecular weight of Jet-A    
        self.MW_S         = 18.01    # [g/g-mol]         Average molecular weight of steam
        self.MW_C         = 12.01    # [g/g-mol]         Average molecular weight of carbon
        self.MW_H2        = 2.016    # [g/g-mol]         Average molecular weight of hydrogen
        self.A_F_st_Jet_A = 14.62    # [lb_Air/lb_Jet_A] Stoichiometric air-to-fuel mass ratio 
        self.theta        = 0.074    # [sec**-1]         Contact time
        self.LHV_F        = 43.435   # [kJ/g-mol]        Lower heating value of Jet-A
        self.LHV_H2       = 240.2    # [kJ/g-mol]        Lower heating value of Hydrogen
        self.LHV_CO       = 283.1    # [kJ/g-mol]        Lower heating value of Carbon Monoxide
        self.V_cat        = 9.653    # [cm**3]           Catalyst bed volume
        self.eta          = 0.9