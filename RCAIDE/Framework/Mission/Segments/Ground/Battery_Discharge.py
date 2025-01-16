# RCAIDE/Framework/Mission/Segments/Ground/Battery_Disharge.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Mission.Segments.Evaluate        import Evaluate    
from RCAIDE.Framework.Core                                      import Units
from RCAIDE.Library.Mission.Segments                  import Ground  
from RCAIDE.Library.Methods.skip                              import skip 

# ----------------------------------------------------------------------------------------------------------------------
#  SEGMENT
# ----------------------------------------------------------------------------------------------------------------------
class Battery_Discharge(Evaluate):
    """
    Mission segment for discharging battery while vehicle is on ground

    Attributes
    ----------
    altitude : float
        Ground altitude [m], required
    time : float
        Duration of discharge [s], defaults to 1.0 s
    cooling_time : float
        Additional time for battery cooling [s], defaults to 0.0 s
    overcharge_contingency : float
        Safety factor for discharge capacity, defaults to 1.10
    true_course : float
        True course angle [rad], defaults to 0 degrees

    Notes
    -----
    This segment simulates battery discharge while the vehicle is stationary
    on the ground. Useful for pre-flight systems checks or ground operations.
    Aerodynamic and stability calculations are skipped since the vehicle is
    stationary.

    The segment processes include:
    - Ground battery discharge conditions initialization
    - Energy state tracking
    - Battery thermal management

    **Major Assumptions**
    * Vehicle is stationary
    * No aerodynamic forces
    * Constant discharge rate
    * Battery thermal limits maintained
    * Ground support equipment available if needed

    **Process Flow**
    
    Initialize:
    - conditions (battery discharge)

    Iterate:
    - unknowns.mission (skipped)
    - conditions.aerodynamics (skipped)
    - conditions.stability (skipped)

    Post Process:
    - noise (skipped)
    - emissions (skipped)

    See Also
    --------
    RCAIDE.Framework.Mission.Segments.Evaluate
    RCAIDE.Library.Mission.Segments.Ground
    """

    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  

    def __defaults__(self):
        """
        Sets default values for segment parameters

        Notes
        -----
        Initializes segment with default values and sets up process flow.
        Called automatically when segment is instantiated.

        The process flow skips aerodynamic and stability calculations since
        the vehicle is stationary on the ground.
        """
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude               = None
        self.time                   = 1.0 * Units.seconds 
        self.cooling_time           = 0.0 * Units.seconds
        self.overcharge_contingency = 1.10 
        self.true_course            = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------       
        initialize                         = self.process.initialize 
        initialize.conditions              = Ground.Battery_Charge_Discharge.initialize_conditions 
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = skip
        iterate.conditions.aerodynamics    = skip
        iterate.conditions.stability       = skip  
        post_process                       = self.process.post_process  
        post_process.noise                 = skip
        post_process.emissions             = skip
        
        return
