# RCAIDE/Library/Methods/Powertrain/Converters/External_Power_Shaft/compute_shaft_power_offtaker.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# compute_external_power_shaft_performance
# ----------------------------------------------------------------------------------------------------------------------     
def compute_external_power_shaft_performance(external_power_shaft,external_power_shaft_conditions, conditions):
    """ This computes the work done from the power draw. The following properties are computed: 
    external_power_shaft.outputs.
      power        (numpy.ndarray): power                              [W]
      work_done    (numpy.ndarray): work done normalized by mass flow  [J/(kg/s)] 

    Assumptions:
        None

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        external_power_shaft
          .inputs.mdhc                  (numpy.ndarray): Compressor nondimensional mass flow   [unitless] 
          .inputs.reference_temperature (numpy.ndarray): Reference temperature                 [K]
          .inputs.reference_pressure    (numpy.ndarray): Reference pressure                    [Pa]
          .power_draw                           (float): power draw                            [W]

    Returns:
        None 
    """  
    if external_power_shaft.power_draw == 0.0:
        external_power_shaft_conditions.outputs.work_done = np.array([0.0]) 
    else: 
        # unpack 
        total_temperature_reference = external_power_shaft_conditions.inputs.total_temperature_reference
        total_pressure_reference    = external_power_shaft_conditions.inputs.total_pressure_reference
        mdhc                        = external_power_shaft_conditions.inputs.mdhc
        Tref                        = external_power_shaft.reference_temperature
        Pref                        = external_power_shaft.reference_pressure
        
        # compute core mass flow rate 
        mdot_core = mdhc * np.sqrt(Tref / total_temperature_reference) * (total_pressure_reference / Pref)
        if external_power_shaft.fixed_power_ratio:  
            external_power_shaft_conditions.outputs.power     = external_power_shaft.power_draw
            external_power_shaft_conditions.outputs.work_done = external_power_shaft_conditions.outputs.power / mdot_core  
            external_power_shaft_conditions.outputs.work_done[mdot_core == 0] = 0 
            external_power_shaft_conditions.external_power_shaft.percent_power = external_power_shaft_conditions.outputs.work_done / external_power_shaft_conditions.inputs.compressor.work_done
        else: 
            external_power_shaft_conditions.outputs.work_done = external_power_shaft.power_draw_percentage * external_power_shaft_conditions.inputs.compressor.work_done
            external_power_shaft_conditions.outputs.power     = external_power_shaft_conditions.outputs.work_done * mdot_core
            external_power_shaft_conditions.external_power_shaft.percent_power[:,0] = external_power_shaft.power_draw_percentage   
    return 