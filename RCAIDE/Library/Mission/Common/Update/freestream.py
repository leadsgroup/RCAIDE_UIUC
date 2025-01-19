# RCAIDE/Library/Mission/Common/Update/freestream.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import numpy as np 
    
# ----------------------------------------------------------------------------------------------------------------------
#  Update Freestream
# ----------------------------------------------------------------------------------------------------------------------
def freestream(segment):
    """
    Updates freestream flow conditions

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function computes freestream conditions like velocity magnitude,
    Mach number, Reynolds number, and dynamic pressure from vehicle state
    and atmospheric properties.

    **Required Segment Components**

    segment.state.conditions:
        frames.inertial:
            - velocity_vector : array
                Vehicle velocity [m/s]
        freestream:
            - density : array
                Air density [kg/m³]
            - speed_of_sound : array
                Speed of sound [m/s]
            - dynamic_viscosity : array
                Air viscosity [Pa·s]

    **Major Assumptions**
    * Continuous flow
    * Perfect gas behavior
    * Valid atmospheric properties
    * Well-defined velocity state

    Returns
    -------
    None
        Updates segment conditions directly:
        - conditions.freestream:
            - velocity [m/s]
            - mach_number [-]
            - reynolds_number [1/m]
            - dynamic_pressure [Pa]

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """   
    
    # unpack
    conditions = segment.state.conditions
    V          = conditions.frames.inertial.velocity_vector
    rho        = conditions.freestream.density
    a          = conditions.freestream.speed_of_sound
    mu         = conditions.freestream.dynamic_viscosity

    # velocity magnitude
    Vmag2 = np.sum( V**2, axis=1)[:,None]  
    Vmag  = np.sqrt(Vmag2)

    # dynamic pressure
    q = 0.5 * rho * Vmag2 # Pa

    # Mach number
    M = Vmag / a

    # Reynolds number
    Re = rho * Vmag / mu  # per m

    # pack
    conditions.freestream.velocity         = Vmag
    conditions.freestream.mach_number      = M
    conditions.freestream.reynolds_number  = Re
    conditions.freestream.dynamic_pressure = q

    return

