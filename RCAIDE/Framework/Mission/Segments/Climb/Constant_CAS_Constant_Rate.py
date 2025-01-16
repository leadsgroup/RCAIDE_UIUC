# RCAIDE/Framework/Mission/Segments/Climb/Constant_CAS_Constant_Rate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                                   import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate              import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant CAS Constant Rate
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_CAS_Constant_Rate(Evaluate):
    """
    Mission segment for constant calibrated airspeed climb at constant rate

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_rate : float
        Rate of climb [m/s], defaults to 3 m/s
    calibrated_air_speed : float
        Calibrated airspeed [m/s]
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains a constant calibrated airspeed (CAS) while climbing
    at a specified rate. The true airspeed will vary with altitude to maintain
    constant CAS.

    The segment processes include:
    - Altitude differential initialization
    - CAS climb conditions initialization
    - Control surface unpacking
    - Orientation unpacking
    - Flight dynamics residual evaluation

    **Major Assumptions**
    * Standard atmosphere
    * Constant climb rate achievable
    * No wind effects
    * Quasi-steady flight

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (CAS climb)
    
    Iterate:
    - unknowns.controls
    - unknowns.mission
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
        2. Iterate on controls, orientation and flight dynamics
        """  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start       = None # Optional
        self.altitude_end         = 10. * Units.km
        self.climb_rate           = 3.  * Units.m / Units.s
        self.calibrated_air_speed = None
        self.true_course          = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_CAS_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return
       
