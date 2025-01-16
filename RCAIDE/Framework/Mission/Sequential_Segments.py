# RCAIDE/Framework/Mission/Sequential_Segments.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports   
import RCAIDE
from RCAIDE.Library.Mission.Common.Segments    import  sequential_segments
from RCAIDE.Library.Mission.Common.Pre_Process import  aerodynamics,stability, energy,emissions, set_residuals_and_unknowns
from RCAIDE.Framework.Core                               import Container as ContainerBase
from RCAIDE.Framework.Analyses                           import Process 
from . import Segments

# ----------------------------------------------------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  -Mission
class Sequential_Segments(Segments.Segment.Container):
    """
    Mission analysis class that evaluates segments sequentially

    Attributes
    ----------
    tag : str
        Identifier for the mission, defaults to 'mission'
    process.initialize : Process
        Container for initialization processes
        - aero: Aerodynamics initialization
        - stability: Stability analysis setup
        - energy: Energy analysis initialization
        - emissions: Emissions tracking setup
        - set_residuals_and_unknowns: Problem setup

    Notes
    -----
    This class provides a framework for analyzing mission segments in sequence,
    where each segment is fully evaluated before proceeding to the next. This
    approach ensures proper state propagation and maintains dependencies between
    consecutive segments.

    The analysis process includes:
    - Aerodynamic analysis initialization
    - Stability evaluation setup
    - Energy tracking configuration
    - Emissions analysis preparation
    - Sequential segment evaluation

    **Process Flow**
    
    Initialize:
    1. Aerodynamics setup
    2. Stability analysis configuration
    3. Energy tracking initialization
    4. Emissions analysis setup
    5. Residuals and unknowns definition

    Converge:
    - Sequential segment evaluation
    - State propagation between segments
    - Results compilation

    **Major Features**
    * Sequential segment processing
    * State propagation management
    * Comprehensive initialization
    * Results tracking
    * Multi-domain analysis capability

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Segment.Container
    RCAIDE.Library.Mission.Common.Segments
    RCAIDE.Library.Mission.Common.Pre_Process
    """
    
    def __defaults__(self):
        """
        Sets default values for sequential segment analysis

        Notes
        -----
        Initializes the analysis structure including:
        - Process containers
        - Analysis modules
        - Convergence handling
        
        Removes iteration process as segments are evaluated sequentially.
        """

        self.tag = 'mission'
        
        #   Initialize   
        self.process.initialize                                = Process() 
        self.process.initialize.aero                           = aerodynamics
        self.process.initialize.stability                      = stability
        self.process.initialize.energy                         = energy
        self.process.initialize.emissions                      = emissions
        self.process.initialize.set_residuals_and_unknowns     = set_residuals_and_unknowns
 
        #   Converge 
        self.process.converge    = sequential_segments
         
        #   Iterate     
        del self.process.iterate  

        return  

                        
    def evaluate(self,state=None):
        """
        Executes the sequential segment analysis

        Notes
        -----
        Processes all segments in sequence, maintaining state continuity
        between segments. Each segment is fully evaluated before moving
        to the next.

        Parameters
        ----------
        state : Data, optional
            Initial state data structure. If None, uses self.state

        Returns
        -------
        self : Sequential_Segments
            Returns self for method chaining
        """  
        
        if state is None:
            state = self.state
        self.process(self)
        return self     
        
    
# ----------------------------------------------------------------------
#   Container Class
# ----------------------------------------------------------------------
class Container(ContainerBase):
    """
    Container class for organizing sequential segment missions

    Notes
    -----
    Provides structure for managing multiple sequential segment missions.
    Allows for organization and evaluation of different mission profiles
    using the sequential segment approach.

    The container supports:
    - Multiple mission storage
    - Mission evaluation management
    - Results organization
    - State handling across missions

    See Also
    --------
    RCAIDE.Framework.Core.Container
    RCAIDE.Framework.Mission.Sequential_Segments
    """
    
    def evaluate(self,state=None):
        """
        Evaluates all missions in the container

        Notes
        -----
        Processes each mission in the container, maintaining proper
        separation between different mission analyses.

        Parameters
        ----------
        state : Data, optional
            Initial state data structure

        Returns
        -------
        Results : Data
            Container of mission results
        """
        pass

# Link container
Sequential_Segments.Container = Container