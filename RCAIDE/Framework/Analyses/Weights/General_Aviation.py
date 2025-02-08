# RCAIDE/Frameworks/Analysis/Weights/Weights_General_Aviation.py
#
# Created:  Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE 
from RCAIDE.Framework.Core import Data 
from .Weights import Weights

# ----------------------------------------------------------------------------------------------------------------------
#  General Aviation Weights Analysis
# ----------------------------------------------------------------------------------------------------------------------
class General_Aviation(Weights):
    """ This is class that evaluates the weight of a general aviation aircraft
    
    Assumptions:
        None

    Source:
        N/A

    Inputs:
        None
      
    Outputs:
        None 
    """
    def __defaults__(self):
        """This sets the default values and methods for the general aviation weight analysis.
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """           
        self.tag      = 'weights_general_aviation'
        self.vehicle  = None    
        
        self.settings = Data()  
        self.settings.use_max_fuel_weight = True
        self.settings.advanced_composites = False

        # FLOPS settings
        self.settings.FLOPS = Data() 
        self.settings.FLOPS.aeroelastic_tailoring_factor = 0.   # Aeroelastic tailoring factor [0 no aeroelastic tailoring, 1 maximum aeroelastic tailoring] 
        self.settings.FLOPS.strut_braced_wing_factor     = 0.   # Wing strut bracing factor [0 for no struts, 1 for struts]
        
        
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
        settings = self.settings
        
        if self.method == 'Raymer':
            results = RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups.General_Aviation.Raymer.compute_operating_empty_weight(vehicle, settings=settings)
        elif self.method == "FLOPS Simple" or self.method == "FLOPS Complex":
            self.settings.complexity = self.method.split()[1]
            results =  RCAIDE.Library.Methods.Mass_Properties.Weight_Buildups.General_Aviation.FLOPS.compute_operating_empty_weight(vehicle, self.settings)
        else:   
            raise ValueError('Method type not supported')

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty.total

        # done!
        return results        