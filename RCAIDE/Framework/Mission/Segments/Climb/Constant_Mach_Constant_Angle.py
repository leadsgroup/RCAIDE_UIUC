# RCAIDE/Framework/Mission/Segments/Climb/Constant_Mach_Constant_Angle.py
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
# Constant_Mach_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Mach_Constant_Angle(Evaluate):
    """
    Mission segment for climbing at constant Mach number and constant angle

    Attributes
    ----------
    altitude_start : float
        Initial altitude [m], optional
    altitude_end : float
        Final altitude [m], defaults to 10 km
    climb_angle : float
        Climb angle [rad], defaults to 3 degrees
    mach_number : float
        Mach number to maintain
    true_course : float
        True course angle [rad], defaults to 0 degrees

    state.unknowns.altitude : ndarray
        Altitude values to be solved
    state.residuals.altitude : ndarray
        Altitude constraint residuals

    Notes
    -----
    This segment maintains constant Mach number while climbing at a fixed angle.
    It requires additional computation time due to extra unknowns and residuals
    for maintaining Mach number with changing atmospheric conditions.

    The segment processes include:
    - Altitude differential initialization
    - Mach climb conditions initialization
    - Flight dynamics residual evaluation
    - Differential updates
    - Orientation and control surface updates
    - Kinematics calculations

    **Major Assumptions**
    * Standard atmosphere
    * Quasi-steady flight
    * No wind effects
    * Mach number achievable throughout climb
    * Sufficient thrust available for climb angle

    **Process Flow**
    
    Initialize:
    - differentials_altitude
    - conditions (Mach climb)

    Iterate:
    - residuals.flight_dynamics (total forces)
    - conditions.differentials
    - unknowns.mission (orientation)
    - unknowns.controls (control surfaces)
    - unknowns.kinematics

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
        2. Iterate on flight dynamics, differentials, and kinematics
        3. Update orientation and control surfaces
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_angle       = 3.  * Units.deg
        self.mach_number       = None
        self.true_course       = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Unique Mission Unknowns and Residuals
        # --------------------------------------------------------------------------------------------------------------  
        ones_row = self.state.ones_row        
        self.state.unknowns.altitude   = ones_row(1) * 0.0   
        self.state.residuals.altitude  = ones_row(1) * 0.0   
    
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Mach_Constant_Angle.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.flight_dynamics  = Segments.Climb.Constant_Mach_Constant_Angle.residual_total_forces
        iterate.conditions.differentials   = Segments.Climb.Constant_Mach_Constant_Angle.update_differentials 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.kinematics        = Segments.Climb.Constant_Mach_Constant_Angle.initialize_conditions
          
        return

