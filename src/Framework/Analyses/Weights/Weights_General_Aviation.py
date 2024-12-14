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
class Weights_General_Aviation(Weights):
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
        self.settings = None        
        
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
        results = RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight(vehicle, settings=self.settings)

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty.total

        # done!
        return results        