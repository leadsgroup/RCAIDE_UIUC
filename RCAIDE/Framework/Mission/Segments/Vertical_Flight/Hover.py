# RCAIDE/Framework/Mission/Segments/Vertical_Flight/Hover.py
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
#  Hover
# ---------------------------------------------------------------------------------------------------------------------- 
class Hover(Evaluate):
    """
    Mission segment for stationary hover in VTOL aircraft

    Attributes
    ----------
    altitude : float
        Hover altitude [m], required
    time : float
        Duration of hover [s], defaults to 1.0 s
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment simulates a stationary hover for VTOL aircraft where the
    vehicle maintains a fixed position in space. Aerodynamic forces are
    considered negligible due to zero translational velocity. Typically
    used for multicopter or helicopter operations like precision hover,
    payload operations, or transition preparation.

    The segment processes include:
    - Hover conditions initialization
    - Flight dynamics evaluation
    - Power and thrust calculations
    - Energy consumption tracking

    **Major Assumptions**
    * Zero translational velocity
    * Negligible aerodynamic forces
    * Thrust exactly counters weight
    * No wind effects
    * Perfect position hold
    * Quasi-steady state
    * Constant altitude
    * No ground effect

    **Process Flow**
    
    Initialize:
    - conditions (hover)

    Iterate:
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Common
    RCAIDE.Library.Mission.Segments.Vertical_Flight
    RCAIDE.Framework.Mission.Segments.Vertical_Flight.Climb
    RCAIDE.Framework.Mission.Segments.Vertical_Flight.Descent
    """

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow includes hover flight dynamics evaluation
        with focus on thrust and power requirements for maintaining
        stationary flight.
        """
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        
        self.altitude           = None
        self.time               = 1.0 * Units.seconds
        self.true_course        = 0.0 * Units.degrees            
             
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize
        iterate                            = self.process.iterate 
        initialize.conditions              = Segments.Vertical_Flight.Hover.initialize_conditions
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

