# RCAIDE/Library/Methods/Propulsors/Common/compute_static_sea_level_performance.py
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE  
from RCAIDE.Framework.Mission.Common      import  Conditions

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Design Turbofan
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_static_sea_level_performance(propulsor):
    """
    Computes the static sea level performance characteristics of a propulsion system.
    
    Parameters
    ----------
    propulsor : RCAIDE.Library.Components.Propulsors.Propulsor
        The propulsion system object to analyze
            - working_fluid : Gas
                Working fluid properties for the propulsion system
            - tag : str
                Unique identifier for the propulsor
    
    Returns
    -------
    None
    
    Notes
    -----
    This function creates a simulated sea level static test condition and computes
    the propulsor performance. It sets up atmospheric conditions at sea level
    with near-zero velocity (Mach 0.01) to approximate static conditions. It then 
    appends the propulsor operating conditions to the segment state.
  
    
    **Major Assumptions**
        * Earth standard atmosphere (US 1976)
        * Static conditions approximated with Mach 0.01
        * Full throttle (1.0) operation
        * Sea level gravity
    
    **Theory**
    
    Static sea level performance is computed by simulating the propulsor
    at sea level conditions with:
    
    See Also
    --------
    RCAIDE.Framework.Mission.Common.Results
    RCAIDE.Library.Attributes.Planets.Earth
    RCAIDE.Library.Components.Propulsors
    """  
    # Step 28: Static Sea Level Thrust  
    planet                                            = RCAIDE.Library.Attributes.Planets.Earth()
    atmosphere_sls                                    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data                                         = atmosphere_sls.compute_values(0.0,0.0)
                                                      
    p                                                 = atmo_data.pressure          
    T                                                 = atmo_data.temperature       
    rho                                               = atmo_data.density          
    a                                                 = atmo_data.speed_of_sound    
    mu                                                = atmo_data.dynamic_viscosity     
                                                      
    conditions                                        = RCAIDE.Framework.Mission.Common.Results() 
    conditions.freestream.altitude                    = np.atleast_1d(0)
    conditions.freestream.mach_number                 = np.atleast_1d(0.01)
    conditions.freestream.pressure                    = np.atleast_1d(p)
    conditions.freestream.temperature                 = np.atleast_1d(T)
    conditions.freestream.density                     = np.atleast_1d(rho)
    conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
    conditions.freestream.gravity                     = np.atleast_2d(planet.sea_level_gravity)
    conditions.freestream.isentropic_expansion_factor = np.atleast_1d(propulsor.working_fluid.compute_gamma(T,p))
    conditions.freestream.Cp                          = np.atleast_1d(propulsor.working_fluid.compute_cp(T,p))
    conditions.freestream.R                           = np.atleast_1d(propulsor.working_fluid.gas_specific_constant)
    conditions.freestream.speed_of_sound              = np.atleast_1d(a)
    conditions.freestream.velocity                    = np.atleast_1d(a*0.01)   

    # setup conditions   
    segment                                           = RCAIDE.Framework.Mission.Segments.Segment()  
    segment.state.conditions                          = conditions      
    propulsor.append_operating_conditions(segment) 
    for tag, item in  propulsor.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,propulsor) 
    
    # set throttle
    segment.state.conditions.energy[propulsor.tag].throttle[:,0] = 1.0  
    sls_T,sls_M,sls_P,_,_                             = propulsor.compute_performance(segment.state)
        
    propulsor.sealevel_static_thrust                  = sls_T[0][0]
    return 