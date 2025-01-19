# RCAIDE/Library/Mission/Common/Update/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Battery Age
# ---------------------------------------------------------------------------------------------------------------------- 
def energy(segment):
    """
    Updates battery age and conditions based on segment operation

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function updates the battery age and conditions based on operating
    parameters, cell temperature, and time of operation. The specific aging
    model depends on the battery cell type.

    **Required Segment Components**

    segment:
        conditions:
            energy : dict
                Energy system conditions by component
        analyses.energy.vehicle.networks:
            busses:
                - battery_modules : list
                    Battery modules to update
        increment_battery_age_by_one_day : bool
            Flag to increment battery cycle day

    **Major Assumptions**
    * Valid battery models
    * Well-defined operating conditions
    * Compatible aging models
    * Proper temperature tracking

    Returns
    -------
    None
        Updates battery conditions directly

  
    """  
    # loop throuh networks in vehicle 
    for network in segment.analyses.energy.vehicle.networks: 
        if 'busses' in network: 
            busses  = network.busses
            for bus in busses:
                for battery in bus.battery_modules: 
                    increment_day = segment.increment_battery_age_by_one_day
                    battery_conditions  = segment.conditions.energy[bus.tag].battery_modules[battery.tag] 
                    battery.update_battery_age(segment,battery_conditions,increment_battery_age_by_one_day = increment_day) 