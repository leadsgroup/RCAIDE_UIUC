# RCAIDE/Framework/Mission/Mission.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports        
from RCAIDE.Framework.Core import Container 

# ----------------------------------------------------------------------------------------------------------------------
#  Mission
# ----------------------------------------------------------------------------------------------------------------------  
class Missions(Container):
    """
    Top-level container class for organizing mission analyses

    Attributes
    ----------
    tag : str
        Identifier for the missions container, defaults to 'missions'

    Notes
    -----
    This class serves as the highest-level container for organizing and managing
    mission analyses. It provides a structure for storing multiple mission
    profiles and their associated segments. Each mission within the container
    can represent different operational scenarios or analysis cases.

    The class handles:
    - Mission organization and storage
    - Mission sequence management
    - Analysis case management
    - Results collection and organization

    **Typical Usage**
    
    Missions are typically organized as:
    - Multiple mission profiles
        * Different operational scenarios
        * Various flight conditions
        * Alternative mission objectives
    - Analysis variations
        * Parameter studies
        * Performance evaluations
        * Optimization cases

    **Mission Organization**
    
    Each mission can contain:
    - Multiple segments
    - Different vehicle configurations
    - Varying environmental conditions
    - Specific analysis requirements

    See Also
    --------
    RCAIDE.Framework.Core.Container
    RCAIDE.Framework.Mission.Segments.Segment
    """
    
    def __defaults__(self):
        """
        Sets default values for the missions container

        Notes
        -----
        Initializes the basic container structure with default tag.
        """
        self.tag = 'missions'

    def append_mission(self, mission):
        """
        Adds a new mission to the container

        Notes
        -----
        Appends a mission profile to the container. Missions are
        executed in the order they are added unless specified
        otherwise.

        Parameters
        ----------
        mission : Mission
            Mission profile to be added to container

        Returns
        -------
        None
        """
        self.append(mission)
        return        
    
     