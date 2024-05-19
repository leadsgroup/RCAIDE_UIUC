## @ingroup Library-Methods-Missions-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/battery_age.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Battery Age
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Missions-Common-Update
def battery_age(segment):  
    """Updates battery age based on operating conditions, cell temperature and time of operation.
       Source: 
       Cell specific. See individual battery cell for more details

       Assumptions:
       Cell specific. See individual battery cell for more details

       Inputs: 
       segment.
           conditions                         - conditions of battery at each segment  [unitless]
           increment_battery_age_by_one_day   - flag to increment battery cycle day    [boolean]

       Outputs:
       N/A  

       Properties Used:
       N/A 
    """  
    # loop throuh networks in vehicle 
    for network in segment.analyses.energy.networks: 
        if 'busses' in network: 
            busses  = network.busses
            for bus in busses:
                for battery in bus.batteries: 
                    increment_day = segment.increment_battery_age_by_one_day
                    battery_conditions  = segment.conditions.energy[bus.tag][battery.tag] 
                    battery.update_battery_age(battery_conditions,increment_battery_age_by_one_day = increment_day) 