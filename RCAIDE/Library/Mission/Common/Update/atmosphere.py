# RCAIDE/Library/Mission/Common/Update/atmosphere.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Atmosphere
# ----------------------------------------------------------------------------------------------------------------------
def atmosphere(segment):
    """
    Computes atmospheric properties at current altitude

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function evaluates the atmospheric model to obtain properties
    like pressure, temperature, density etc. at the current altitude.

    **Required Segment Components**

    segment:
        state.conditions:
            freestream:
                - altitude : array
                    Vehicle altitude [m]
        analyses.atmosphere : Model
            Atmospheric model
        temperature_deviation : float
            Temperature offset from standard day [K]

    **Major Assumptions**
    * Valid atmospheric model
    * Hydrostatic equilibrium
    * Well-mixed atmosphere
    * Ideal gas behavior

    Returns
    -------
    None
        Updates segment conditions directly with:
        - conditions.freestream:
            - pressure [Pa]
            - temperature [K]
            - density [kg/m³]
            - speed_of_sound [m/s]
            - dynamic_viscosity [Pa·s]
            - kinematic_viscosity [m²/s]
            - thermal_conductivity [W/(m·K)]
            - prandtl_number [-]

    
    """
    
    # unpack
    conditions            = segment.state.conditions
    h                     = conditions.freestream.altitude
    temperature_deviation = segment.temperature_deviation
    atmosphere            = segment.analyses.atmosphere
    
    # compute
    atmosphere_data = atmosphere.compute_values(h,temperature_deviation)
    
    # pack
    conditions.freestream.pressure               = atmosphere_data.pressure
    conditions.freestream.temperature            = atmosphere_data.temperature
    conditions.freestream.thermal_conductivity   = atmosphere_data.thermal_conductivity
    conditions.freestream.density                = atmosphere_data.density
    conditions.freestream.speed_of_sound         = atmosphere_data.speed_of_sound
    conditions.freestream.dynamic_viscosity      = atmosphere_data.dynamic_viscosity
    conditions.freestream.kinematic_viscosity    = atmosphere_data.kinematic_viscosity
    conditions.freestream.prandtl_number         = atmosphere_data.prandtl_number
    
    return
     