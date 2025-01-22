# RCAIDE/Library/Methods/Propulsors/Turbojet_Propulsor/size_core.py
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Propulsors.Turbojet_Propulsor import compute_thrust

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ---------------------------------------------------------------------------------------------------------------------- 
def size_core(turbojet,turbojet_conditions,conditions):
    """
    Sizes the core flow of a turbojet engine based on design thrust requirements and flight conditions.
    
    Parameters
    ----------
    turbojet : Turbojet
        Turbojet engine object containing design parameters
            - reference_temperature : float
                Reference temperature [K]
            - reference_pressure : float
                Reference pressure [Pa]
            - design_thrust : float
                Design thrust requirement [N]
            - SFC_adjustment : float
                Thrust specific fuel consumption adjustment factor [-]
    turbojet_conditions : Data
        Operating conditions for the turbojet
            - throttle : float
                Throttle setting [-]
            - total_temperature_reference : float
                Reference total temperature [K]
            - total_pressure_reference : float
                Reference total pressure [Pa]
    conditions : Data
        Flight conditions
            - freestream.speed_of_sound : float
                Freestream speed of sound [m/s]
    
    Returns
    -------
    None
        Updates turbojet object attributes in-place:
            - mass_flow_rate_design : float
                Design core mass flow rate [kg/s]
            - compressor_nondimensional_massflow : float
                Non-dimensional mass flow parameter [-]
            - TSFC : float
                Thrust specific fuel consumption [kg/(N*hr)]
    
    Notes
    -----
    This function determines the required core mass flow rate to achieve the design
    thrust using non-dimensional analysis and corrected flow parameters.
    
    **Major Assumptions**
        * Perfect gas behavior
        * Steady state operation
        * One-dimensional flow
        * Design point defines core sizing
    
    **Theory**
    The core sizing is based on non-dimensional thrust parameters and corrected flow:
    
    .. math::
        \\dot{m}_{core} = \\frac{F_{design}}{F_{sp} a_0 \\theta}
    
        \\dot{m}_{corr} = \\frac{\\dot{m}_{core}}{\\delta}\\sqrt{\\theta}
    
    where:
        - :math:`F_{design}` is the design thrust
        - :math:`F_{sp}` is the specific thrust
        - :math:`a_0` is the freestream speed of sound
        - :math:`\\theta = \\frac{T_t}{T_{ref}}` is the temperature correction
        - :math:`\\delta = \\frac{P_t}{P_{ref}}` is the pressure correction
        - :math:`\\dot{m}_{corr}` is the corrected mass flow
    
    References
    ----------
    [1] Mattingly, J. D., "Elements of Gas Turbine Propulsion", McGraw-Hill, 1996
    [2] Walsh, P. P., Fletcher, P., "Gas Turbine Performance", Blackwell Science, 2004
    
    See Also
    --------
    RCAIDE.Library.Methods.Propulsors.Turbojet_Propulsor.compute_thrust
    RCAIDE.Library.Methods.Propulsors.Turbojet_Propulsor.design_turbojet
    """            
    #unpack inputs
    a0                   = conditions.freestream.speed_of_sound
    throttle             = 1.0

    #unpack from turbojet 
    Tref                        = turbojet.reference_temperature
    Pref                        = turbojet.reference_pressure 

    total_temperature_reference = turbojet_conditions.total_temperature_reference  
    total_pressure_reference    = turbojet_conditions.total_pressure_reference 

    #compute nondimensional thrust
    turbojet_conditions.throttle = 1.0
    compute_thrust(turbojet,turbojet_conditions,conditions)

    #unpack results 
    Fsp                         = turbojet_conditions.non_dimensional_thrust

    #compute dimensional mass flow rates
    mdot_core                   = turbojet.design_thrust/(Fsp*a0*throttle)  
    mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))

    #pack outputs
    turbojet.mass_flow_rate_design               = mdot_core
    turbojet.compressor_nondimensional_massflow  = mdhc

    return    
