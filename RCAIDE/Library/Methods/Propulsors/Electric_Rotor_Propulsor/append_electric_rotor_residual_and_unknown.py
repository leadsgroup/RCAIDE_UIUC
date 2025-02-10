# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/append_electric_rotor_residual_and_unknown.py
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Library.Components.Propulsors.Converters.Propeller   import Propeller 
from RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor  import Lift_Rotor 
from RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor  import Prop_Rotor 

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_electric_rotor_residual_and_unknown
# ----------------------------------------------------------------------------------------------------------------------  
def append_electric_rotor_residual_and_unknown(propulsor,segment):
    """
    Initializes the power coefficient unknown and torque matching residual for an electric rotor 
    propulsion system. The initial power coefficient is set based on the rotor type (propeller, 
    lift rotor, or prop rotor).

    Parameters
    ----------
    propulsor : RCAIDE.Library.Components.Propulsors.Electric_Rotor
        The electric rotor propulsion system
            - tag : str
                Identifier for the propulsor
            - rotor : Component
                The rotor component (Propeller, Lift_Rotor, or Prop_Rotor)
    segment : RCAIDE.Framework.Mission.Segments.Segment
        The mission segment being analyzed
            - state : State
                Contains solver unknowns and residuals

    Returns
    -------
    None

    Notes
    -----
    The function sets up two key variables for the solver:
        1. Power coefficient (Cp) unknown - initialized from design conditions
        2. Motor-rotor torque matching residual - initialized to zero

    **Definitions**

    'Power Coefficient'
        Non-dimensional parameter representing the power absorbed by the rotor
    """
    
    ones_row    = segment.state.ones_row
    rotor       = propulsor.rotor  
    motor       = propulsor.motor
    if type(rotor) == Propeller:
        cp_init  = float(rotor.cruise.design_power_coefficient)
    elif (type(rotor) == Lift_Rotor) or (type(rotor) == Prop_Rotor):
        cp_init  = float(rotor.hover.design_power_coefficient)
    else:
        cp_init  = 0.5
         
    if (type(motor) == RCAIDE.Library.Components.Propulsors.Converters.PMSM_Motor):
        segment.state.unknowns[ propulsor.tag + '_current']                    = 50 * ones_row(1)  
    else:
        segment.state.unknowns[ propulsor.tag + '_rotor_cp']                    = cp_init * ones_row(1)  
    segment.state.residuals.network[propulsor.tag +'_rotor_motor_torque'] = 0. * ones_row(1)
    
    return 