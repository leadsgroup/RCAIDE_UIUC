# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Pitch_Rate_Constant_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                                 import Units   
from RCAIDE.Library.Mission.Segments             import Cruise
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Pitch_Rate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

class Constant_Pitch_Rate_Constant_Altitude(Evaluate):
    """
    Mission segment for maneuvering at constant pitch rate while maintaining altitude

    Attributes
    ----------
    altitude : float
        Constant altitude to maintain [m], required
    pitch_rate : float
        Rate of pitch change [rad/s^2], defaults to 1 rad/s^2
    pitch_initial : float
        Initial pitch angle [rad], required
    pitch_final : float
        Final pitch angle [rad], defaults to 0 rad
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant altitude while executing a pitch maneuver
    at a fixed rate. Primarily used for VTOL aircraft transitions between
    different pitch attitudes. The segment duration is determined by the
    pitch rate and total pitch angle change required.

    The segment processes include:
    - Constant altitude conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Sufficient control authority for pitch maneuver
    * Altitude can be maintained during pitch change
    * Constant pitch rate achievable

    **Process Flow**
    
    Initialize:
    - conditions (constant pitch rate maneuver)

    Iterate:
    - unknowns.mission (orientation)
    - unknowns.controls (control surfaces)
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    RCAIDE.Library.Mission.Segments.Cruise
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
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = None
        self.pitch_rate        = 1.  * Units['rad/s/s']
        self.pitch_initial     = None
        self.pitch_final       = 0.0 * Units['rad']
        self.true_course       = 0.0 * Units.degrees  
 
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------       
        initialize                         = self.process.initialize  
        initialize.conditions              = Cruise.Constant_Pitch_Rate_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return

