# RCAIDE/Framework/Mission/Segments/Transition/Constant_Acceleration_Constant_Angle_Linear_Climb.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                            import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                           import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Angle_Linear_Climb
# ----------------------------------------------------------------------------------------------------------------------
class Constant_Acceleration_Constant_Angle_Linear_Climb(Evaluate):
    """
    Mission segment for transitioning with constant acceleration and climb angle

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], required
    altitude_end : float
        Final altitude [m], required
    air_speed_start : float
        Initial true airspeed [m/s], required
    climb_angle : float
        Flight path angle [rad], defaults to 0.0
    acceleration : float
        Longitudinal acceleration [m/s^2], defaults to 1.0
    pitch_initial : float
        Initial pitch angle [rad], required
    pitch_final : float
        Final pitch angle [rad], defaults to 0.0
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment simulates a transition maneuver where the vehicle maintains
    constant longitudinal acceleration and flight path angle while climbing.
    Typically used for VTOL transition phases or acceleration climbs. The
    pitch angle varies linearly between initial and final values.

    The segment processes include:
    - Transition conditions initialization
    - Control surface unpacking
    - Flight dynamics evaluation
    - Orientation tracking

    **Major Assumptions**
    * Constant longitudinal acceleration
    * Constant flight path angle
    * Linear pitch angle variation
    * Quasi-steady aerodynamics
    * No lateral-directional coupling
    * Sufficient thrust available
    * Small angle approximations

    **Process Flow**
    
    Initialize:
    - conditions (transition climb)

    Iterate:
    - unknowns.mission (orientation)
    - unknowns.controls (control surfaces)
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Common
    RCAIDE.Library.Mission.Segments.Transition
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes transition maneuver evaluation with
        constant acceleration and flight path angle constraints.
        """           
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude_start         = None
        self.altitude_end           = None
        self.air_speed_start        = None
        self.climb_angle            = 0.0 * Units['rad'] 
        self.acceleration           = 1.  * Units['m/s/s'] 
        self.pitch_initial          = None
        self.pitch_final            = 0.0 * Units['rad']
        self.true_course            = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize 
        initialize.conditions              = Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb.initialize_conditions  
        iterate                            = self.process.iterate  
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return

