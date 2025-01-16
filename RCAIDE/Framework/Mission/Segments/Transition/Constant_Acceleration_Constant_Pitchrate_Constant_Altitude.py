# RCAIDE/Framework/Mission/Segments/Transition/Constant_Acceleration_Constant_Pitchrate_Constant_Altitude.py 
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                            import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                   import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Pitchrate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------
class Constant_Acceleration_Constant_Pitchrate_Constant_Altitude(Evaluate):
    """
    Mission segment for transitioning with constant acceleration and pitch rate at fixed altitude

    Attributes
    ----------
    altitude : float
        Flight altitude [m], required
    acceleration : float
        Longitudinal acceleration [m/s^2], defaults to 1.0
    air_speed_start : float
        Initial true airspeed [m/s], required
    air_speed_end : float
        Final true airspeed [m/s], defaults to 1.0 m/s
    pitch_initial : float
        Initial pitch angle [rad], required
    pitch_final : float
        Final pitch angle [rad], defaults to 0.0
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment simulates a transition maneuver where the vehicle maintains
    constant altitude while accelerating at a fixed rate and rotating at a
    constant pitch rate. Typically used for VTOL transition phases between
    hover and forward flight modes.

    The segment processes include:
    - Transition conditions initialization
    - Flight dynamics evaluation
    - Pitch rate and acceleration tracking

    **Major Assumptions**
    * Constant longitudinal acceleration
    * Constant pitch rate
    * Constant altitude maintained
    * Quasi-steady aerodynamics
    * No lateral-directional coupling
    * Sufficient thrust available
    * Small angle approximations
    * Prop-rotor pitch varies linearly with time

    **Process Flow**
    
    Initialize:
    - conditions (transition)

    Iterate:
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Common
    RCAIDE.Library.Mission.Segments.Transition
    RCAIDE.Framework.Mission.Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb
    """
    
    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes transition maneuver evaluation with
        constant acceleration and pitch rate constraints while maintaining
        constant altitude. Prop-rotor pitch command is automatically
        applied linearly throughout the segment.
        """           
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude                     = None
        self.acceleration                 = 1.  * Units['m/s/s']
        self.air_speed_start              = None
        self.air_speed_end                = 1.0 * Units['m/s']        
        self.pitch_initial                = None
        self.pitch_final                  = 0.0 * Units['rad']   
        self.true_course                  = 0.0 * Units.degrees   
         
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------          
        initialize                         = self.process.initialize 
        initialize.conditions              = Segments.Transition.Constant_Acceleration_Constant_Pitchrate_Constant_Altitude.initialize_conditions      
        iterate                            = self.process.iterate    
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return