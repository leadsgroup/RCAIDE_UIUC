# RCAIDE/Library/Missions/Common/helper_functions.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Core  import Data 

def pre_process(mission):
    """
    Executes pre-processing steps for all mission segments

    Parameters
    ----------
    mission : Mission
        The mission containing segments to be analyzed

    Notes
    -----
    This function calls the pre_process() method on each segment in the mission.
    Pre-processing typically includes:
    - Initializing analysis models
    - Setting up numerical schemes
    - Preparing state variables

    **Required Mission Components**

    mission.segments:
        Each segment must implement:
        - pre_process() : method
            Segment-specific preprocessing

    Returns
    -------
    None
        Updates mission segments directly

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    for tag,segment in mission.segments.items():     
        segment.pre_process()

def sequential_segments(mission):  
    """
    Evaluates mission segments in sequence with state continuity

    Parameters
    ----------
    mission : Mission
        The mission containing segments to be analyzed

    Notes
    -----
    This function processes mission segments sequentially, passing final
    state from each segment as initial conditions to the next segment.
    It handles state expansion and segment evaluation.

    **Process Flow**

    For each segment:
    1. Set initial conditions from previous segment if available
    2. Expand state variables
    3. Evaluate segment
    4. Store for next segment

    **Required Mission Components**

    mission.segments:
        Each segment must implement:
        - process.initialize.expand_state : method
            State expansion method
        - evaluate() : method
            Segment evaluation method

    Returns
    -------
    None
        Updates mission segments directly

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    last_tag = None
    for tag,segment in mission.segments.items(): 
        if last_tag:
            segment.state.initials = mission.segments[last_tag].state
        last_tag = tag        
        
        segment.process.initialize.expand_state(segment) 
        segment.process.initialize.expand_state = RCAIDE.Library.Methods.skip        
        segment.evaluate()
        
def update_segments(mission):   
    """
    Executes post-processing steps for all mission segments

    Parameters
    ----------
    mission : Mission
        The mission containing segments to be analyzed

    Notes
    -----
    This function calls the post_process() method on each segment in the mission.
    Post-processing typically includes:
    - Final state updates
    - Results processing
    - Data cleanup

    **Required Mission Components**

    mission.segments:
        Each segment must implement:
        - post_process() : method
            Segment-specific post-processing

    Returns
    -------
    None
        Updates mission segments directly

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    for tag,segment in mission.segments.items():
        segment.post_process() 
        
def merge_segment_states(mission): 
    """
    Combines all segment states into unified mission state

    Parameters
    ----------
    mission : Mission
        The mission containing segments to be analyzed

    Notes
    -----
    This function merges the states from all segments into a single
    mission-level state object using the merged() method.

    **Required Mission Components**

    mission:
        - merged() : method
            State merging method
        - state : Data
            Mission state container

    Returns
    -------
    None
        Updates mission.state directly

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    mission.state.update(mission.merged())
    
def unpack_segments(mission): 
    """
    Distributes mission unknowns back to individual segments

    Parameters
    ----------
    mission : Mission
        The mission containing segments to be analyzed

    Notes
    -----
    This function takes the mission-level unknowns and distributes them
    back to the appropriate segments based on segment size and ordering.

    **Required Mission Components**

    mission:
        state:
            unknowns : dict
                Mission-level unknown variables
        segments : list
            List of mission segments
            Each segment must have:
            - state.unknowns : dict
                Segment unknown variables

    **Major Assumptions**
    * Consistent unknown variable names
    * Valid segment ordering
    * Compatible array sizes

    Returns
    -------
    None
        Updates segment states directly

    See Also
    --------
    RCAIDE.Framework.Mission.Segments
    """
    # Build a dict with the sections, sections start at 0
    counter = Data()
    
    for key in mission.state.unknowns.keys():
        counter[key] = 0

    for i, segment in enumerate(mission.segments):
        for key in segment.state.unknowns.keys():
            if key=='tag':
                continue
            points = segment.state.unknowns[key].size
            segment.state.unknowns[key] = mission.state.unknowns[key][counter[key]:counter[key]+points]
            counter[key] = counter[key]+points
            
    return
            
            