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
        else:
            raise ValueError('Method type not supported')

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty.total

        # done!
        return results        