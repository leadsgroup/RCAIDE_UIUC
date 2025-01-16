# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Acceleration_Constant_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                                 import Units   
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 

class Constant_Acceleration_Constant_Altitude(Evaluate):
    """
    Mission segment for accelerating at constant rate while maintaining altitude

    Attributes
    ----------
    altitude : float
        Constant altitude to maintain [m], required
    acceleration : float
        Acceleration rate [m/s^2], defaults to 1 m/s^2
    air_speed_start : float
        Initial true airspeed [m/s], required
    air_speed_end : float
        Final true airspeed [m/s], defaults to 1 m/s
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant altitude while accelerating at a fixed rate
    between specified airspeeds. The segment duration is determined by the
    acceleration rate and speed change required.

    The segment processes include:
    - Constant altitude conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Sufficient thrust available for acceleration
    * Altitude can be maintained during acceleration
    * Constant acceleration achievable

    **Process Flow**
    
    Initialize:
    - conditions (constant altitude acceleration)

    Iterate:
    - unknowns.mission (orientation)
    - unknowns.controls (control surfaces)
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow defines how the segment is evaluated:
        1. Initialize conditions
        2. Iterate on orientation, controls and flight dynamics
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = None
        self.acceleration      = 1.  * Units['m/s/s']
        self.air_speed_start   = None
        self.air_speed_end     = 1.0 * Units['m/s']
        self.true_course       = 0.0 * Units.degrees       
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize 
        initialize.conditions              = Segments.Cruise.Constant_Acceleration_Constant_Altitude.initialize_conditions       
        iterate                            = self.process.iterate  
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

