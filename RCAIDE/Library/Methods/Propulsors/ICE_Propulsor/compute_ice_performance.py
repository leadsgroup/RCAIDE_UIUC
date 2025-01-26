# RCAIDE/Methods/Energy/Propulsors/ICE_Propulsor/compute_ice_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Methods.Propulsors.Converters.Engine import compute_power_from_throttle
from RCAIDE.Library.Methods.Propulsors.Converters.Rotor.compute_rotor_performance import  compute_rotor_performance

# pacakge imports  
from copy import deepcopy
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
# compute_ice_performance
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_ice_performance(propulsor,state,center_of_gravity= [[0.0, 0.0,0.0]]):
    """
    Computes the performance characteristics of an Internal Combustion Engine (ICE) propulsion 
    system by evaluating the engine and propeller in sequence. Handles throttle settings, 
    power generation, and thrust production.

    Parameters
    ----------
    propulsor : RCAIDE.Library.Components.Propulsors.ICE_Propeller
        The ICE propulsion system
            - tag : str
                Identifier for the propulsor
            - engine : Component
                Internal combustion engine component
            - propeller : Component
                Propeller component
    state : RCAIDE.Framework.Mission.Common.State
        Contains flight conditions and operating state
            - conditions : Conditions
                Flight condition parameters including energy settings
                    - energy : dict
                        Contains propulsor-specific conditions
                            - throttle : float
                                Engine power setting
                            - rpm : float
                                Engine rotational speed
    center_of_gravity : list, optional
        Aircraft center of gravity coordinates [[x, y, z]] [m]
        Default is [[0.0, 0.0, 0.0]]

    Returns
    -------
    T : array_like
        Thrust force vector [N]
    M : array_like
        Moment vector [N-m]
    P : float
        Power output [W]
    stored_results_flag : bool
        Indicator that results have been stored
    stored_propulsor_tag : str
        Identifier of the propulsor with stored results

    Notes
    -----
    The function performs a sequential computation through the propulsion system:
        1. Conditions and propulsor data is unpacked
        2. Engine throttle setting is processed
        3. Power is computed from throttle
        4. Propeller performance is evaluated
        5. System forces and moments are calculated

    **Major Assumptions**
        * Direct mechanical coupling between engine and propeller
        * Moments from engine rotation are not included (noted as future work)

    **Definitions**

    'Throttle'
        Control input ranging from 0 to 1 that modulates engine power output
        
    'Stored Results'
        Performance data saved for reuse with identical propulsors
    """
    conditions              = state.conditions  
    ice_conditions          = conditions.energy[propulsor.tag]
    engine                  = propulsor.engine 
    propeller               = propulsor.propeller
    eta                     = ice_conditions.throttle
    engine_conditions       = ice_conditions[engine.tag]
    RPM                     = engine_conditions.rpm

    # Throttle the engine
    engine_conditions.speed           = RPM * Units.rpm
    engine_conditions.throttle        = eta 
    compute_power_from_throttle(engine,engine_conditions,conditions)        
     
    # Run the propeller to get the power
    propeller_conditions                = ice_conditions[propeller.tag]
    propeller_conditions.omega          = RPM * Units.rpm 
    propeller_conditions.throttle       = engine_conditions.throttle
    compute_rotor_performance(propulsor,state,center_of_gravity)
    
    # Create the outputs
    ice_conditions.fuel_flow_rate            = engine_conditions.fuel_flow_rate  
    stored_results_flag                      = True
    stored_propulsor_tag                     = propulsor.tag 


    # compute total forces and moments from propulsor (future work would be to add moments from motors)
    ice_conditions.thrust      = conditions.energy[propulsor.tag][propeller.tag].thrust 
    ice_conditions.moment      = conditions.energy[propulsor.tag][propeller.tag].moment
    ice_conditions.power       = conditions.energy[propulsor.tag][propeller.tag].power 
    
    T  = conditions.energy[propulsor.tag][propeller.tag].thrust  
    M  = conditions.energy[propulsor.tag][propeller.tag].moment 
    P  = conditions.energy[propulsor.tag][propeller.tag].power 
    
    return T,M,P,stored_results_flag,stored_propulsor_tag 
    
    
    
def reuse_stored_ice_data(propulsor,state,network,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    """
    Reuses previously computed performance data for identical ICE propulsors to avoid 
    redundant calculations. Copies stored energy conditions and recalculates moments based on 
    the propulsor's position relative to the center of gravity.

    Parameters
    ----------
    propulsor : RCAIDE.Core.Systems.Propulsors
        The ICE propulsion system to copy data to
            - tag : str
                Identifier for the propulsor
            - engine : Component
                Internal combustion engine component
            - propeller : Component
                Propeller component with origin coordinates
    state : RCAIDE.Core.State
        Contains flight conditions and operating state
    network : RCAIDE.Core.Systems.Networks
        The propulsion network containing stored results
            - propulsors : dict
                Dictionary of propulsors with stored results
    stored_propulsor_tag : str
        Identifier of the propulsor containing the source data
    center_of_gravity : list, optional
        Aircraft center of gravity coordinates [[x, y, z]] [m]
        Default is [[0.0, 0.0, 0.0]]

    Returns
    -------
    thrust : array_like
        Thrust force vector [N]
    moment : array_like
        Moment vector [N-m]
    power : float
        Power output [W]

    Notes
    -----
    The function performs these operations:
        1. Copies stored energy conditions from source to target propulsor
        2. Extracts thrust and power values
        3. Recalculates moments based on new propulsor position
        4. Updates propulsor conditions with new values

    **Major Assumptions**
        * Source and target propulsors are identical in configuration, thrust, conditions, and fuel flow characteristics
        * Only position relative to CG affects moment calculations

    **Theory**
    Moment calculation follows the cross product:

    .. math::
        \\vec{M} = \\vec{r} \\times \\vec{F}

    where:
        - M is the moment vector
        - r is the position vector from CG to propulsor
        - F is the thrust force vector

    **Definitions**

    'Stored Results'
        Performance data previously computed and saved for an identical propulsor
        
    'Moment Arm'
        Vector from center of gravity to propulsor location
        
    'Propulsor Origin'
        Reference point for propulsor location and moment calculations
    """
    conditions   = state.conditions 
    engine       = propulsor.engine
    propeller    = propulsor.propeller 
    engine_0     = network.propulsors[stored_propulsor_tag].engine
    propeller_0  = network.propulsors[stored_propulsor_tag].propeller  
    
    conditions.energy[propulsor.tag][engine.tag]        = deepcopy(conditions.energy[stored_propulsor_tag][engine_0.tag])
    conditions.energy[propulsor.tag][propeller.tag]     = deepcopy(conditions.energy[stored_propulsor_tag][propeller_0.tag])
  
    thrust                  = conditions.energy[propulsor.tag][propeller.tag].thrust 
    power                   = conditions.energy[propulsor.tag][propeller.tag].power 
    
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = propeller.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = propeller.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust)
    
    conditions.energy[propulsor.tag][propeller.tag].moment = moment  
    conditions.energy[propulsor.tag].thrust            = thrust   
    conditions.energy[propulsor.tag].moment            = moment  
    conditions.energy[propulsor.tag].power             = power
 
    return thrust,moment,power 

            
               