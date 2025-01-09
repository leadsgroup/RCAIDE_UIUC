# Aluminum_Rib.py
#
# Created: Jul, 2017, J. Smart
# Modified: Apr, 2018, J. Smart

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Solid import Solid
from .Aluminum import Aluminum
from RCAIDE.Framework.Core import Units

#-------------------------------------------------------------------------------
# Aluminim Component Material Property Data Class
#-------------------------------------------------------------------------------

class Aluminum_Rib(Aluminum):
    """
    A class representing 6061-T6 aluminum ribs with specific manufacturing constraints.

    Attributes
    ----------
    minimum_gage_thickness : float
        Minimum manufacturable thickness for precision rib components in m (1.5e-3)
    minimum_width : float
        Minimum manufacturable width for rib components in m (25.4e-3)

    Notes
    -----
    This class extends the base Aluminum class, specifically for rib components.
    It adds manufacturing constraints typical for precision machined aluminum ribs.
    All other material properties (strength, density, etc.) are inherited from the 
    Aluminum class for 6061-T6 alloy.

    **Definitions**
    
    'Minimum Gage Thickness'
        The smallest thickness that can be reliably manufactured for a rib component
        while maintaining structural integrity and manufacturing tolerances
    
    'Minimum Width'
        The smallest width that can be reliably manufactured for a rib component
        while maintaining structural integrity and manufacturing tolerances

    References
    ----------
    [1] MatWeb. (n.d.). Aluminum 6061-T6; 6061-T651. https://www.matweb.com/search/DataSheet.aspx?MatGUID=b8d536e0b9b54bd7b69e4124d8f1d20a 
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


        self.minimum_gage_thickness = 1.5e-3   * Units.m
        self.minimum_width          = 25.4e-3  * Units.m

