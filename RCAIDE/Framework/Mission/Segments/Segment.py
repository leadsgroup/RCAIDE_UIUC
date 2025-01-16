# RCAIDE/Framework/Mission/Segments/Segment.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE Imports
from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses                    import Analysis, Settings, Process   
from RCAIDE.Framework.Mission.Common     import State 

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSES
# ----------------------------------------------------------------------------------------------------------------------  
class Segment(Analysis):
    """
    Base class for all mission segments

    Attributes
    ----------
    settings : Settings
        Configuration settings for the segment
    state : State
        Current state of the vehicle
    analyses : Analysis.Container
        Container for analysis methods
    process : Process
        Process flow control object
    conditions : Data
        Reference to state.conditions

    Notes
    -----
    This class provides the fundamental structure for all mission segments.
    It establishes the framework for initialization, convergence, iteration,
    and post-processing of flight segments. The class manages flight dynamics
    and control variables through a comprehensive data structure.

    The segment processes include:
    - Process initialization
    - State convergence
    - Iteration control
    - Post-processing
    - Flight dynamics and control management

    **Flight Dynamics Controls**
    
    The class manages the following control variables:
    - Body angles (pitch, roll, yaw)
    - Bank angle
    - Wind angles
    - Time and velocity
    - Altitude and acceleration
    - Control surface deflections
        * Elevator
        * Rudder
        * Flaps
        * Slats
        * Ailerons
    - Thrust settings and vectoring

    **Process Flow**
    
    Initialize:
    - Set up initial conditions
    - Configure analyses

    Converge:
    - Iterate until convergence criteria met

    Iterate:
    - Update unknowns
    - Process conditions
    - Evaluate residuals

    Post Process:
    - Finalize results
    - Update state

    See Also
    --------
    RCAIDE.Framework.Analyses.Analysis
    RCAIDE.Framework.Mission.Common.State
    RCAIDE.Framework.Analyses.Process
    """
    
    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes the basic structure of a mission segment including:
        - Settings container
        - State object
        - Analysis container
        - Process control structure
        - Flight dynamics and control variables

        All control variables are initialized as inactive with no
        default values or assignments.
        """          
        
        self.settings                      = Settings() 
        self.state                         = State() 
        self.analyses                      = Analysis.Container() 
        self.process                       = Process() 
        self.process.initialize            = Process()
          
        self.process.converge              = Process()
        self.process.iterate               = Process()
        self.process.iterate.unknowns      = Process()
        self.process.iterate.initials      = Process()
        self.process.iterate.conditions    = Process()
        self.process.iterate.residuals     = Process()
        self.process.post_process          = Process()  
        
        self.conditions = self.state.conditions 
        
        return
    
    def initialize(self):
        """
        Executes the segment initialization process

        Notes
        -----
        Performs initial setup of the segment including:
        - State variable initialization
        - Analysis configuration
        - Process setup
        
        This method is called automatically at the start of
        segment evaluation.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """        
        self.process.initialize(self)
        return
    
    def converge(self, state):
        """
        Executes the segment convergence process

        Notes
        -----
        Iterates the segment solution until convergence criteria are met.
        Handles the convergence of:
        - Flight dynamics
        - Control surface settings
        - Performance parameters

        Parameters
        ----------
        state : Data
            Current segment state data structure

        Returns
        -------
        None
        """             
        self.process.converge(self,state)    
    
    def iterate(self):
        """
        Executes a single iteration of the segment solution process

        Notes
        -----
        Performs one complete iteration including:
        - Unknown variable updates
        - Condition evaluations
        - Residual calculations
        - State updates

        Parameters
        ----------
        None

        Returns
        -------
        None
        """        
        self.process.iterate(self)
        return
    
    def post_process(self):
        """
        Executes segment post-processing operations

        Notes
        -----
        Performs final calculations and cleanup including:
        - Performance metric calculations
        - Data storage and formatting
        - State finalization
        - Resource cleanup

        Parameters
        ----------
        None

        Returns
        -------
        None
        """         
        self.process.post_process(self)
        return
    
    def evaluate(self, state=None):
        """
        Executes the complete segment evaluation process

        Notes
        -----
        Runs the full segment analysis sequence:
        1. Initialization
        2. Convergence
        3. Iteration
        4. Post-processing

        This is the main entry point for segment execution.

        Parameters
        ----------
        state : Data, optional
            Initial state data structure. If None, uses self.state

        Returns
        -------
        self : Segment
            Returns self for method chaining
        """          
        if state is None:
            state = self.state
        self.process(self)
        return self
    
    def flight_dynamics_and_controls(self):
        """
        Initializes flight dynamics flags and control variable structures

        Notes
        -----
        Sets up data structures for:
        - Force and moment tracking (x, y, z axes)
        - Control variable management
            * Body angles and orientations
            * Flight parameters (velocity, altitude, etc.)
            * Control surface deflections
            * Propulsion controls
        
        All control variables are initialized as inactive and must be
        explicitly activated and configured for use.
        """
        self.flight_dynamics                                             = Data()
        self.flight_dynamics.force_x                                     = False 
        self.flight_dynamics.force_y                                     = False 
        self.flight_dynamics.force_z                                     = False 
        self.flight_dynamics.moment_x                                    = False 
        self.flight_dynamics.moment_y                                    = False 
        self.flight_dynamics.moment_z                                    = False    
        
        self.assigned_control_variables                                              = Data() 
        
        self.assigned_control_variables.body_angle                                   = Data()
        self.assigned_control_variables.body_angle.active                            = False               
        self.assigned_control_variables.body_angle.initial_guess_values              = None

        self.assigned_control_variables.bank_angle                                   = Data()
        self.assigned_control_variables.bank_angle.active                            = False 
        self.assigned_control_variables.bank_angle.initial_guess_values              = None

        self.assigned_control_variables.wind_angle                                   = Data()
        self.assigned_control_variables.wind_angle.active                            = False             
        self.assigned_control_variables.wind_angle.initial_guess_values              = None   

        self.assigned_control_variables.elapsed_time                                 = Data()
        self.assigned_control_variables.elapsed_time.active                          = False                 
        self.assigned_control_variables.elapsed_time.initial_guess_values            = None  
    
        self.assigned_control_variables.velocity                                     = Data()
        self.assigned_control_variables.velocity.active                              = False                  
        self.assigned_control_variables.velocity.initial_guess_values                = None
        
        self.assigned_control_variables.acceleration                                 = Data()
        self.assigned_control_variables.acceleration.active                          = False                 
        self.assigned_control_variables.acceleration.initial_guess_values            = None
        
        self.assigned_control_variables.altitude                                     = Data()
        self.assigned_control_variables.altitude.active                              = False                 
        self.assigned_control_variables.altitude.initial_guess_values                = None
    
        self.assigned_control_variables.throttle                                     = Data() 
        self.assigned_control_variables.throttle.active                              = False                
        self.assigned_control_variables.throttle.assigned_propulsors                 = None       
        self.assigned_control_variables.throttle.initial_guess_values                = None
    
        self.assigned_control_variables.elevator_deflection                          = Data() 
        self.assigned_control_variables.elevator_deflection.active                   = False      
        self.assigned_control_variables.elevator_deflection.assigned_surfaces        = None 
        self.assigned_control_variables.elevator_deflection.initial_guess_values     = None

        self.assigned_control_variables.rudder_deflection                            = Data()
        self.assigned_control_variables.rudder_deflection.active                     = False
        self.assigned_control_variables.rudder_deflection.assigned_surfaces          = None 
        self.assigned_control_variables.rudder_deflection.initial_guess_values       = None

        self.assigned_control_variables.flap_deflection                              = Data() 
        self.assigned_control_variables.flap_deflection.active                       = False          
        self.assigned_control_variables.flap_deflection.assigned_surfaces            = None 
        self.assigned_control_variables.flap_deflection.initial_guess_values         = None

        self.assigned_control_variables.slat_deflection                              = Data() 
        self.assigned_control_variables.slat_deflection.active                       = False          
        self.assigned_control_variables.slat_deflection.assigned_surfaces            = None 
        self.assigned_control_variables.slat_deflection.initial_guess_values         = None            
    
        self.assigned_control_variables.aileron_deflection                           = Data() 
        self.assigned_control_variables.aileron_deflection.active                    = False      
        self.assigned_control_variables.aileron_deflection.assigned_surfaces         = None 
        self.assigned_control_variables.aileron_deflection.initial_guess_values      = None
    
        self.assigned_control_variables.thrust_vector_angle                          = Data() 
        self.assigned_control_variables.thrust_vector_angle.active                   = False        
        self.assigned_control_variables.thrust_vector_angle.assigned_propulsors      = None 
        self.assigned_control_variables.thrust_vector_angle.initial_guess_values     = None
        
        return     
           
# ----------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------

class Container(Segment):
    """
    Container class for organizing multiple mission segments

    Attributes
    ----------
    segments : Process
        Container for mission segments
    state : State.Container
        Container for segment states

    Notes
    -----
    This class provides organization and management for multiple mission
    segments. It allows segments to be grouped and processed together
    while maintaining proper sequencing and data flow.

    The container handles:
    - Segment storage and organization
    - State management across segments
    - Sequential segment execution
    - Data transfer between segments

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Segment
    RCAIDE.Framework.Mission.Common.State
    """    
    
    def __defaults__(self):
        """
        Sets default values for the container

        Notes
        -----
        Initializes:
        - Empty segments container
        - Container state structure
        """          
        self.segments = Process()
        self.state = State.Container()
        
    def append_segment(self, segment):
        """
        Adds a new segment to the container

        Notes
        -----
        Appends a segment to the sequence of mission segments.
        Segments are executed in the order they are added.

        Parameters
        ----------
        segment : Segment
            Mission segment to be added to container

        Returns
        -------
        None
        """          
        self.segments.append(segment)
        return    
        
Segment.Container = Container