# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis  

# ----------------------------------------------------------------------
#  Analysis
# ---------------------------------------------------------------------- 
class Weights(Analysis):
    """ This is a class that call the functions that computes the weight of 
    an aircraft depending on its configration
    
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
    def __defaults__(self):
        """This sets the default values and methods for the weights analysis.

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
        self.tag      = 'weights' 
        self.method   = 'RCAIDE'

        self.vehicle  = None
        
        self.settings = Data()
        self.settings.use_max_fuel_weight                =  True
        self.settings.weight_reduction_factors           = Data()  
        self.settings.weight_reduction_factors.main_wing = 0.  # Reduction factors are proportional (.1 is a 10% weight reduction)
        self.settings.weight_reduction_factors.fuselage  = 0.  # Reduction factors are proportional (.1 is a 10% weight reduction)
        self.settings.weight_reduction_factors.empennage = 0.  # applied to horizontal and vertical stabilizers
        
        # FLOPS settings
        self.settings.FLOPS = Data() 
        self.settings.FLOPS.aeroelastic_tailoring_factor = 0.   # Aeroelastic tailoring factor [0 no aeroelastic tailoring, 1 maximum aeroelastic tailoring] 
        self.settings.FLOPS.strut_braced_wing_factor     = 0.   # Wing strut bracing factor [0 for no struts, 1 for struts]
        self.settings.FLOPS.composite_utilization_factor = 0.5  # Composite utilization factor [0 no composite, 1 full composite]
        
        # Raymer settings
        self.settings.Raymer = Data()
        self.settings.Raymer.fuselage_mounted_landing_gear_factor = 1. # 1. if false, 1.12 if true
                       
        
    def evaluate(self):
        """Evaluate the weight analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results 
        """
        # unpack
        vehicle = self.vehicle 
        results = RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common.compute_operating_empty_weight(vehicle, settings=self.settings)

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty.total

        # done!
        return results        