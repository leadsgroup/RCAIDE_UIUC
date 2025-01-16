# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Speed_Constant_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                                 import Units   
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

class Constant_Speed_Constant_Altitude(Evaluate):
    """
    Mission segment for cruising at constant true airspeed and altitude

    Attributes
    ----------
    altitude : float
        Constant altitude to maintain [m], required
    air_speed : float
        True airspeed to maintain [m/s], required
    distance : float
        Ground distance to cover [m], defaults to 10 km
    true_course : float
        True course angle [rad], defaults to 0 degrees
    bank_angle : float
        Bank angle [rad], defaults to 0 degrees

    Notes
    -----
    This is the most basic cruise segment, maintaining constant altitude and
    true airspeed while covering a specified ground distance. Most other cruise
    segments are derived from this fundamental segment. The true airspeed remains
    constant regardless of atmospheric conditions.

    The segment processes include:
    - Constant altitude/speed conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Airspeed achievable at altitude
    * Sufficient thrust available
    * Constant altitude maintainable

    **Process Flow**
    
    Initialize:
    - conditions (constant speed cruise)

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
        1. Initialize conditions
        2. Iterate on orientation, controls and flight dynamics
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = None
        self.air_speed         = None
        self.distance          = 10. * Units.km
        self.true_course       = 0.0 * Units.degrees
        self.bank_angle        = 0.0 * Units.degrees

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Speed_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate   
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
 
        return

