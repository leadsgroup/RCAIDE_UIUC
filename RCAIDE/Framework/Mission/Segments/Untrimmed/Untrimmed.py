# RCAIDE/Framework/Mission/Segments/Untrimmed/Untrimmed.py
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
from RCAIDE.Library.Mission                    import Common ,Solver,  Segments
from RCAIDE.Framework.Analyses                 import Process   
from RCAIDE.Library.Methods.skip               import skip 

# ----------------------------------------------------------------------------------------------------------------------
#  Untrimmed
# ---------------------------------------------------------------------------------------------------------------------- 

class Untrimmed(Segment):
    """
    Base segment class for untrimmed flight analysis

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
    linear_acceleration_x : float
        Body-axis x acceleration [m/s^2], defaults to 0.0
    linear_acceleration_y : float
        Body-axis y acceleration [m/s^2], defaults to 0.0
    linear_acceleration_z : float
        Body-axis z acceleration [m/s^2], defaults to 0.0 (positive down)
    roll_rate : float
        Body-axis roll rate [rad/s], defaults to 0.0
    pitch_rate : float
        Body-axis pitch rate [rad/s], defaults to 0.0
    yaw_rate : float
        Body-axis yaw rate [rad/s], defaults to 0.0
    state.numerics.number_of_control_points : int
        Number of analysis points, defaults to 2
    trim_lift_coefficient : float
        Target lift coefficient for trim, optional

    Notes
    -----
    This segment provides the base functionality for analyzing vehicle flight
    without enforcing trim conditions. Used for dynamic maneuvers or when
    analyzing off-nominal flight conditions. The segment handles flight dynamics,
    aerodynamics, and propulsion calculations in an untrimmed state.

    The segment processes include:
    - Flight dynamics and controls initialization
    - State expansion
    - Atmosphere and freestream conditions
    - Force and moment calculations
    - Stability analysis
    - Noise and emissions evaluation

    **Major Assumptions**
    * Quasi-steady aerodynamics
    * Rigid body dynamics
    * Standard atmosphere (with optional temperature deviation)
    * No trim requirements enforced
    * Small angle approximations for stability derivatives

    **Process Flow**
    
    Initialize:
    - expand_state
    - differentials
    - conditions

    Iterate:
    - initials (time, weights, position)
    - unknowns (controls, orientation)
    - conditions (atmosphere through moments)
    - residuals (flight dynamics)

    Post Process:
    - noise
    - skip (energy, emissions, position)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Segment
    RCAIDE.Library.Mission.Common
    RCAIDE.Framework.Mission.Common.Results
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes comprehensive flight dynamics evaluation
        without enforcing trim conditions. Includes initialization of flight
        controls and residuals.
        """           
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.temperature_deviation                   = 0.0
        self.sideslip_angle                          = 0.0 
        self.angle_of_attack                         = 1.0 *  Units.degree
        self.bank_angle                              = 0.0 
        self.linear_acceleration_x                   = 0.
        self.linear_acceleration_y                   = 0.  
        self.linear_acceleration_z                   = 0. # note that down is positive
        self.roll_rate                               = 0.
        self.pitch_rate                              = 0.  
        self.yaw_rate                                = 0.  
        self.state.numerics.number_of_control_points = 2     
        self.trim_lift_coefficient                   = None
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
        initialize.conditions              = Segments.Untrimmed.Untrimmed.initialize_conditions  
        
        # --------------------------------------------------------------          
        #   Iterate  
        # -------------------------------------------------------------- 
        iterate                            = self.process.iterate 
        iterate.initials                   = Process()
        iterate.initials.time              = Common.Initialize.time
        iterate.initials.weights           = Common.Initialize.weights
        iterate.initials.energy            = skip
        iterate.initials.inertial_position = Common.Initialize.inertial_position
        iterate.initials.planet_position   = Common.Initialize.planet_position
        
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials         = Common.Update.differentials_time
        iterate.conditions.orientations          = Common.Update.orientations
        iterate.conditions.acceleration          = skip 
        iterate.conditions.angular_acceleration  = skip 
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
        iterate.conditions.planet_position       = skip

        # Solve Residuals 
        iterate.unknowns.controls                = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission                 = Common.Unpack_Unknowns.orientation  
        iterate.residuals.flight_dynamics        = Common.Residuals.flight_dynamics

        # --------------------------------------------------------------  
        #  Post Process   
        # -------------------------------------------------------------- 
        post_process                    = self.process.post_process   
        post_process.inertial_position  = skip
        post_process.energy             = skip
        post_process.noise              = Common.Update.noise
        post_process.emissions          = skip
        
        return 