# RCAIDE/Framework/Mission/Segments/Climb/Constant_Mach_Constant_Rate.py
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
# Constant_Mach_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Mach_Constant_Rate(Evaluate):
    """
    Mission segment for climbing at constant Mach number and constant rate

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_rate : float
        Rate of climb [m/s], defaults to 3 m/s
    mach_number : float
        Mach number to maintain, defaults to 0.7
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant Mach number while climbing at a fixed rate.
    The true airspeed will increase with altitude to maintain constant Mach
    number as the speed of sound changes with atmospheric conditions.

    The segment processes include:
    - Altitude differential initialization
    - Mach climb conditions initialization
    - Control surface unpacking
    - Orientation unpacking
    - Flight dynamics residual evaluation

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Mach number achievable throughout climb
    * Sufficient thrust available for climb rate

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (Mach climb)

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
        self.mach_number       = 0.7 
        self.true_course       = 0.0 * Units.degrees         
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Mach_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics

        return

