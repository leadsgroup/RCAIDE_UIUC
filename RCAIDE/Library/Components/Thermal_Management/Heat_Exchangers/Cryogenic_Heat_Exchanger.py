# RCAIDE/Library/Components/Thermal_Management/Heat_Exchangers/Cryogenic_Heat_Exchange.py
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports  
import RCAIDE 
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Thermal_Management.Cryogenics.compute_cryogen_mass_flow_rate import compute_cryogen_mass_flow_rate
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Cryogenic Heat Exchanger Component
# ---------------------------------------------------------------------------------------------------------------------- 
class Cryogenic_Heat_Exchanger(Component):
    """
    A class representing a heat exchanger designed for cryogenic cooling applications, 
    using cryogenic fluids to maintain extremely low temperatures.

    Attributes
    ----------
    tag : str
        Unique identifier for the heat exchanger, defaults to 'Cryogenic_Heat_Exchanger'
        
    cryogen : Cryogen
        Cryogenic fluid properties, defaults to Liquid_H2()
        
    cryogen_inlet_temperature : float
        Temperature of cryogen at inlet in K, defaults to 300.0
        
    cryogen_outlet_temperature : float
        Temperature of cryogen at outlet in K, defaults to 300.0
        
    cryogen_pressure : float
        Operating pressure of cryogen in Pa, defaults to 100000.0
        
    cryogen_is_fuel : float
        Proportion of cryogen used as fuel, defaults to 0.0
        
    inputs.cooling_power : float
        Required cooling power in W, defaults to 0.0
        
    outputs.mdot : float
        Mass flow rate of cryogen in kg/s, defaults to 0.0

    Notes
    -----
    The cryogenic heat exchanger provides cooling at extremely low temperatures using 
    cryogenic fluids. The system:
    
    * Manages heat transfer between cryogen and cooled equipment
    * Controls cryogen flow based on cooling demand
    * Maintains equipment at cryogenic temperatures

    **Definitions**

    'Cryogen'
        Fluid used to achieve very low temperatures, typically below 120K
        
    'Cooling Power'
        Heat removal capacity at cryogenic temperature

    See Also
    --------
    RCAIDE.Library.Components.Thermal_Management.Heat_Exchangers.Cross_Flow_Heat_Exchanger
        Alternative heat exchanger for moderate temperature applications
    """
    
    def __defaults__(self):
        """
        Sets default values for the cryogenic heat exchanger attributes.
        """         
        self.tag                       = 'Cryogenic_Heat_Exchanger'
        self.cryogen                   = RCAIDE.Library.Attributes.Cryogens.Liquid_H2()
        self.cryogen_inlet_temperature = 300.0
        self.cryogen_outlet_temperature= 300.0
        self.cryogen_pressure         = 100000.0
        self.cryogen_is_fuel          = 0.0
        self.inputs.cooling_power     = 0.0
        self.outputs.mdot             = 0.0

    def energy_calc(self, conditions):
        """
        Calculates required cryogen mass flow rate for desired cooling power.

        Parameters
        ----------
        conditions : Data
            Operating conditions for the calculation

        Returns
        -------
        float
            Required cryogen mass flow rate in kg/s

        Notes
        -----
        Calculation considers:
        * Inlet and outlet temperatures
        * Required cooling power
        * Cryogen properties
        * System pressure
        """
        # unpack the values
        temp_in      = self.cryogen_inlet_temperature 
        temp_out     = self.cryogen_outlet_temperature
        pressure     = self.cryogen_pressure
        cryogen      = self.cryogen        
        cooling_power= self.inputs.cooling_power 
        vent_pressure= pressure

        # calculate the cryogen mass flow
        mdot = compute_cryogen_mass_flow_rate(cryogen, temp_in, temp_out, 
                                            cooling_power, vent_pressure)
        self.outputs.mdot = mdot
        return mdot
        
    