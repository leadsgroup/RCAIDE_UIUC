# RCAIDE/Framework/Mission/Segment/Evaluate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import Units
from RCAIDE.Framework.Mission.Segments         import Segment
from RCAIDE.Framework.Mission.Common.Results   import Results
from RCAIDE.Library.Mission            import Common , Solver 
from RCAIDE.Framework.Analyses                 import Process  

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSES
# ---------------------------------------------------------------------------------------------------------------------- 
class Evaluate(Segment):
    """
    Base class for mission segments that evaluate vehicle performance

    Attributes
    ----------
    temperature_deviation : float
        Temperature offset from standard atmosphere [K], defaults to 0.0
    sideslip_angle : float
        Aircraft sideslip angle [rad], defaults to 0.0
    angle_of_attack : float
        Aircraft angle of attack [rad], defaults to 1.0 degree
    bank_angle : float
        Aircraft bank angle [rad], defaults to 0.0
    trim_lift_coefficient : float
        Target lift coefficient for trim, optional

    Notes
    -----
    This class provides the core framework for analyzing vehicle performance
    in different flight segments. It handles the initialization, iteration,
    and convergence of flight dynamics calculations. The class serves as a
    base for specific mission segment types like cruise, climb, descent, etc.

    The segment processes include:
    - State initialization and expansion
    - Flight dynamics and controls setup
    - Time-based differential updates
    - Atmosphere and environment modeling
    - Force and moment calculations
    - Energy and emissions tracking

    **Major Assumptions**
    * Quasi-steady flight dynamics
    * Standard atmosphere model
    * Rigid body dynamics
    * Small angle approximations
    * Point mass for certain calculations

    **Process Flow**
    
    Initialize:
    - expand_state
    - differentials
    - conditions

    Converge:
    - converge_root

    Iterate:
    - initials (time, weights, energy, position)
    - unknowns
    - conditions (differentials through planet_position)
    - residuals

    Post Process:
    - inertial_position
    - energy
    - noise
    - emissions

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Segment
    RCAIDE.Framework.Mission.Common.Results
    RCAIDE.Library.Mission.Common
    """
    
    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes comprehensive flight dynamics evaluation
        with initialization, iteration, convergence, and post-processing
        steps. Sets up the framework for analyzing vehicle performance
        in specific mission segments.
        """           
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.temperature_deviation                = 0.0
        self.sideslip_angle                       = 0.0 
        self.angle_of_attack                      = 1.0 *  Units.degree
        self.bank_angle                           = 0.0
        self.trim_lift_coefficient                = None
        self.state.conditions.update(Results())
        
        # ---------------------------------------------------------------
        # Define Flight Controls and Residuals 
        # ---------------------------------------------------------------     
        self.flight_dynamics_and_controls()    
        
        # --------------------------------------------------------------
        #   Initialize - before iteration
        # -------------------------------------------------------------- 
        initialize                         = self.process.initialize 
        initialize.expand_state            = Solver.expand_state
        initialize.differentials           = Common.Initialize.differentials_dimensionless 
        initialize.conditions              = None 

        # --------------------------------------------------------------         
        #   Converge 
        # -------------------------------------------------------------- 
        converge = self.process.converge 
        converge.converge_root             = Solver.converge_root        

        # --------------------------------------------------------------          
        #   Iterate  
        # -------------------------------------------------------------- 
        iterate                            = self.process.iterate 
        iterate.initials                   = Process()
        iterate.initials.time              = Common.Initialize.time
        iterate.initials.weights           = Common.Initialize.weights
        iterate.initials.energy            = Common.Initialize.energy
        iterate.initials.inertial_position = Common.Initialize.inertial_position
        iterate.initials.planet_position   = Common.Initialize.planet_position
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials         = Common.Update.differentials_time
        iterate.conditions.orientations          = Common.Update.orientations
        iterate.conditions.acceleration          = Common.Update.acceleration
        iterate.conditions.angular_acceleration  = Common.Update.angular_acceleration
        iterate.conditions.altitude              = Common.Update.altitude
        iterate.conditions.atmosphere            = Common.Update.atmosphere
        iterate.conditions.gravity               = Common.Update.gravity
        iterate.conditions.freestream            = Common.Update.freestream
        iterate.conditions.thrust                = Common.Update.thrust
        iterate.conditions.aerodynamics          = Common.Update.aerodynamics
        iterate.conditions.stability             = Common.Update.stability
        iterate.conditions.weights               = Common.Update.weights
        iterate.conditions.forces                = Common.Update.forces
        iterate.conditions.moments               = Common.Update.moments
        iterate.conditions.planet_position       = Common.Update.planet_position

        # Solve Residuals
        iterate.residuals = Process()

        # --------------------------------------------------------------  
        #  Post Process   
        # -------------------------------------------------------------- 
        post_process                    = self.process.post_process   
        post_process.inertial_position  = Common.Update.linear_inertial_horizontal_position
        post_process.energy             = Common.Update.energy 
        post_process.noise              = Common.Update.noise
        post_process.emissions          = Common.Update.emissions
        
        return

