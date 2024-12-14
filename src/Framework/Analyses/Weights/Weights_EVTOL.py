# RCAIDE/Frameworks/Analysis/Weights/Weights_EVTOL.py
#
# Created:  Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE
from RCAIDE.Framework.Core import  Data 
from .Weights import Weights

# ----------------------------------------------------------------------------------------------------------------------
#  BWB Weights Analysis
# ----------------------------------------------------------------------------------------------------------------------
class Weights_EVTOL(Weights):
    """ This is class that evaluates the weight of an electric vertical takeoff and landing aircraft  
    
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
        """This sets the default values and methods for the  electric vertical takeoff and landing aircraft weight analysis.
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """           
        self.tag                                    = 'weights_evtol'
        self.vehicle                                = None 
        self.settings                               = Data()    
        self.settings.miscelleneous_weight_factor   = 1.1 
        self.settings.safety_factor                 = 1.5   
        self.settings.disk_area_factor              = 1.15     
        self.settings.max_thrust_to_weight_ratio    = 1.1
        self.settings.max_g_load                    = 3.8        
        
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
        results = RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric.compute_operating_empty_weight(vehicle, settings=self.settings)

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty.total

        # done!
        return results        