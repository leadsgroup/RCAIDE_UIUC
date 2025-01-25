# RCAIDE/Methods/Energy/Sources/Cryogenic_Tanks/append_cryogenic_tank_conditions.py
# 
# 
# Created:  Jan 2025, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ----------------------------------------------------------------------------------------------------------------------  
def append_cryogenic_tank_conditions(cryogenic_tank,segment,cryogenic_line): 
    ones_row    = segment.state.ones_row                 
    segment.state.conditions.energy[cryogenic_line.tag][cryogenic_tank.tag]                 = Conditions()  
    segment.state.conditions.energy[cryogenic_line.tag][cryogenic_tank.tag].mass_flow_rate  = ones_row(1)  
    segment.state.conditions.energy[cryogenic_line.tag][cryogenic_tank.tag].mass            = ones_row(1)
    
    return 
