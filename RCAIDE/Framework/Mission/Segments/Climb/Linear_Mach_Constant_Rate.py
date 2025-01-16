# RCAIDE/Framework/Mission/Segments/Climb/Linear_Mach_Constant_Rate.py
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
#  Linear_Mach_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 
class Linear_Mach_Constant_Rate(Evaluate):
    """
    Mission segment for climbing at constant rate with linear Mach number variation

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_rate : float
        Rate of climb [m/s], defaults to 3 m/s
    mach_number_start : float
        Initial Mach number, defaults to 0.8
    mach_number_end : float
        Final Mach number, defaults to 0.7
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains a constant climb rate while linearly varying the
    Mach number between specified start and end values. The true airspeed
    will vary both due to the Mach number change and the variation in speed
    of sound with altitude.

    The segment processes include:
    - Altitude differential initialization
    - Linear Mach climb conditions initialization
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Linear Mach variation achievable
    * Sufficient thrust available throughout Mach range
    * Constant climb rate maintainable

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (linear Mach climb)

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
        self.altitude_end      = 10. * Units.km
        self.climb_rate        = 3.  * Units.m / Units.s
        self.mach_number_end   = 0.7
        self.mach_number_start = 0.8
        self.true_course       = 0.0 * Units.degrees    
      
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Linear_Mach_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   
        
        return

