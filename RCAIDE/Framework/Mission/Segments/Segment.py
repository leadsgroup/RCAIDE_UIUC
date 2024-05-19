## @ingroup Analyses-Mission-Segments
# RCAIDE/Framework/Analyses/Mission/Segment/Segment.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE Imports
from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses                    import Analysis, Settings, Process   
from RCAIDE.Framework.Mission.Common     import State 

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSES
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Mission-Segments
class Segment(Analysis):
    """ 
    """    
    
    def __defaults__(self):
        """This sets the default values.
    
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
        
        self.settings                      = Settings() 
        self.state                         = State() 
        self.analyses                      = Analysis.Container() 
        self.process                       = Process() 
        self.process.initialize            = Process()
          
        self.process.converge              = Process()
        self.process.iterate               = Process()
        self.process.iterate.unknowns      = Process()
        self.process.iterate.initials      = Process()
        self.process.iterate.conditions    = Process()
        self.process.iterate.residuals     = Process()
        self.process.post_process          = Process()  
        
        self.conditions = self.state.conditions 
        
        return
    
    def initialize(self):
        """ This executes the initialize process
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State  [Data()]
    
            Outputs:
            None
    
            Properties Used:
            None
        """        
        self.process.initialize(self)
        return
    
    def converge(self,state):
        """ This executes the converge process
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State  [Data()]
    
            Outputs:
            None
    
            Properties Used:
            None
        """             
        self.process.converge(self,state)    
    
    def iterate(self):
        """ This executes the iterate process
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State  [Data()]
    
            Outputs:
            None
    
            Properties Used:
            None
        """        
        self.process.iterate(self)
        return
    
    def post_process(self):
        """ This executes post processing
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State  [Data()]
    
            Outputs:
            None
    
            Properties Used:
            None
        """         
        self.process.post_process(self)
        return
    
    def evaluate(self,state=None):
        """ This executes the entire process
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State  [Data()]
    
            Outputs:
            State  [Data()]
    
            Properties Used:
            None
        """          
        if state is None:
            state = self.state
        self.process(self)
        return self
    
    def flight_dynamics_and_controls(self): 
        self.flight_dynamics                                             = Data()
        self.flight_dynamics.force_x                                     = False 
        self.flight_dynamics.force_y                                     = False 
        self.flight_dynamics.force_z                                     = False 
        self.flight_dynamics.moment_x                                    = False 
        self.flight_dynamics.moment_y                                    = False 
        self.flight_dynamics.moment_z                                    = False    
        
        self.flight_controls                                              = Data() 
        
        self.flight_controls.body_angle                                   = Data()
        self.flight_controls.body_angle.active                            = False                 
        self.flight_controls.body_angle.initial_guess                     = False             
        self.flight_controls.body_angle.initial_guess_values              = None

        self.flight_controls.bank_angle                                   = Data()
        self.flight_controls.bank_angle.active                            = False
        self.flight_controls.bank_angle.initial_guess                     = False
        self.flight_controls.bank_angle.initial_guess_values              = None

        self.flight_controls.wind_angle                                   = Data()
        self.flight_controls.wind_angle.active                            = False                 
        self.flight_controls.wind_angle.initial_guess                     = False           
        self.flight_controls.wind_angle.initial_guess_values              = None   

        self.flight_controls.elapsed_time                                 = Data()
        self.flight_controls.elapsed_time.active                          = False                 
        self.flight_controls.elapsed_time.initial_guess                   = False               
        self.flight_controls.elapsed_time.initial_guess_values            = None  
    
        self.flight_controls.velocity                                     = Data()
        self.flight_controls.velocity.active                              = False                 
        self.flight_controls.velocity.initial_guess                       = False                
        self.flight_controls.velocity.initial_guess_values                = None
        
        self.flight_controls.acceleration                                 = Data()
        self.flight_controls.acceleration.active                          = False                 
        self.flight_controls.acceleration.initial_guess                   = False                
        self.flight_controls.acceleration.initial_guess_values            = None
        
        self.flight_controls.altitude                                     = Data()
        self.flight_controls.altitude.active                              = False                 
        self.flight_controls.altitude.initial_guess                       = False               
        self.flight_controls.altitude.initial_guess_values                = None
    
        self.flight_controls.throttle                                     = Data() 
        self.flight_controls.throttle.active                              = False                
        self.flight_controls.throttle.assigned_propulsors                 = None      
        self.flight_controls.throttle.initial_guess                       = False    
        self.flight_controls.throttle.initial_guess_values                = None
    
        self.flight_controls.elevator_deflection                          = Data() 
        self.flight_controls.elevator_deflection.active                   = False      
        self.flight_controls.elevator_deflection.assigned_surfaces        = None
        self.flight_controls.elevator_deflection.initial_guess            = False 
        self.flight_controls.elevator_deflection.initial_guess_values     = None

        self.flight_controls.rudder_deflection                            = Data()
        self.flight_controls.rudder_deflection.active                     = False
        self.flight_controls.rudder_deflection.assigned_surfaces          = None
        self.flight_controls.rudder_deflection.initial_guess              = False
        self.flight_controls.rudder_deflection.initial_guess_values       = None

        self.flight_controls.flap_deflection                              = Data() 
        self.flight_controls.flap_deflection.active                       = False          
        self.flight_controls.flap_deflection.assigned_surfaces            = None
        self.flight_controls.flap_deflection.initial_guess                = False 
        self.flight_controls.flap_deflection.initial_guess_values         = None

        self.flight_controls.slat_deflection                              = Data() 
        self.flight_controls.slat_deflection.active                       = False          
        self.flight_controls.slat_deflection.assigned_surfaces            = None
        self.flight_controls.slat_deflection.initial_guess                = False 
        self.flight_controls.slat_deflection.initial_guess_values         = None            
    
        self.flight_controls.aileron_deflection                           = Data() 
        self.flight_controls.aileron_deflection.active                    = False      
        self.flight_controls.aileron_deflection.assigned_surfaces         = None
        self.flight_controls.aileron_deflection.initial_guess             = False 
        self.flight_controls.aileron_deflection.initial_guess_false       = None
    
        self.flight_controls.thrust_vector_angle                          = Data() 
        self.flight_controls.thrust_vector_angle.active                   = False        
        self.flight_controls.thrust_vector_angle.assigned_propulsors      = None
        self.flight_controls.thrust_vector_angle.initial_guess            = False 
        self.flight_controls.thrust_vector_angle.initial_guess_values     = None
    
        self.flight_controls.blade_pitch_angle                            = Data() 
        self.flight_controls.blade_pitch_angle.active                     = False          
        self.flight_controls.blade_pitch_angle.assigned_propulsors        = None
        self.flight_controls.blade_pitch_angle.initial_guess              = False 
        self.flight_controls.blade_pitch_angle.initial_guess_values       = None
    
        self.flight_controls.RPM                                          = Data() 
        self.flight_controls.RPM.active                                   = False              
        self.flight_controls.RPM.assigned_propulsors                      = None
        self.flight_controls.RPM.initial_guess                            = False 
        self.flight_controls.RPM.initial_guess_values                     = None
    
        return     
           
# ----------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments
class Container(Segment):
    """ A container for the segment
    
        Assumptions:
        None
        
        Source:
        None
    """    
    
    def __defaults__(self):
        """This sets the default values.
    
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
                
        self.segments = Process()
        
        self.state = State.Container()
        
    def append_segment(self,segment):
        """ Add a SubSegment
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment  [Segment()]
    
            Outputs:
            None
    
            Properties Used:
            None
        """          
        self.segments.append(segment)
        return    
        
Segment.Container = Container