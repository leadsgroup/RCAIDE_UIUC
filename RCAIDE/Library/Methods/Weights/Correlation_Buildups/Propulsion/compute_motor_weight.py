# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/compute_motor_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE  
 
# ----------------------------------------------------------------------------------------------------------------------
#  Motor Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_motor_weight(motor):
    """
    Calculates electric motor weight using empirical correlation based on motor torque.

    Parameters
    ----------
    motor : RCAIDE.Component()
        Motor component with the following properties:
            - design_torque : float
                Maximum safe operating torque [N-m]

    Returns
    -------
    mass : float
        Mass of the electric motor [kg]

    Notes
    -----
    This method uses a quadratic correlation to estimate electric motor mass
    based on the motor's design torque. The correlation is derived from 
    NASA electric motor data.

    **Major Assumptions**
        * Motor mass is primarily driven by torque requirements
        * Correlation valid for aerospace-grade electric motors
        * Quadratic relationship between torque and mass
        * Mass includes motor housing and essential components
        * Does not include power electronics or cooling systems

    **Theory**
    The motor mass is calculated using the following quadratic correlation:
    .. math::
        m_{motor} = -2 \\times 10^{-7}\\tau^2 + 0.0117\\tau + 34.124

    where:
        * :math:`\\tau` is the design torque in N-m
        * Mass is output directly in kilograms

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_jet_engine_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion.compute_piston_engine_weight
    """
    
    torque =  motor.design_torque
    mass  = -2E-7 * (torque ** 2) +  0.0117 * torque +  34.124
     
    return mass 