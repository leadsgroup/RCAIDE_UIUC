## @ingroup Library-Methods-Missions-Segments-Common-Pre_Process
# RCAIDE/Library/Methods/Missions/Common/Pre_Process/aerodynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE 
# ----------------------------------------------------------------------------------------------------------------------
#  aerodynamics
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Missions-Segments-Common-Pre_Process
def aerodynamics(mission):
    """ Runs aerdoynamics model and build surrogate
    
        Assumptions:
            N/A
        
        Inputs:
            None
            
        Outputs:
            None 

        Properties Used:
        N/A                
    """      
    last_tag = None
    for tag,segment in mission.segments.items():        
        if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Subsonic_VLM) or (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Supersonic_VLM): 
            if last_tag and  'compute' in mission.segments[last_tag].analyses.aerodynamics.process: 
                segment.analyses.aerodynamics.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.aerodynamics.process.compute.lift.inviscid_wings 
            else:          
                aero   = segment.analyses.aerodynamics
                aero.initialize()   
                last_tag = tag  
    return 