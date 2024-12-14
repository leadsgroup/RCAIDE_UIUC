# RCAIDE/Library/Components/Propulsors/Converters/Combustor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor.append_combustor_conditions import  append_combustor_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Combustor
# ---------------------------------------------------------------------------------------------------------------------- 
class Combustor(Component):
    """This is a combustor compoment class.
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        None 
        """         
        
        self.tag                               = 'Combustor' 
        self.alphac                            = 0.0
        self.turbine_inlet_temperature         = 1500
        self.area_ratio                        = 1.0
        self.axial_fuel_velocity_ratio         = 0.0
        self.fuel_velocity_ratio               = 0.0
        self.burner_drag_coefficient           = 0.0
        self.absolute_sensible_enthalpy        = 0.0 
        self.diameter                          = 0.2
        self.length                            = 0.3
        self.fuel_equivalency_ratio            = 0.3 
        self.number_of_combustors              = 30 
                                               
        self.f_air_PZ                          = 0.18                                                  # [-]       Fraction of total air present in the combustor that enters the Primary Zone         
        self.FAR_st                            = 0.068                                                 # [-]       Stoichiometric Fuel to Air ratio
        self.N_comb                            = 10                                                    # [-]       Number of can-annular combustors
        self.N_PZ                              = 8                                                     # [-]       Number of PSR (EVEN, must match the number of PSR below)
        self.A_PZ                              = 0.15                                                  # [m**2]    Primary Zone cross-sectional area     
        self.L_PZ                              = 0.0153                                                # [m]       Primary Zone length  
        self.N_SZ                              = 3                                                     # [-]       Number of dilution air inlets        
        self.A_SZ                              = 0.15                                                  # [m**2]    Secondary Zone cross-sectional area
        self.L_SZ                              = 0.075                                                 # [m]       Secondary Zone length  
        self.phi_SZ                            = 0.2                                                   # [-]       Equivalence Ratio for PFR    phi_PZ_des              = 0.6                                                   # [-]       Primary Zone Design Equivalence Ratio
        self.S_PZ                              = 0.6                                                   # [-]       Mixing parameter, used to define the Equivalence Ratio standard deviation  
        self.F_SC                              = 0.425                                                 # [-]       Fuel scaler
        self.number_of_assigned_PSR_1st_mixers = 2                                                     # [-]       Number of assigned PSRs to each mixer in the first row of mixers (CRN network model)
        self.number_of_assigned_PSR_2nd_mixers = 2                                                     # [-]       Number of assigned mixers to each mixer in the second row of mixers (CRN network model)
    
    def append_operating_conditions(self,segment,propulsor):
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_combustor_conditions(self,segment,propulsor_conditions)
        return
