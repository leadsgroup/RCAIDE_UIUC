# RCAIDE/Framework/Mission/Segments/Descent/Constant_EAS_Constant_Rate.py
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
#  Constant_EAS_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_EAS_Constant_Rate(Evaluate):
    """
    Mission segment for descending at constant equivalent airspeed and rate

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    descent_rate : float
        Rate of descent [m/s], defaults to 3 m/s
    equivalent_air_speed : float
        Equivalent airspeed to maintain [m/s], defaults to 100 m/s
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant equivalent airspeed (EAS) while descending
    at a fixed rate. The true airspeed will vary with altitude to maintain
    constant EAS as atmospheric density changes. Unlike CAS, EAS accounts for
    compressibility effects.

    The segment processes include:
    - Altitude differential initialization
    - EAS descent conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * EAS achievable throughout descent
    * Sufficient control authority
    * Constant descent rate maintainable

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (EAS descent)

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
        self.altitude_start       = None # Optional
        self.altitude_end         = 10. * Units.km
        self.descent_rate         = 3.  * Units.m / Units.s
        self.equivalent_air_speed = 100 * Units.m / Units.s
        self.true_course          = 0.0 * Units.degrees      
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Descent.Constant_EAS_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics

        return
       