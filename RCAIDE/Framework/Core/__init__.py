## @defgroup Core
# RCAIDE/Core/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Core.Data          import Data
from Legacy.trunk.S.Core.DataOrdered   import DataOrdered
from Legacy.trunk.S.Core.Diffed_Data   import Diffed_Data, diff
from Legacy.trunk.S.Core               import ContainerOrdered , redirect
from .Container                        import Container
from .Utilities                        import * 
from Legacy.trunk.S.Core.Units         import Units 