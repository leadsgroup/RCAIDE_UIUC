# RCAIDE/Framework/Mission/Segments/Ground/Landing.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Mission.Segments.Evaluate        import Evaluate 
from RCAIDE.Framework.Core                                      import Units , Data 
from RCAIDE.Library.Mission.Segments                  import Ground  
from RCAIDE.Library.Mission.Common                    import Residuals , Unpack_Unknowns, Update

# ----------------------------------------------------------------------------------------------------------------------
#  Landing
# ----------------------------------------------------------------------------------------------------------------------

class Landing(Evaluate):
    """
    Mission segment for aircraft landing with ground roll deceleration

    Attributes
    ----------
    velocity_start : float
        Touchdown velocity [m/s], defaults to 150 knots
    velocity_end : float
        Final ground velocity [m/s], defaults to 0.0
    friction_coefficient : float
        Braking friction coefficient [-], defaults to 0.4
    throttle : float
        Engine throttle setting [-], defaults to 0.1
    altitude : float
        Ground altitude [m], defaults to 0.0
    reverse_thrust_ratio : float
        Thrust reverser effectiveness [-], defaults to 0.1
    true_course : float
        True course angle [rad], defaults to 0 degrees

    state.residuals.final_velocity_error : float
        Error in final velocity constraint
    state.residuals.force_x : array_like
        Longitudinal force balance residuals [N]
    state.unknowns.elapsed_time : float
        Landing roll duration [s], defaults to 30 s
    state.unknowns.ground_velocity : array_like
        Ground velocity history [m/s]
    state.conditions.ground.friction_coefficient : array_like
        Friction coefficient history [-]
    state.conditions.frames.inertial.ground_force_vector : array_like
        Ground reaction forces [N]

    Notes
    -----
    This segment simulates the landing ground roll from touchdown to full stop,
    including braking and thrust reverser effects. The deceleration is modeled
    using ground friction forces and reduced/reversed thrust.

    **Friction Coefficient Reference Values**
    
    * Dry asphalt/concrete: 0.04 brakes off, 0.4 brakes on
    * Wet asphalt/concrete: 0.05 brakes off, 0.225 brakes on
    * Icy asphalt/concrete: 0.02 brakes off, 0.08 brakes on
    * Hard turf: 0.05 brakes off, 0.4 brakes on
    * Firm dirt: 0.04 brakes off, 0.3 brakes on
    * Soft turf: 0.07 brakes off, 0.2 brakes on
    * Wet grass: 0.08 brakes off, 0.2 brakes on

    The segment processes include:
    - Landing conditions initialization
    - Ground forces calculation
    - Flight dynamics evaluation
    - Ground condition tracking

    **Major Assumptions**
    * Rigid ground surface
    * Constant friction coefficient
    * Point contact with ground
    * No tire deformation effects
    * No aerodynamic ground effects
    * Constant thrust reverser effectiveness
    * Immediate brake application

    **Process Flow**
    
    Initialize:
    - conditions (landing roll)

    Iterate:
    - conditions.forces_ground
    - unknowns.mission (ground conditions)
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Segments.Ground
    RCAIDE.Library.Mission.Common.Update
    RCAIDE.Framework.Mission.Segments.Ground.Ground

    References
    ----------
    .. [1] Gudmundsson, S. (2014). General Aviation Aircraft Design: Applied
       Methods and Procedures. Elsevier, Waltham, MA, USA. p.938
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes ground forces calculation and flight
        dynamics evaluation with braking and thrust reverser effects.
        """
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
 
        self.velocity_start       = 150 * Units.knots
        self.velocity_end         = 0.0
        self.friction_coefficient = 0.4
        self.throttle             = 0.1
        self.altitude             = 0.0
        self.reverse_thrust_ratio = 0.1
        self.true_course          = 0.0 * Units.degrees 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Unique Mission Unknowns and Residuals
        # -------------------------------------------------------------------------------------------------------------- 
        ones_row_m1                               = self.state.ones_row_m1
        self.state.residuals.final_velocity_error = 0.0
        self.state.residuals.force_x              = ones_row_m1(1) * 0.0    
        self.state.unknowns.elapsed_time          = 30.                        
        self.state.unknowns.ground_velocity       = ones_row_m1(1) * 0  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Conditions 
        # --------------------------------------------------------------------------------------------------------------          
        ones_row = self.state.ones_row  
        self.state.conditions.ground                              = Data() 
        self.state.conditions.ground.friction_coefficient         = ones_row(1) * 0.0
        self.state.conditions.frames.inertial.ground_force_vector = ones_row(3) * 0.0 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize
        initialize.conditions              = Ground.Landing.initialize_conditions  
        iterate                            = self.process.iterate   
        iterate.conditions.forces_ground   = Update.ground_forces
        iterate.unknowns.mission           = Unpack_Unknowns.ground
        iterate.residuals.flight_dynamics  = Residuals.flight_dynamics    

        return