## @ingroup Library-Energy-Methods-Thermal_Management-Common-Batteries
# RCAIDE/Library/Methods/Energy/Thermal_Management/Common/design_cross_flow_heat_exchanger.py


# Created:  Apr 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core                            import Units, Data   
from RCAIDE.Library.Methods.Energy.Thermal_Management.Common.Heat_Exchanger_Systems.Cross_Flow_Heat_Exchanger.cross_flow_heat_exchanger_sizing_setup import cross_flow_heat_exchanger_sizing_setup 
from RCAIDE.Library.Methods.Energy.Thermal_Management.Common.Heat_Exchanger_Systems.Cross_Flow_Heat_Exchanger.cross_flow_heat_exchanger_geometry_setup import cross_flow_heat_exchanger_geometry_setup
from RCAIDE.Framework.Optimization.Common             import Nexus
from RCAIDE.Framework.Optimization.Packages.scipy     import scipy_setup

# Python package imports   
import numpy as np  
import time 

# ----------------------------------------------------------------------
#  Rotor Design
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries
def design_cross_flow_heat_exchanger(HEX,HAS,battery, single_side_contact=True, dry_mass=True,
                                       solver_name= 'SLSQP',iterations = 200,solver_sense_step = 1E-2,
                                       solver_tolerance = 1E-1,print_iterations = False):
    
    """ Optimizes heat exchanger geometric properties input parameters to minimize either design power and mass. 
        This scrip adopts RCAIDE's native optimization style where the objective function is expressed 
        as a sizing function, considering both power and mass.
          
          Inputs: 
          HAS.
              Length, Height and width of the Heat Exchanger System 
             
          Outputs:
                 Length, Height, and Width of the Heat Exchanger System
                 Mass of Heat Exchanger System
                 Power Consumed by Heat Exchanger System 
                 
          Assumptions: 
             The wavy channel extracts from the battery pack considering it to be a lumped mass.  
        
          Source:
            Zhao, C., Clarke, M., Kellermann H., Verstraete D., “Design of a Liquid Cooling System for Lithium-Ion Battery Packs for eVTOL Aircraft" 
    """    
    
    
    # start optimization 
    ti                   = time.time()  
    optimization_problem = crossflow_heat_exchanger_design_problem_setup(HEX,HAS,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  
    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('HEX sizing optimization Simulation Time: ' + str(elapsed_time) + ' mins')    
 
    HEX_opt = optimization_problem.hex_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_exchanger_system 
    HEX.design_air_inlet_pressure     = output[0]
    HEX.design_coolant_inlet_pressure = output[1]
    HEX.design_air_mass_flow_rate     = output[2]
    HEX.design_coolant_mass_flow_rate = output[3]
    HEX.stack_length                  = HEX_opt.stack_length
    HEX.stack_width                   = HEX_opt.stack_width
    HEX.stack_height                  = HEX_opt.stack_height
    HEX.design_air_frontal_area       = HEX_opt.air_frontal_area
    HEX.design_air_pressure_diff      = HEX_opt.pressure_diff_air   
    return HEX

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def crossflow_heat_exchanger_design_problem_setup(HEX,HAS,print_iterations): 
    
    nexus                        = Nexus()
    problem                      = Data()
    nexus.optimization_problem   = problem    
    
    
    # ---------------------------------------------------------------------------------------------------------- 
    # Design Variables 
    # ----------------------------------------------------------------------------------------------------------       
    inputs = []   
    #               variable   initial   lower limit   upper limit     scaling       units 
    inputs.append([ 'p_c_1'   ,   200e3     ,  200e3     , 200e3+1       , 1         ,  1*Units.less]) 
    inputs.append([ 'p_h_1'   ,   160e3     ,  160e3     , 160e3+1       , 1         ,  1*Units.less]) 
    inputs.append([ 'm_dot_c' ,   1         ,  0.1       , 2.1           , 1.0       ,  1*Units.less])  
    inputs.append([ 'm_dot_h' ,   0.1       ,  0.1       , 0.5           , 1.0       ,  1*Units.less])  
   
        
    problem.inputs = np.array(inputs,dtype=object)   

    # ----------------------------------------------------------------------------------------------------------
    # Objective
    # ---------------------------------------------------------------------------------------------------------- 
    problem.objective = np.array([  
                                 [  'P_hex'  ,  10000   ,    1*Units.less] 
    ],dtype=object)
            

    # ----------------------------------------------------------------------------------------------------------
    # Constraints
    # ----------------------------------------------------------------------------------------------------------  
    constraints = []      
    constraints.append([ 'L'         ,  '<'  ,  2.0 ,   1.0   , 1*Units.less])
    constraints.append([ 'W'         ,  '<'  ,  2.0 ,   1.0   , 1*Units.less])  
    constraints.append([ 'H'         ,  '<'  ,  2.0 ,   1.0   , 1*Units.less]) 
    constraints.append([ 'L'         ,  '>'  ,  0.1 ,   1.0   , 1*Units.less])
    constraints.append([ 'W'         ,  '>'  ,  0.1 ,   1.0   , 1*Units.less])  
    constraints.append([ 'H'         ,  '>'  ,  0.1 ,   1.0   , 1*Units.less])     
    problem.constraints =  np.array(constraints,dtype=object)                
    
    # -------------------------------------------------------------------
    #  Aliases
    # ------------------------------------------------------------------- 
    aliases = [] 
    btms = 'hex_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_exchanger_system'  
    aliases.append([ 'm_dot_c'     , btms + '.air_flow_rate' ]) 
    aliases.append([ 'm_dot_c'     , btms + '.coolant_flow_rate' ]) 
    aliases.append([ 'p_c_1'       , btms + '.air_inlet_pressure' ])       
    aliases.append([ 'p_h_1'       , btms + '.coolant_inlet_pressure' ])   
    aliases.append([ 'L'           , 'summary.stack_length' ])     
    aliases.append([ 'W'           , 'summary.stack_width' ])   
    aliases.append([ 'H'           , 'summary.stack_height' ])        
    aliases.append([ 'P_hex'       , 'summary.mass_power_objective' ])   
    problem.aliases = aliases
    
    # -------------------------------------------------------------------
    #  Vehicles
    # ------------------------------------------------------------------- 
    nexus.hex_configurations = cross_flow_heat_exchanger_geometry_setup(HEX) # removed HAS as they are decoupled SAI 

    # -------------------------------------------------------------------
    #  Analyses
    # -------------------------------------------------------------------
    nexus.analyses = None 
    
    # -------------------------------------------------------------------
    #  Missions
    # -------------------------------------------------------------------
    nexus.missions = None
    
    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
    nexus.print_iterations  = print_iterations 
    nexus.procedure         = cross_flow_heat_exchanger_sizing_setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary         = Data()     
         
    return nexus   