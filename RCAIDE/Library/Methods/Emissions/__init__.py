# RCAIDE/Library/Methods/Emissions/__init__.py
#
# Created: 2024, M. Clarke

"""
Aircraft Emissions Analysis Package

This module provides functionality for evaluating aircraft emissions using both empirical 
and physics-based methods.

Notes
-----
The Emissions package contains two main approaches for emissions calculation:

1. Chemical Reactor Network (CRN) Method:
    - Detailed chemical kinetics using Cantera
    - Primary and secondary combustion zone modeling
    - Species-specific emission indices computation
    - Surrogate model capabilities 

2. Empirical Index Method:
    - Quick estimation utilizing pre-defined empirical correlations
    - Global Warming Potential considerations
    - Contrail effects estimation

**Definitions**

'Emission Index (EI)'
    Mass of pollutant emitted per unit mass of fuel burned [kg_pollutant/kg_fuel]

'Global Warming Potential (GWP)'
    Relative measure of heat trapped by a greenhouse gas compared to CO2

See Also
--------
RCAIDE.Library.Methods.Emissions.Emission_Index_Empirical_Method
RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method

References
----------
[1] Goodwin, D. G., Speth, R. L., Moffat, H. K., & Weber, B. W. (2023). Cantera: An object-oriented software toolkit for chemical kinetics, thermodynamics, and transport processes (Version 3.0.0) [Computer software]. https://www.cantera.org

[2] Lee, D. S., et al. (2021). The contribution of global aviation to anthropogenic climate forcing for 2000 to 2018. Atmospheric Environment, 244, 117834.
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Emission_Index_Empirical_Method import *
from .Chemical_Reactor_Network_Method  import *

