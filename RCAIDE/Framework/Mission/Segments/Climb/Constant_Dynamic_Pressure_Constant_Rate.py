# RCAIDE/Framework/Mission/Segments/Climb/Constant_Dynamic_Pressure_Constant_Rate.py
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
#  Constant_Dynamic_Pressure_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Dynamic_Pressure_Constant_Rate(Evaluate):
    """
    Mission segment for climbing at constant dynamic pressure and constant rate

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_rate : float
        Rate of climb [m/s], defaults to 3 m/s
    dynamic_pressure : float
        Dynamic pressure to maintain [Pa]
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant dynamic pressure while climbing at a fixed rate.
    The true airspeed will vary with altitude to maintain the specified dynamic
    pressure as atmospheric density changes.

    The segment processes include:
    - Altitude differential initialization
    - Dynamic pressure climb conditions initialization
    - Orientation unpacking
    - Total forces residual evaluation

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Dynamic pressure achievable throughout climb
    * Sufficient thrust available for climb rate

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (dynamic pressure climb)

    Iterate:
    - residuals.total_forces (climb/descent forces)
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
        2. Iterate on total forces and orientation
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_rate        = 3.  * Units.m / Units.s
        self.dynamic_pressure  = None
        self.true_course       = 0.0 * Units.degrees               
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Dynamic_Pressure_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation           
    
        return
       