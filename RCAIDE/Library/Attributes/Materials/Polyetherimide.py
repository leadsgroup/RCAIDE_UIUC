# @ingroup Attributes-Materials 

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Material import Material
from RCAIDE.Core import Units

#-------------------------------------------------------------------------------
# Aluminum for WavyChannel for battery cooling
#-------------------------------------------------------------------------------

## @ingroup Attributes-Solid
class Polyetherimide(Material):

    """ Physical Constants Specific to 6061-T6 Aluminum

    Assumptions:
    None

    Source:
    Cao W, Zhao C, Wang Y, et al. Thermal modeling of full-size-scale cylindrical battery pack cooled
    by channeled liquid flow[J]. International journal of heat and mass transfer, 2019, 138: 1178-1187.

    Inputs:
    N/A

    Outputs:
    N/A

    Properties Used:
    None
    """

    def __defaults__(self):
        """Sets material properties at instantiation.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        N/A

        Outputs:
        N/A

        Properties Used:
        None
        """ 
        self.conductivity              = 2.0                                      # [W/m-K]
        self.emissivity                = 0.96                                     # [uniteless]
        self.specific_heat             = 1100              
