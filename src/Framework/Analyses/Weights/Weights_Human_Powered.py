# RCAIDE/Frameworks/Analysis/Weights/Weights_Human_Powered.py
#
# Created:  Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE 
from .Weights import Weights

# ----------------------------------------------------------------------------------------------------------------------
#  Human Powered Weights Analysis
# ----------------------------------------------------------------------------------------------------------------------
class Weights_Human_Powered(Weights):
    """ This is class that evaluates the weight of a human powered aircraft 
    
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
        """This sets the default values and methods for the human powered weight analysis.
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """           
        self.tag      = 'weights_uav'
        self.vehicle  = None     
        
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
        results = RCAIDE.Library.Methods.Weights.Correlation_Buildups.UAV.compute_operating_empty_weight(vehicle)

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty.total

        # done!
        return results        