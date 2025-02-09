# RCAIDE/Framework/Analyses/Weights/Electric.py
#
# Created:  Feb 2025, S. Shekar
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core import Data 
from .Weights import Weights

# ----------------------------------------------------------------------------------------------------------------------
#  
# ----------------------------------------------------------------------------------------------------------------------
class Electric(Weights):
    """ This is class that evaluates the weight of Transport class aircraft

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
        """This sets the default values and methods for the tube and wing
        aircraft weight analysis.

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
        self.tag           = 'electric_weights'
        self.method        = 'Physics_Based'
        self.aircraft_type = 'General_Aviation'
        self.propulsion_architecture = 'Electric'

        
     