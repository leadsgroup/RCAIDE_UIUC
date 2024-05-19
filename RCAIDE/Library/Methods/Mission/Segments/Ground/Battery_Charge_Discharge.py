## @ingroup Library-Methods-Missions-Segments-Ground
# RCAIDE/Library/Methods/Missions/Segments/Ground/Battery_Charge_or_Discharge.py
# 
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Missions-Segments-Ground 
def initialize_conditions(segment):  
    """Sets the specified conditions which are given for the segment type.

    Assumptions: 
    During recharging, the charge time associated with the largest capacity battery pack is used 
    
    Source:
    N/A

    Inputs:
    segment.overcharge_contingency              [-]
    battery.                                    [-]

    Outputs: 
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """    
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions   
    
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_nondim  = segment.state.numerics.dimensionless.control_points
    time      = t_nondim * ( segment.time ) + t_initial
    
    segment.state.conditions.frames.inertial.time[:,0] = time[:,0] 

