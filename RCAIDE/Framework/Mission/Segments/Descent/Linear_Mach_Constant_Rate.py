# RCAIDE/Framework/Mission/Segments/Descent/Linear_Mach_Constant_Rate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Framework.Core                                 import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------  
#  Linear_Mach_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------  
class Linear_Mach_Constant_Rate(Evaluate):
    """
    Mission segment for descending at constant rate with linear Mach variation

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    descent_rate : float
        Rate of descent [m/s], defaults to 3 m/s
    mach_start : float
        Initial Mach number, required
    mach_end : float
        Final Mach number, required
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains a constant descent rate while linearly varying the
    Mach number between specified start and end values. The true airspeed will
    vary both due to the Mach number change and atmospheric conditions during
    descent.

    The segment processes include:
    - Altitude differential initialization
    - Linear Mach descent conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Mach range achievable throughout descent
    * Sufficient control authority
    * Constant descent rate maintainable
    * Linear Mach variation achievable

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (linear Mach descent)

    Iterate:
    - unknowns.controls (control surfaces)
    - residuals.flight_dynamics
    - unknowns.mission (orientation)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    RCAIDE.Framework.Mission.Segments.Descent.Constant_Speed_Constant_Rate
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
        2. Iterate on controls, flight dynamics and orientation
        """            
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.descent_rate      = 3.  * Units.m / Units.s
        self.mach_number_end   = 0.7
        self.mach_number_start = None
        self.true_course       = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Descent.Linear_Mach_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics

        return

