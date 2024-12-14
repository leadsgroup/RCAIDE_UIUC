# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/append_electric_rotor_residual_and_unknown.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports   
from RCAIDE.Library.Components.Propulsors.Converters.Propeller   import Propeller 
from RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor  import Lift_Rotor 
from RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor  import Prop_Rotor 

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_electric_rotor_residual_and_unknown
# ----------------------------------------------------------------------------------------------------------------------  
def append_electric_rotor_residual_and_unknown(propulsor,segment):
    '''
    
    appends the torque matching residual and unknown
    '''
    
    ones_row    = segment.state.ones_row
    rotor   = propulsor.rotor  
    if type(rotor) == Propeller:
        cp_init  = float(rotor.cruise.design_power_coefficient)
    elif (type(rotor) == Lift_Rotor) or (type(rotor) == Prop_Rotor):
        cp_init  = float(rotor.hover.design_power_coefficient)    
    segment.state.unknowns[ propulsor.tag + '_rotor_cp']                    = cp_init * ones_row(1)  
    segment.state.residuals.network[propulsor.tag +'_rotor_motor_torque'] = 0. * ones_row(1)
    
    return 