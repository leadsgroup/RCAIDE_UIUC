# RCAIDE/Library/Attributes/Materials/__init__.py
# 

"""
This module provides material handling capabilities for RCAIDE. It includes classes for managing different types of materials 
and their physical properties, with implementations for various structural and aerospace materials including:
    - Metals (Aluminum, Steel, Nickel, Titanium, Magnesium)
    - Composites (Unidirectional and Bidirectional Carbon Fiber, Carbon Fiber Honeycomb)
    - Polymers (Epoxy, Polyetherimide, Acrylic)
    - Surface Treatments (Paint)

The Solid class serves as the base class for all material implementations.

See Also
--------
RCAIDE.Library.Attributes.Gases : Related module for gas properties
RCAIDE.Library.Attributes.Liquids : Related module for liquid properties
RCAIDE.Library.Attributes.Cryogens : Related module for cryogenic material properties
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Solid                       import Solid
from .Unidirectional_Carbon_Fiber import Unidirectional_Carbon_Fiber
from .Bidirectional_Carbon_Fiber  import Bidirectional_Carbon_Fiber
from .Carbon_Fiber_Honeycomb      import Carbon_Fiber_Honeycomb
from .Epoxy                       import Epoxy
from .Aluminum_Rib                import Aluminum_Rib
from .Paint                       import Paint
from .Aluminum                    import Aluminum
from .Polyetherimide              import Polyetherimide
from .Acrylic                     import Acrylic
from .Steel                       import Steel
from .Nickel                      import Nickel
from .Titanium                    import Titanium
from .Magnesium                   import Magnesium