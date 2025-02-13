# RCAIDE/Library/Methods/Powertrain/Converters/Generator/append_generator_conditions.py
# 
# Created:  Feb 2025, M. Guidotti

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_generator_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_generator_conditions(generator,segment,propulsor_conditions): 

    """
    Initializes generator operating conditions for a mission segment.

    Parameters
    ----------
    generator : Converter
        Generator component for which conditions are being initialized
    segment : Segment
        Mission segment containing the state conditions
    propulsor_conditions : Conditions
        Container for propulsor operating conditions

    Returns
    -------
    None
        Modifies propulsor_conditions in-place by adding generator-specific conditions

    Notes
    -----
    This function initializes arrays of zeros for key generator operating parameters during
    a mission segment. The conditions are stored in a nested structure under the generator's
    tag within propulsor_conditions.

    The following conditions are initialized:
        - torque: Generator output torque [N-m]
        - efficiency: Generator operating efficiency [-] 
        - current: Generator current draw [A]
        - voltage: Generator voltage [V]

    See Also
    --------
    RCAIDE.Library.Components.Powertrain.Converters.DC_Motor
    RCAIDE.Library.Components.Powertrain.Converters.PMSM_Motor
    """


    ones_row    = segment.state.ones_row 
    propulsor_conditions[generator.tag]                         = Conditions()
    propulsor_conditions[generator.tag].inputs                  = Conditions()
    propulsor_conditions[generator.tag].outputs                 = Conditions()
    propulsor_conditions[generator.tag].torque                  = 0. * ones_row(1) 
    propulsor_conditions[generator.tag].omega                   = 0. * ones_row(1) 
    propulsor_conditions[generator.tag].torque                  = 0. * ones_row(1) 
    propulsor_conditions[generator.tag].current                 = 0. * ones_row(1) 
    propulsor_conditions[generator.tag].voltage                 = 0. * ones_row(1) 
    return 

