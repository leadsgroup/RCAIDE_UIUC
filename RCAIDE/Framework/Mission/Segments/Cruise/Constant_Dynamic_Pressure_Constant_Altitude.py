# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Dynamic_Pressure_Constant_Altitude.py
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
#  Constant_Dynamic_Pressure_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

class Constant_Dynamic_Pressure_Constant_Altitude(Evaluate):
    """
    Mission segment for cruising at constant dynamic pressure and altitude

    Attributes
    ----------
    altitude : float
        Constant altitude to maintain [m], defaults to 0.0
    dynamic_pressure : float
        Dynamic pressure to maintain [Pa], required
    distance : float
        Ground distance to cover [m], defaults to 1 km
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment maintains constant altitude and dynamic pressure while covering
    a specified ground distance. The true airspeed will vary with atmospheric
    density to maintain constant dynamic pressure. Based on constant speed
    constant altitude segment framework.

    The segment processes include:
    - Constant altitude/dynamic pressure conditions initialization
    - Control surface unpacking
    - Flight dynamics residual evaluation
    - Orientation unpacking

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Dynamic pressure achievable at altitude
    * Sufficient thrust available
    * Constant altitude maintainable

    **Process Flow**
    
    Initialize:
    - conditions (constant dynamic pressure cruise)

    Iterate:
    - unknowns.controls (control surfaces)
    - unknowns.mission (orientation)
    - residuals.flight_dynamics

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Framework.Mission.Common
    RCAIDE.Framework.Mission.Segments.Cruise.Constant_Speed_Constant_Altitude
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
        2. Iterate on controls, orientation and flight dynamics
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = 0.0
        self.dynamic_pressure  = None  
        self.distance          = 1.0 * Units.km
        self.true_course       = 0.0 * Units.degrees              
    
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Dynamic_Pressure_Constant_Altitude.initialize_conditions 
        iterate                            = self.process.iterate   
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics

        return

