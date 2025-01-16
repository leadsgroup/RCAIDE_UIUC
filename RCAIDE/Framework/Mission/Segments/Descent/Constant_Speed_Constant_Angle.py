# RCAIDE/Framework/Mission/Segments/Descent/Constant_Speed_Constant_Angle.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
from RCAIDE.Framework.Core                                 import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------  
#  Constant_Speed_Constant_Angle
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_Speed_Constant_Angle(Evaluate):
    """
    Mission segment for descending at constant true airspeed and flight path angle

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 0 km
    descent_angle : float
        Flight path angle [rad], defaults to 3 degrees
        Positive angles indicate descent
    air_speed : float
        True airspeed to maintain [m/s], defaults to 100 m/s
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant true airspeed while descending at a fixed
    flight path angle. Unlike rate-based descent segments, the descent rate
    will vary with true airspeed according to the specified angle. The true
    airspeed remains constant regardless of atmospheric conditions.

    The segment processes include:
    - Altitude differential initialization
    - Constant speed/angle descent conditions initialization
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Airspeed achievable throughout descent
    * Sufficient control authority
    * Constant flight path angle maintainable

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (constant speed/angle descent)

    Iterate:
    - residuals.flight_dynamics
    - unknowns.mission (orientation)

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
        1. Initialize altitude differentials and conditions
        2. Iterate on flight dynamics and orientation
        """
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 0.0 * Units.km
        self.descent_angle     = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course       = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Descent.Constant_Speed_Constant_Angle.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation          
        return

