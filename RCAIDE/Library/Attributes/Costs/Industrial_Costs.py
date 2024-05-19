## @ingroup Library-Attributes-Costs
# RCAIDE/Library/Attributes/Costs/Industrial_Costs.py
# 
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Framework.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Industrial_Costs Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Attributes-Costs
class Industrial_Costs(Data):
    """A class containing industrial cost variables. 
    """     
    def __defaults__(self):
        """This sets the default values used in the industrial cost methods.
        
        Assumptions:
            None
        
        Source:
            None 
        """        
        # inputs
        self.tag                            = 'industrial_costs'
        self.reference_year                 = 0.0
        self.production_total_units         = 0.0
        self.units_to_amortize              = None
        self.prototypes_units               = 0.0
        self.avionics_cost                  = 0.0
        self.test_facilities_cost           = 0.0
        self.manufacturing_facilities_cost  = 0.0
        self.escalation_factor              = 0.0
        self.development_total_years        = 0.0
        self.aircraft_type                  = None # ('military','general aviation','regional','commercial','business')
        self.difficulty_factor              = 1.0  # (1.0 for conventional, 1.5 for moderately advanc. tech., 2 for agressive use of adv. tech.)
        self.cad_factor                     = 1.0  # (1.2 for learning, 1.0 for manual, 0.8 for experienced)
        self.stealth                        = 0.0  # (0 for non-stealth, 1 for stealth)
        self.material_factor                = 1.0  # (1 for conventional Al, 1.5 for stainless steel, 2~2.5 for composites, 3 for carbon fiber)

        # hourly rates
        self.hourly_rates                   = Data()
        hourly_rates                        = self.hourly_rates
        hourly_rates.engineering            = 0.0
        hourly_rates.tooling                = 0.0
        hourly_rates.manufacturing          = 0.0
        hourly_rates.quality_control        = 0.0