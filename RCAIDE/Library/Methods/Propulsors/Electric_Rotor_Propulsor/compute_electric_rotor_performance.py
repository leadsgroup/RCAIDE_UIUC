# RCAIDE/Methods/Energy/Propulsors/Electric_Rotor_Propulsor/compute_electric_rotor_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   
from RCAIDE.Library.Methods.Propulsors.Modulators.Electronic_Speed_Controller.compute_esc_performance  import * 
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor.compute_motor_performance                   import *
from RCAIDE.Library.Methods.Propulsors.Converters.Rotor.compute_rotor_performance                      import * 


# pacakge imports  
import numpy as np 
from copy import deepcopy

# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_rotor_performance
# ----------------------------------------------------------------------------------------------------------------------  
def compute_electric_rotor_performance(propulsor,state,voltage,center_of_gravity= [[0.0, 0.0,0.0]]):
    """
    Computes the performance characteristics of an electric rotor propulsion system by evaluating 
    the electronic speed controller (ESC), DC motor, and rotor in sequence.

    Parameters
    ----------
    propulsor : RCAIDE.Library.Components.Propulsors.Electric_Rotor
        The electric rotor propulsion system
            - tag : str
                Identifier for the propulsor
            - motor : Component
                DC motor component
            - rotor : Component
                Rotor component
            - electronic_speed_controller : Component
                ESC component
    state : RCAIDE.Framework.Mission.Common.State
        Contains flight conditions and operating state
            - conditions : Conditions
                Flight condition parameters including energy and throttle settings
    voltage : float
        System input voltage [V]
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
        Total electrical power consumption [W]
    stored_results_flag : bool
        Indicator that results have been stored
    stored_propulsor_tag : str
        Identifier of the propulsor with stored results

    Notes
    -----
    The function performs a sequential computation through the propulsion system:
        1. Unpacks conditions and propulsor components
        2. ESC modulates input voltage based on throttle setting
        3. Motor converts electrical power to mechanical rotation
        4. Rotor converts mechanical rotation to thrust
        5. System performance metrics are computed

    **Major Assumptions**
        * Components are connected in series: ESC → Motor → Rotor
        * Power losses occur at each conversion stage
        * Moments from motor rotation are not included (noted as future work)
        * Perfect mechanical coupling between motor and rotor

    **Definitions**

    'Throttle'
        Control input ranging from 0 to 1 that modulates power output

    'Stored Results'
        Performance data saved for reuse with identical propulsors
    """
    conditions                 = state.conditions    
    electric_rotor_conditions  = conditions.energy[propulsor.tag] 
    motor                      = propulsor.motor 
    rotor                      = propulsor.rotor 
    esc                        = propulsor.electronic_speed_controller  
    esc_conditions             = electric_rotor_conditions[esc.tag]
    motor_conditions           = electric_rotor_conditions[motor.tag]
    rotor_conditions           = electric_rotor_conditions[rotor.tag]
    eta                        = conditions.energy[propulsor.tag].throttle
    
    esc_conditions.inputs.voltage   = voltage
    esc_conditions.throttle         = eta 
    compute_voltage_out_from_throttle(esc,esc_conditions,conditions)

    # Assign conditions to the rotor
    motor_conditions.voltage                   = esc_conditions.outputs.voltage 
    compute_RPM_and_torque_from_power_coefficent_and_voltage(motor,motor_conditions,conditions)
    
    # Spin the rotor 
    rotor_conditions.omega           = motor_conditions.omega
    rotor_conditions.throttle        = esc_conditions.throttle 
    compute_rotor_performance(propulsor,state,center_of_gravity)  

    # Run the motor for current
    compute_current_from_RPM_and_voltage(motor,motor_conditions,conditions)
    
    # Detemine esc current 
    esc_conditions.outputs.current = motor_conditions.current
    compute_current_in_from_throttle(esc,esc_conditions,conditions)  
    esc_conditions.current   = esc_conditions.inputs.current  
    esc_conditions.power     = esc_conditions.inputs.power
    
    stored_results_flag     = True
    stored_propulsor_tag    = propulsor.tag 
    
    # compute total forces and moments from propulsor (future work would be to add moments from motors)
    electric_rotor_conditions.thrust      = conditions.energy[propulsor.tag][rotor.tag].thrust 
    electric_rotor_conditions.moment      = conditions.energy[propulsor.tag][rotor.tag].moment 
    
    T  = conditions.energy[propulsor.tag][rotor.tag].thrust 
    M  = conditions.energy[propulsor.tag][rotor.tag].moment 
    P  = conditions.energy[propulsor.tag][esc.tag].power 
    
    return T,M,P, stored_results_flag,stored_propulsor_tag 
                
def reuse_stored_electric_rotor_data(propulsor,state,network,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    """
    Reuses previously computed performance data for identical electric rotor propulsors to avoid 
    redundant calculations. Copies stored energy conditions and recalculates moments based on 
    the propulsor's position relative to the center of gravity.

    Parameters
    ----------
    propulsor : RCAIDE.Core.Systems.Propulsors
        The electric rotor propulsion system to copy data to
            - tag : str
                Identifier for the propulsor
            - motor : Component
                DC motor component
            - rotor : Component
                Rotor component
            - electronic_speed_controller : Component
                ESC component
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
        Total electrical power consumption [W]

    Notes
    -----
    The function performs these operations:
        1. Copies stored energy conditions from source to target propulsor
        2. Extracts thrust and power values
        3. Recalculates moments based on new propulsor position
        4. Updates propulsor conditions with new values

    **Major Assumptions**
        * Source and target propulsors are identical in configuration
        * Only position relative to CG affects moment calculations
        * Energy conditions can be directly copied between propulsors
        * Thrust magnitude and direction remain unchanged

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
    """
    conditions                 = state.conditions 
    motor                      = propulsor.motor 
    rotor                      = propulsor.rotor 
    esc                        = propulsor.electronic_speed_controller  
    motor_0                    = network.propulsors[stored_propulsor_tag].motor 
    rotor_0                    = network.propulsors[stored_propulsor_tag].rotor 
    esc_0                      = network.propulsors[stored_propulsor_tag].electronic_speed_controller
    
    conditions.energy[propulsor.tag][motor.tag]        = deepcopy(conditions.energy[stored_propulsor_tag][motor_0.tag])
    conditions.energy[propulsor.tag][rotor.tag]        = deepcopy(conditions.energy[stored_propulsor_tag][rotor_0.tag])
    conditions.energy[propulsor.tag][esc.tag]          = deepcopy(conditions.energy[stored_propulsor_tag][esc_0.tag])
  
    thrust                  = conditions.energy[propulsor.tag][rotor.tag].thrust 
    power                   = conditions.energy[propulsor.tag][esc.tag].power 
    
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = rotor.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = rotor.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = rotor.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust)
    
    conditions.energy[propulsor.tag][rotor.tag].moment = moment  
    conditions.energy[propulsor.tag].thrust            = thrust   
    conditions.energy[propulsor.tag].moment            = moment  
    
    return thrust,moment,power