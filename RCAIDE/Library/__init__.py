# RCAIDE/Library/__init__.py 

"""
RCAIDE Library provides core functionality for aircraft design and optimization through a collection of modules.
The module contains the methods and classes used for modeling aircraft components and systems. The 
Framework module contains the system architecture that calls to different library modules. The 
modules work together to enable aircraft conceptual design, analysis, and optimization workflows.

See Also
--------
RCAIDE.Framework : Core framework functionality and tools
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from . import Attributes
from . import Components 
from . import Methods 
from . import Mission
from . import Plots 