# RCAIDE/Library/Methods/Powertrain/Converters/Generator/compute_generator_performance.py

# 
# Created: Feb 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_omega_and_Q_from_Cp_and_V
# ----------------------------------------------------------------------------------------------------------------------    
def compute_generator_performance(generator,generator_conditions,conditions):
    """
    Computes generator performance characteristics including electrical, mechanical and thermal parameters.

    Parameters
    ----------
    generator : Converter
        Generator component for which performance is being computed
    generator_conditions : Conditions
        Container for generator operating conditions
    conditions : Conditions 
        Mission segment conditions containing freestream properties

    Returns
    -------
    None
        Updates generator_conditions in-place with computed performance parameters

    Notes
    -----
    This function handles both PMSM and DC generator types with different computation approaches:
     
    - Uses speed-torque relationships
    - Accounts for gearbox effects
    - Computes electrical parameters (current, voltage)
    - Determines overall efficiency

    **Major Assumptions**
        * Steady state operation
        * Uniform temperature distribution
        * No magnetic saturation effects
        * Linear speed-torque characteristics for DC generators
        * Constant material properties

    See Also
    --------
    RCAIDE.Library.Components.Powertrain.Converters.DC_generator
    RCAIDE.Library.Components.Powertrain.Converters.PMSM_generator
    """           
    # Unpack  
    Res   = generator.resistance 

    # Unpack
    G     = generator.gearbox_ratio
    Kv    = generator.speed_constant
    Res   = generator.resistance
    v     = generator_conditions.voltage 
    omeg  = generator_conditions.omega*G
    power = generator_conditions.shaft_powwer
    etaG  = generator.gearbox_efficiency
    exp_i = generator.expected_current
    io    = generator.no_load_current + exp_i*(1-etaG)
    
    i=(v-omeg/Kv)/Res 
    i[i < 0.0] = 0.0
 
    etam=(1-io/i)*(1-i*Res/v)
    
    Q     = power / omeg 

    v     = generator_conditions.voltage
    
    generator_conditions.torque     = Q   
    generator_conditions.current    = i 
    generator_conditions.power      = i *v 
    generator_conditions.efficiency = etam 
 
    return