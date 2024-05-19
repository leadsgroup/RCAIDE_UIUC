## @ingroup Library-Compoments-Thermal_Management-Cryogenics
# RCAIDE/Library/Compoments/Thermal_Management/Cryogenics/Cryogenic_Heat_Exchange.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Energy.Thermal_Management.Cryogenics.compute_cryogen_mass_flow_rate import compute_cryogen_mass_flow_rate
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Cryogenic Heat Exchanger Component
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Thermal_Management-Cryogenics
class Cryogenic_Heat_Exchanger(Component):
    """This provides output values for a heat exchanger used to cool cryogenic components
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """         
        
        self.tag = 'Cryogenic_Heat_Exchanger'
        
        #-----setting the default values for the different components
        self.cryogen                        = RCAIDE.Library.Attributes.Cryogens.Liquid_H2()
        self.cryogen_inlet_temperature      =    300.0      # [K]
        self.cryogen_outlet_temperature     =    300.0      # [K]
        self.cryogen_pressure               = 100000.0      # [Pa]
        self.cryogen_is_fuel                =      0.0      # Proportion of cryogen that is burned as fuel. Assumes the cryogen is the same as the fuel, e.g. that both are hydrogen.
        self.inputs.cooling_power           =      0.0      # [W]
        self.outputs.mdot                   =      0.0      #[kg/s]

    def energy_calc(self, conditions):

        
        """ This calculates the mass of cryogen required to achieve the desired cooling power given the temperature of the cryogen supplied, and the desired temperature of the cryogenic equipment.

        Assumptions:
        Perfect thermal conduction of the cryogen to the cooled equipment.

        Source:
        N/A

        Inputs:
        self.inputs
            cooling_power      [W]

        Outputs:
        self.outputs.
            mdot                   [kg/s]

        Properties Used:
        self.
            cryogen_inlet_temperature       [K]
            cryogen_outlet_temperature      [K]
            cryogen_pressure                [Pa]

        
        """         
        # unpack the values from self
        temp_in         = self.cryogen_inlet_temperature 
        temp_out        = self.cryogen_outlet_temperature
        pressure        = self.cryogen_pressure
        cryogen         = self.cryogen        

        cooling_power   = self.inputs.cooling_power 

        # If the heat exchanger does not vent to ambient, set the system pressure.
        vent_pressure   = pressure

        # calculate the cryogen mass flow
        mdot = compute_cryogen_mass_flow_rate(cryogen,temp_in,temp_out,cooling_power,vent_pressure)
        self.outputs.mdot = mdot
    
        return mdot
        
    