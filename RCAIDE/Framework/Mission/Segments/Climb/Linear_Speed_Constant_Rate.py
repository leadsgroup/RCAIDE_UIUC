# RCAIDE/Framework/Mission/Segments/Climb/Linear_Speed_Constant_Rate.py
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
#  Linear_Speed_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------
class Linear_Speed_Constant_Rate(Evaluate):
    """
    Mission segment for climbing at constant rate with linear true airspeed variation

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_rate : float
        Rate of climb [m/s], defaults to 3 m/s
    air_speed_start : float
        Initial true airspeed [m/s], required
    air_speed_end : float
        Final true airspeed [m/s], defaults to 200 m/s
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains a constant climb rate while linearly varying the
    true airspeed between specified start and end values. Unlike Mach-based
    segments, the true airspeed variation is independent of atmospheric
    conditions.

    The segment processes include:
    - Altitude differential initialization
    - Linear speed climb conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Linear speed variation achievable
    * Sufficient thrust available throughout speed range
    * Constant climb rate maintainable

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (linear speed climb)

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
        1. Initialize altitude differentials and conditions
        2. Iterate on orientation, controls and flight dynamics
        """
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_rate        = 3.  * Units.m / Units.s
        self.air_speed_start   = None
        self.air_speed_end     = 200 * Units.m / Units.s
        self.true_course       = 0.0 * Units.degrees    
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Linear_Speed_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

