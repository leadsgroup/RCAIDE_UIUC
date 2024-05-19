## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Framework/Analyses/Mission/Segments/Climb/Linear_Mach_Constant_Rate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                                     import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Methods.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Linear_Mach_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Climb
class Linear_Mach_Constant_Rate(Evaluate):
    """ Linearly change mach number while climbing at a constant rate.
    
        Assumptions:
        None
        
        Source:
        None
    """         
    
    def __defaults__(self):
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_rate        = 3.  * Units.m / Units.s
        self.mach_number_end   = 0.7
        self.mach_number_start = 0.8
        self.true_course_angle = 0.0 * Units.degrees    
      
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Linear_Mach_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.flight_dynamics  = Common.Residuals.climb_descent_flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   
        
        return

