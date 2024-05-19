## @ingroup Analyses-Aerodynamics
# RCAIDE/Framework/Analyses/Aerodynamics/Subsonic_VLM.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                             import Data, Units
from RCAIDE.Framework.Analyses                         import Process 
from RCAIDE.Library.Methods.Aerodynamics               import Common
from .Aerodynamics                                     import Aerodynamics 
from RCAIDE.Framework.Analyses.Common.Process_Geometry import Process_Geometry 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method.VLM_Aerodynamics import *  

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Subsonic_VLM
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics
class Subsonic_VLM(Aerodynamics):
    """This is a subsonic aerodynamic buildup analysis based on the vortex lattice method

     Assumptions:
     Stall effects are negligible 
 
     Source:
     N/A
 
     Inputs:
     None
 
     Outputs:
     None
 
     Properties Used:
     N/A 
    """      
    
    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """          
        self.tag                                    = 'Subsonic_Zero_VLM'  
        self.geometry                               = Data()  
        self.process                                = Process()
        self.process.initialize                     = Process()   
        
        # correction factors
        settings                                    = self.settings
        settings.fuselage_lift_correction           = 1.14
        settings.trim_drag_correction_factor        = 1.02
        settings.wing_parasite_drag_form_factor     = 1.1
        settings.fuselage_parasite_drag_form_factor = 2.3
        settings.maximum_lift_coefficient_factor    = 1.0        
        settings.lift_to_drag_adjustment            = 0.  
        settings.oswald_efficiency_factor           = None
        settings.span_efficiency                    = None
        settings.viscous_lift_dependent_drag_factor = 0.38
        settings.drag_coefficient_increment         = 0.0000
        settings.spoiler_drag_increment             = 0.00 
        settings.maximum_lift_coefficient           = np.inf 
        settings.use_surrogate                      = True
        settings.recalculate_total_wetted_area      = False
        settings.propeller_wake_model               = False 
        settings.discretize_control_surfaces        = False
        settings.model_fuselage                     = False
        settings.model_nacelle                      = False
        
      
        self.settings.number_of_spanwise_vortices        = 15
        self.settings.number_of_chordwise_vortices       = 5
        self.settings.wing_spanwise_vortices          = None
        self.settings.wing_chordwise_vortices         = None
        self.settings.fuselage_spanwise_vortices      = None
        self.settings.fuselage_chordwise_vortices     = None  
        self.settings.spanwise_cosine_spacing         = True
        self.settings.vortex_distribution             = Data()  
        self.settings.leading_edge_suction_multiplier = 1.0  
        self.settings.use_VORLAX_matrix_calculation   = False
        self.settings.floating_point_precision        = np.float32 
    
        # conditions table, used for surrogate model training
        self.training                                = Data()
        self.training.angle_of_attack                = np.array([[-5., -2. , 0.0 , 2.0, 5.0, 8.0, 10.0 , 12., 45., 75.]]).T * Units.deg 
        self.training.Mach                           = np.array([[0.0, 0.1  , 0.2 , 0.3,  0.5,  0.75 , 0.85 , 0.9,\
                                                                      1.3, 1.35 , 1.5 , 2.0, 2.25 , 2.5  , 3.0  , 3.5]]).T       
    
        self.training.lift_coefficient_sub           = None
        self.training.lift_coefficient_sup           = None
        self.training.wing_lift_coefficient_sub      = None
        self.training.wing_lift_coefficient_sup      = None
        self.training.drag_coefficient_sub           = None
        self.training.drag_coefficient_sup           = None
        self.training.wing_drag_coefficient_sub      = None
        self.training.wing_drag_coefficient_sup      = None
    
        # blending function 
        self.hsub_min                                = 0.85
        self.hsub_max                                = 0.95
        self.hsup_min                                = 1.05
        self.hsup_max                                = 1.25 
    
        # surrogoate models
        self.surrogates                              = Data() 
        self.surrogates.lift_coefficient_sub         = None
        self.surrogates.lift_coefficient_sup         = None
        self.surrogates.lift_coefficient_trans       = None
        self.surrogates.wing_lift_coefficient_sub    = None
        self.surrogates.wing_lift_coefficient_sup    = None
        self.surrogates.wing_lift_coefficient_trans  = None
        self.surrogates.drag_coefficient_sub         = None
        self.surrogates.drag_coefficient_sup         = None
        self.surrogates.drag_coefficient_trans       = None
        self.surrogates.wing_drag_coefficient_sub    = None
        self.surrogates.wing_drag_coefficient_sup    = None
        self.surrogates.wing_drag_coefficient_trans  = None  
        

        

    def initialize(self):  
        use_surrogate             = self.settings.use_surrogate  

        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            sample_training(self)

            # build surrogate
            build_surrogate(self)  
    
        # build the evaluation process
        compute                                    = Process() 
        compute.lift                               = Process()
        if use_surrogate == True: 
            compute.lift.inviscid_wings                = evaluate_surrogate
        else:
            compute.lift.inviscid_wings  = evaluate_no_surrogate
        compute.lift.vortex                        = RCAIDE.Library.Methods.skip
        compute.lift.fuselage                      = Common.Lift.fuselage_correction
        compute.lift.total                         = Common.Lift.aircraft_total  
        compute.drag                               = Process()
        compute.drag.parasite                      = Process()
        compute.drag.parasite.wings                = Process_Geometry('wings')
        compute.drag.parasite.wings.wing           = Common.Drag.parasite_drag_wing 
        compute.drag.parasite.fuselages            = Process_Geometry('fuselages')
        compute.drag.parasite.fuselages.fuselage   = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.booms                = Process_Geometry('booms')
        compute.drag.parasite.booms.boom           = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.nacelles             = Process_Geometry('nacelles')
        compute.drag.parasite.nacelles.nacelle     = Common.Drag.parasite_drag_nacelle
        compute.drag.parasite.pylons               = Common.Drag.parasite_drag_pylon
        compute.drag.parasite.total                = Common.Drag.parasite_total
        compute.drag.induced                       = Common.Drag.induced_drag_aircraft
        compute.drag.compressibility               = Process()
        compute.drag.compressibility.wings         = Process_Geometry('wings')
        compute.drag.compressibility.wings.wing    = Common.Drag.compressibility_drag_wing
        compute.drag.compressibility.total         = Common.Drag.compressibility_drag_wing_total
        compute.drag.miscellaneous                 = Common.Drag.miscellaneous_drag_aircraft_ESDU
        compute.drag.untrimmed                     = Common.Drag.untrimmed
        compute.drag.trim                          = Common.Drag.trim
        compute.drag.spoiler                       = Common.Drag.spoiler_drag
        compute.drag.total                         = Common.Drag.total_aircraft 
        self.process.compute                       = compute            

        return 
    
         
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <RCAIDE data class>

        Properties Used:
        self.settings
        self.geometry
        """          
        settings = self.settings
        geometry = self.geometry 
        results  = self.process.compute(state,settings,geometry)
        
        return results