# RCAIDE/Framework/Mission/Segments/Climb/Constant_Speed_Linear_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                                     import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Linear_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Speed_Linear_Altitude(Evaluate):
    """
    Mission segment for climbing at constant true airspeed with linear altitude change

    Attributes
    ----------
    air_speed : float
        True airspeed to maintain [m/s], defaults to 10 km/hr
    distance : float
        Ground distance to cover [m], defaults to 10 km
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], optional
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant true airspeed while linearly varying altitude
    over a specified ground distance. The climb/descent rate varies to achieve
    the linear altitude profile while maintaining constant airspeed.

    The segment processes include:
    - Altitude differential initialization
    - Constant speed climb conditions initialization
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Airspeed achievable throughout altitude range
    * Linear altitude change achievable with available thrust
    * Ground track follows true course

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (constant speed linear altitude)

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
        self.air_speed         = 10. * Units['km/hr']
        self.distance          = 10. * Units.km
        self.altitude_start    = None
        self.altitude_end      = None
        self.true_course       = 0.0 * Units.degrees     
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Speed_Linear_Altitude.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        return