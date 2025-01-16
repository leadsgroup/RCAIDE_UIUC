# RCAIDE/Framework/Mission/Segments/Ground/Ground.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core                            import Units , Data 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission.Common                    import Residuals , Unpack_Unknowns, Update
 
# ----------------------------------------------------------------------------------------------------------------------
#  Ground
# ---------------------------------------------------------------------------------------------------------------------- 
class Ground(Evaluate):
    """
    Base segment for ground operations including takeoff and landing

    Attributes
    ----------
    ground_incline : float
        Ground slope angle [rad], defaults to 0.0
    friction_coefficient : float
        Rolling friction coefficient [-], defaults to 0.04
    throttle : float
        Engine throttle setting [-], required
    velocity_start : float
        Initial ground velocity [m/s], defaults to 0.0
    velocity_end : float
        Final ground velocity [m/s], defaults to 0.0
    altitude : float
        Ground altitude [m], defaults to 0.0
    true_course : float
        True course angle [rad], defaults to 0 degrees

    state.conditions.ground.incline : array_like
        Ground slope angle history [rad]
    state.conditions.ground.friction_coefficient : array_like
        Friction coefficient history [-]
    state.conditions.frames.inertial.ground_force_vector : array_like
        Ground reaction forces [N]

    Notes
    -----
    This is the base class for ground operation segments that include rolling
    friction effects. Used for takeoff and landing analysis.

    **Friction Coefficient Reference Values**
    
    * Dry asphalt/concrete: 0.04 brakes off, 0.4 brakes on
    * Wet asphalt/concrete: 0.05 brakes off, 0.225 brakes on
    * Icy asphalt/concrete: 0.02 brakes off, 0.08 brakes on
    * Hard turf: 0.05 brakes off, 0.4 brakes on
    * Firm dirt: 0.04 brakes off, 0.3 brakes on
    * Soft turf: 0.07 brakes off, 0.2 brakes on
    * Wet grass: 0.08 brakes off, 0.2 brakes on

    The segment processes include:
    - Ground forces calculation
    - Flight dynamics evaluation
    - Ground condition tracking

    **Major Assumptions**
    * Rigid ground surface
    * Constant friction coefficient
    * Point contact with ground
    * No tire deformation effects
    * No aerodynamic ground effects

    **Process Flow**
    
    Iterate:
    - unknowns.mission (ground conditions)
    - residuals.flight_dynamics
    - conditions.forces_ground

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Common.Residuals
    RCAIDE.Library.Mission.Common.Update

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
        dynamics evaluation with rolling friction effects.
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.ground_incline       = 0.0
        self.friction_coefficient = 0.04
        self.throttle             = None
        self.velocity_start       = 0.0
        self.velocity_end         = 0.0 
        self.altitude             = 0.0
        self.true_course          = 0.0 * Units.degrees      

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Conditions 
        # --------------------------------------------------------------------------------------------------------------          
        ones_row = self.state.ones_row  
        self.state.conditions.ground                              = Data()
        self.state.conditions.ground.incline                      = ones_row(1) * 0.0
        self.state.conditions.ground.friction_coefficient         = ones_row(1) * 0.0
        self.state.conditions.frames.inertial.ground_force_vector = ones_row(3) * 0.0 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------       
        iterate.unknowns.mission           = Unpack_Unknowns.ground
        iterate.residuals.flight_dynamics  = Residuals.flight_dynamics
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        iterate                            = self.process.iterate    
        iterate.conditions.forces_ground   = Update.ground_forces
    
        return