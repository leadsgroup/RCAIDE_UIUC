import RCAIDE
from   RCAIDE.Framework.Core                                   import Units,  Data
import  numpy as  np
from scipy.optimize import minimize_scalar

class PEM_Cell:
    """
    PEM Fuel Cell class

    Constants:
    ----------
    R: float 
        Universal gas constant (J / (mol*K))
    F: float 
        Faraday constant (C / mol)
    E_C: float 
        Activation energy of ORR (J)
    MMH2: float 
        Molar mass of H2 (kg/mol)
    MMO2: float 
        Molar mass of O2 (kg/mol)
    """
    
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """
    
        self.R = 8.31
        self.F = 96485 
        self.E_C = 66000
        self.MMH2 = 2.0 * 10 ** -3 
        self.MMO2 = 32 * 10 ** -3 
        self.O2_mass_frac = 0.233         
        
    def __init__(self, 
                 type, 
                 t_m, 
                 a_c,
                 L_c, 
                 A, 
                 CEM, 
                 maximum_deg=0,
                 rated_current_density = None,
                 rated_power_density = None,
                 rated_p_drop_fc= 0.240, 
                 rated_p_drop_hum=0.025, 
                 gamma_para = 0.03, 
                 alpha=0.375, 
                 gamma = 0.45, 
                 lambda_eff=9.15, 
                 c1 = 0.0435, 
                 c2 = 0.0636, 
                 i0ref = 9 * 10 ** -6, 
                 i0ref_P_ref = 1, 
                 i0ref_T_ref = 353,
                 i_lim_multiplier = 1,
                 area_specific_mass = 2.5):
        self.__defaults__()
        """
        Initialize the PEM fuel cell with given parameters.

        Parameters:
        ----------
        type: string
            The type of PEM model to use, "LT" for low temperature, or "HT" for high temperature
        t_m: Length 
            The membrane thickness of the PEM cell 
        a_c: float 
            The catalyst specific area in cm^2 / mg Pt
        L_c: float 
            The catalyst platinum loading in mg Pt / cm^2
        A: Area 
            The membrane area 
        CEM: CEM 
            The compressor expander module of the air supply system 
        maximum_deg: float 
            The maximum voltage drop due to degradation of the fuel cell at EOL
        rated_current_density: float 
            The rated current density for pressure drop calculations (typically the current density at max power)
            Can be calculated using the evaluate_max_PD method
            Defaults to None 
        rated_power_density: float 
            The rated power density of the fuel cell 
            Defaults to None 
        rated_p_drop_fc: Pressure 
            The pressure drop at rated current density of the fuel cell cathode 
            Defaults to 0.240 bar 
        rated_p_drop_hum: Pressure 
            The pressure drop at rated current density of one side of the membrane humidifier
            Defaults to 0.025 bar
        gamma_para: float 
            The parasitic power draw divided by the gross cell power 
            Does not include compressor/ram-air heat exchanger coolant power
            Defaults to 0.03
        alpha: float 
            The charge transfer coefficient
            Used for both models, is between 0-1, but usually around 0.5 
            Defaults to 0.375 (matches reports and experimental data)
        gamma: float 
            The activation loss pressure dependency coefficient
            Generally 1 for HT-PEM 
            Defaults to 0.45 for LT-PEM
        lambda_eff: float 
            Fitting parameter used to calculate the conductivity of Nafion membranes 
            Only used if type is "LT"
            Values from 9-24 are reasonable 
            Defaults to 9.15 for fully humidifed air 
        c1: float 
            Membrane conductivity of HT PBI membrane at 100 C (ms/cm)
            Only used if type is "HT"
            defaults to 0.0435 for standard PBI membrane 
        c2: float 
            Membrane conductivity of HT PBI membrane at 200 C (ms/cm)
            Only used if type is "HT"
            defaults to 0.0636 for standard PBI membrane 
        i0ref: float 
            Reference current density for activation losses for HT PEM model (A / cm^2 Pt)
            Note that it is given per unit catalyst surface area, not per membrane area 
            defaults to 4e-8
        i0ref_P_ref: float 
            Pressure at which i0ref was determined  
            defaults to 1 bar 
        ioref_T_ref: float 
            Temperature at which i0ref was determined 
            defaults to 369.05 K
        i_lim_multiplier: float 
            The value which the limiting current is multiplied by for advanced PEM systems
        area_specific_mass: float 
            The mass per active membrane area of the fuel cell (kg/m2)
        """
        if type == "LT": 
            self.calculate_ohmic_losses = self.calculate_ohmic_losses_LT
            self.calculate_limiting_current_density = self.calculate_limiting_current_density_LT
            self.calculate_concentration_losses = self.calculate_concentration_losses_LT
        elif type == "HT": 
            self.calculate_ohmic_losses = self.calculate_ohmic_losses_HT
            self.calculate_limiting_current_density = self.calculate_limiting_current_density_HT
            self.calculate_concentration_losses = self.calculate_concentration_losses_HT
        else: 
            raise ValueError('PEM type not supported, currently supported types are "LT" and "HT"')
        self.type = type 
        self.t_m = t_m #* Units.cm
        self.alpha = alpha
        self.a_c = a_c
        self.L_c = L_c
        self.A = A#* Units.cm ** 2
        self.gamma = gamma
        self.lambda_eff = lambda_eff
        self.c1 = c1 
        self.c2 = c2
        self.CEM = CEM
        self.maximum_deg = maximum_deg
        self.rated_current_density = rated_current_density
        self.rated_power_density = rated_power_density
        self.rated_p_drop_fc = rated_p_drop_fc#*Units.bar
        self.rated_p_drop_hum = rated_p_drop_hum #* Units.bar
        self.gamma_para = gamma_para
        self.i0ref = i0ref 
        self.i0ref_P_ref = i0ref_P_ref #* Units.bar 
        self.i0ref_T_ref = i0ref_T_ref #* Units.K
        self.i_lim_multiplier = i_lim_multiplier
        self.area_specific_mass = area_specific_mass

    def set_rated_current_density(self, rated_current_density, rated_power_density): 
        """
        Sets the rated cd and pd of the fuel cell system 

        Parameters: 
        ----------
        rated_CD: float
            The current density (A/cm2) to set 
        rated_power_density: float 
            The power density (W/cm2) to set 
        """
        self.rated_current_density = rated_current_density 
        self.rated_power_density = rated_power_density

    def calculate_P_drop_hum(self, i):
        """
        Calculates the pressure drop across the humidifier for the rated current 

        Parameters: 
        ----------
        i: float 
            Current Density (Acm2) to calculate the pressure drop 

        Returns: 
        ----------
        float 
            The Humidifier pressure drop in bar
        """
        P_drop = (i/self.rated_current_density) ** 2 * self.rated_p_drop_hum
        return P_drop

    def calculate_P_drop_stack(self, i):
        """
        Calculates the pressure drop across the stack for the rated current 

        Parameters: 
        ----------
        i: float 
            Current Density (Acm2) to calculate the pressure drop

        Returns:
        ---------- 
        float 
            The stack pressure drop in bar 
        """
        P_drop = (i/self.rated_current_density) ** 2 * self.rated_p_drop_fc
        return P_drop

    def calculate_P_O2(self, P_air, stack_temperature, RH, air_excess_ratio, P_drop, i): 
        """
        Calculate the partial pressure of oxygen at the fuel cell cathode 

        Parameters: 
        ----------
        P_air: float 
            The input air pressure to the fuel cell (bar)
        stack_temperature: float 
            The fuel cell stack temperature (K)
        RH: float 
            The relative humidity of the oxygen stream (0-1)
        air_excess_ratio: float 
            The oxygen excess ratio (above stoichometric)
        P_drop: float 
            The pressure drop (bar) across the fuel cell cathode 
        i: float 
            The current density (Acm2) to calculate the partial pressure at

        Returns: 
        ----------
        float
            The oxygen partial pressure (bar)
        """
        T_C = stack_temperature - 273.15
        log_P_H2O = -2.1794 + 0.02953 * T_C - 9.1837e-5 * T_C**2 + 1.4454e-7 * T_C**3
        P_H2O = 10 ** log_P_H2O
        N = 0.291 * i / (stack_temperature ** 0.832)
        P_O2 = 0.21 * (P_air - P_drop / 2 - RH * P_H2O) *  ((1 + (air_excess_ratio - 1) / air_excess_ratio) / 2)/ np.exp(N)
        return P_O2
    
    def calculate_P_H2(self, P_H2_input, stack_temperature, RH, i):
        """
        Calculate the partial pressure of hydroen at the fuel cell anode

        Parameters: 
        ----------
        P_H2_input: float 
            The input hydrogen pressure to the fuel cell (bar)
        stack_temperature: float 
            The fuel cell stack temperature (K)
        RH: float 
            The relative humidity of the oxygen stream (0-1)
        i: float 
            The current density (Acm2) to calculate the partial pressure at

        Returns: 
        ----------
        float
            The hydrogen partial pressure (bar)
        """
        T_C = stack_temperature - 273.15
        log_P_H2O = -2.1794 + 0.02953 * T_C - 9.1837e-5 * T_C**2 + 1.4454e-7 * T_C**3
        P_H2O = 10 ** log_P_H2O
        P_H2 = 0.5 * (P_H2_input / np.exp(1.653 * i / stack_temperature**1.334) - RH * P_H2O)
        return P_H2

    def calculate_E_cell(self, stack_temperature, P_H2, P_O2):
        """
        Calculates the reversible Nernst Voltage of the cell

        Parameters:
        ----------
        stack_temperature: float 
            The fuel cell stack temperature (K)
        P_H2: float 
            The hydrogen partial pressure (bar)
        P_O2: float 
            The oxygen partial pressure (bar)

        Returns:
        ----------
        float 
            The reversible cell potential (V)
        """
        try:
            E_cell = 1.229 - 8.45e-4 * (stack_temperature - 298.15) + \
            self.R*stack_temperature / (4 * self.alpha * self.F) * (np.log(P_H2) + 0.5 * np.log(P_O2))
        except: 
            return -10
        return E_cell
    
    def calculate_activation_losses(self, stack_temperature, P_O2, i):
        """
        calculation of activation losses for both high temperature and low temperature fuel cells

        Parameters: 
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        P_O2: float 
            Oxygen Partial Pressure (bar)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns: 
        ----------
        float: 
            Activation voltage loss (V)
        """
        A_const = self.R * stack_temperature / (2 * self.alpha * self.F)
        i0 = self.i0ref * self.L_c * self.a_c * (P_O2/self.i0ref_P_ref) ** (self.gamma) * \
            np.exp(-self.E_C / (self.R * stack_temperature) * (1 - (stack_temperature / self.i0ref_T_ref)))
        eta_act = A_const * np.log(i/i0)
        return eta_act
    
    def calculate_ohmic_losses_LT(self, stack_temperature, i):
        """
        Calculation of ohmic losses for low temperature fuel cells

        Parameters: 
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns: 
        ----------
        float: 
            Ohmic voltage loss (V)
        """
        t_m = self.t_m 
        lambda_eff = self.lambda_eff
        num = 181.6 * (1 + 0.03 * i + 0.062 * (stack_temperature/303) ** 2 * i ** 2.5)
        denom = (lambda_eff - 0.634 - 3 * i) * np.exp(4.18 * (stack_temperature - 303) / stack_temperature)
        rho = num/denom 
        eta_ohmic = (rho * t_m) * i
        return eta_ohmic 
    
    def calculate_ohmic_losses_HT(self, stack_temperature, i):
        """
        Calculation of ohmic losses for high temperature fuel cells

        Parameters: 
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns: 
        ----------
        float: 
            Ohmic voltage loss (V)
        """
        t_m = self.t_m 
        c1 = self.c1
        c2 = self.c2
        s = (stack_temperature - 373.15) / (100) * (c2 - c1) + c1
        rho = 1/s 
        eta_ohmic = (rho * t_m) * i
        return eta_ohmic

    def calculate_concentration_losses_LT(self, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i):
        """
        Calculation of concentration losses for low temperature fuel cells 

        Parameters:
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        P_O2: float 
            Oxygen partial pressure (bar)
        RH: float 
            Relative humidity of the oxygen stream (0-1)
        air_excess_ratio: float 
            Oxygen excess ratio (above stoichometric)
        P_drop: float 
            Pressure drop across the fuel cell stack (bar)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns:
        ----------
        float: 
            Concentration voltage loss (V)
        """
        i_lim = self.calculate_limiting_current_density_LT(stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i)
        if i >= i_lim: 
            return 10
        else: 
            eta_conc = (1 + 1 / self.alpha) * self.R * stack_temperature / (2 * self.F) * np.log(i_lim / (i_lim - i)) 
            return eta_conc
        
    def calculate_limiting_current_density_LT(self, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i, **kwargs): 
        """
        Calculation of the limiting current density for LT-PEM

        Parameters:
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        P_O2: float 
            Oxygen partial pressure (bar)
        RH: float 
            Relative humidity of the oxygen stream (0-1)
        air_excess_ratio: float 
            Oxygen excess ratio (above stoichometric)
        P_drop: float 
            Pressure drop across the fuel cell stack (bar)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns:
        -----------
        float: 
            limiting current density (A/cm^2)
        """
        P_O2_ref_1_atm = self.calculate_P_O2(1, stack_temperature, RH, air_excess_ratio, P_drop, i)
        P_O2_ref_2_5_atm = self.calculate_P_O2(2.5, stack_temperature, RH, air_excess_ratio, P_drop, i)
        i_lim = (2.25 - 1.65) * (P_O2 - P_O2_ref_1_atm)**1 / (P_O2_ref_2_5_atm-P_O2_ref_1_atm)**1 + 1.65
        return self.i_lim_multiplier * i_lim
        
    def calculate_concentration_losses_HT(self, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i):
        """
        Calculation of concentration losses for high temperature fuel cells 

        Parameters:
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        P_O2: float 
            Oxygen partial pressure (bar)
        RH: float 
            Relative humidity of the oxygen stream (0-1)
        air_excess_ratio: float 
            Oxygen excess ratio (above stoichometric)
        P_drop: float 
            Pressure drop across the fuel cell stack (bar)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns:
        -----------
        float: 
            Concentration voltage loss (V)
        """
        i_lim = self.calculate_limiting_current_density_HT(stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i)
        if i >= i_lim: 
            return 10
        else: 
            eta_conc = (1 + 1.8/self.alpha) * self.R * stack_temperature / (2* self.F) * np.log(i_lim / (i_lim - i)) 
            return eta_conc

    def calculate_limiting_current_density_HT(self, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i): 
        """
        Calculation of the limiting current density for HT-PEM

        Parameters:
        ----------
        stack_temperature: float 
            Stack Temperature (K)
        P_O2: float 
            Oxygen partial pressure (bar)
        RH: float 
            Relative humidity of the oxygen stream (0-1)
        air_excess_ratio: float 
            Oxygen excess ratio (above stoichometric)
        P_drop: float 
            Pressure drop across the fuel cell stack (bar)
        i: float 
            Current density to evaluate activation losses (A/cm2)
        
        Returns:
        -----------
        float: 
            limiting current density (A/cm^2)
        """
        P_O2_ref_1_atm = self.calculate_P_O2(1, stack_temperature, RH, air_excess_ratio, P_drop, i)
        P_O2_ref_2_atm = self.calculate_P_O2(2, stack_temperature, RH, air_excess_ratio, P_drop, i)
        i_lim = (2.15 - 1.4) * (P_O2 - P_O2_ref_1_atm)**1 / (P_O2_ref_2_atm-P_O2_ref_1_atm)**1 + 1.4
        return self.i_lim_multiplier * i_lim 
    def calculate_voltage(self, i, stack_temperature, P_H2_input, P_air, RH, air_excess_ratio, p_drop_fc, degradation=0):
        """
        Calculates the output voltage of the fuel cell by subtracting the activation,
        ohmic, and concentration voltage losses from the reversible Nernst voltage, E_cell.

        Parameters:
        ----------
        i: float 
            The current density to evaluate the cell voltage at (A/cm^2)
        stack_temperature: float 
            Temperature of the fuel cell (K)
        P_H2_input: float 
            Pressure of the hydrogen stream (bar)
        P_air: float 
            Pressure of the incoming air (bar)
        RH: float 
            Relative humidity of the air and hydrogen streams (0-1)
        air_excess_ratio: float 
            Air excess ratio (above stoichometric)
        p_drop_fc: float 
            Pressure drop of the fuel cell at the rated current density (bar)
        degradation: float 
            The percent of maximumm degradation to evaluate divided by 100
            optional, defaults to 0 (0% of self.maximum_deg)

        Returns:
        ----------
        float: 
            Output voltage of the fuel cell (V)
        """
        P_O2 = self.calculate_P_O2(P_air, stack_temperature, RH, air_excess_ratio, p_drop_fc, i)
        P_H2 = self.calculate_P_H2(P_H2_input, stack_temperature, RH, i)
        E_cell = self.calculate_E_cell(stack_temperature, P_H2, P_O2)
        eta_act = self.calculate_activation_losses(stack_temperature, P_O2, i)
        eta_ohmic = self.calculate_ohmic_losses(stack_temperature, i)
        eta_conc = self.calculate_concentration_losses(stack_temperature, P_O2, RH, air_excess_ratio, p_drop_fc, i)

        # Calculate the output voltage of the fuel cell
        V_cell = E_cell - eta_act - eta_ohmic - eta_conc - degradation * self.maximum_deg
        V_loss = eta_act + eta_ohmic + eta_conc + degradation * self.maximum_deg
        return V_cell, V_loss
    
    def evaluate_max_gross_power(self, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, degradation=0, **kwargs):
        
        P_O2 = self.calculate_P_O2(FC_air_p, stack_temperature, RH, air_excess_ratio, self.rated_p_drop_fc, 0)
        i_lim = self.calculate_limiting_current_density(stack_temperature, P_O2, RH, air_excess_ratio, 0, i=0)

        def evaluate_power(i): 
            V_cell, V_loss = self.calculate_voltage(i, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, self.rated_p_drop_fc, degradation)
            PD = -V_cell * i 
            return PD

        res = minimize_scalar(evaluate_power, bounds = (0.2 * i_lim, 0.95 * i_lim))
        rated_current_density = res.x 
        rated_power_density = -res.fun 
        return rated_current_density, rated_power_density
    
    def evaluate_max_net_power(self, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, thermo_state, degradation=0): 
        P_O2 = self.calculate_P_O2(FC_air_p, stack_temperature, RH, air_excess_ratio, self.rated_p_drop_fc, 0)
        i_lim = self.calculate_limiting_current_density(stack_temperature, P_O2, RH, air_excess_ratio, 0, i=0)
        compressor_powers = []
        def evaluate_power(i): 
            res = self.evaluate(i, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, thermo_state, degradation)
            net_power = res[1]
            compressor_powers.append(res[4])
            return -net_power
        
        res = minimize_scalar(evaluate_power, bounds = (0.2 * i_lim, 0.95 * i_lim))
        compressor_power = compressor_powers[-1]
        rated_current_density = res.x 
        rated_power = -res.fun 
        return rated_current_density, rated_power, compressor_power

    def evaluate_CEM(self, FC_air_p, thermo_state_in, mdot_air_in, air_excess_ratio, p_drop_hum, p_drop_fc):
        """
        Evaluates the power required by the CEM (compressor-expander module)

        Parameters: 
        ----------
        FC_air_p: float 
            Air pressure after the humidifier entering the fuel cell (bar)
        thermo_state_in: ThermoState 
            Air thermostate entering the compressor
        mdot_air_in: float 
            Mass flow of air entering the fuel cell and compressor (kg/s)
        air_excess_ratio: float 
            Oxygen excess ratio (above stoichometric)
        p_drop_hum: float 
            The pressure drop (bar) through the humidifier 
        p_drop_fc: float 
            The pressure drop (bar) through the fuel cell

        Returns: 
        ----------
        float: 
            The power required to run the CEM at the given operating conditions (W)
        """
        p_air_out = FC_air_p + p_drop_hum 
        state = self.CEM.evaluate(p_air_out, thermo_state_in, mdot_air_in, air_excess_ratio, p_drop_hum, p_drop_fc)
        power_req = state.CEM_power
        mdot_out = state.mdot_out_exp
        expander_power = state.P_exp
        return power_req, mdot_out, expander_power
    
    def evaluate(self, i, stack_temperature, P_H2_input, FC_air_p, RH, air_excess_ratio, thermo_state_in, degradation=0):
        """
        Determines the fuel cell state of the PEM fuel cell 

        Parameters: 
        ----------
        i: float 
            The current density to evaluate the cell voltage at (A/cm^2)
        stack_temperature: Temperature 
            Temperature of the fuel cell
        P_H2_input: Pressure
            Pressure of the hydrogen stream 
        FC_air_p: Pressure
            Pressure of the hydrogen air entering the fuel cell
        RH: float 
            Relative humidity of the air and hydrogen streams (0-1)
        air_excess_ratio: float 
            Air excess ratio (above stoichometric)
        thermo_state_in: ThermoState 
            Conditions of air entering the compressor
        degradation: float 
            The voltage drop due to degradation (V)
            optional, defaults to 0 V 

        Returns: 
        ----------
        float: 
            Hydrogen Mass flow (kg/s)
        float: 
            Net Power (W)
        float: 
            Gross power (W)
        float: 
            Gross heat (W)
        float: 
            Compressor Power (W)
        float: 
            mdot_air_in (kg/s)
        """
        p_drop_fc = self.calculate_P_drop_stack(i)
        if self.type == "LT":
            p_drop_hum = self.calculate_P_drop_hum(i) 
        else: 
            p_drop_hum = 0
        mdot_air_in = i * self.A * self.MMO2 / (4 * self.F * self.O2_mass_frac) * air_excess_ratio
        mdot_H2 = i * self.A / (2 * self.F) * self.MMH2
        V, V_loss = self.calculate_voltage(i, stack_temperature, P_H2_input, FC_air_p, RH, air_excess_ratio, p_drop_fc, degradation)
        gross_power = V * i * self.A
        gross_heat = V_loss * i * self.A
        compressor_power, mdot_air_out, expander_power = self.evaluate_CEM(FC_air_p, thermo_state_in, mdot_air_in, air_excess_ratio, p_drop_hum, p_drop_fc)
        parasitic_power = self.gamma_para * gross_power
        net_power = gross_power - compressor_power - parasitic_power
        return mdot_H2, net_power, gross_power, gross_heat, compressor_power, mdot_air_in, mdot_air_out, expander_power

    def get_weight_estimate(self):
        return self.A / 100 / 100 * self.area_specific_mass 

    def generate_gross_polarization_curve_data(self, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, CD_end, thermo_state, degradation=0, no_points = 200):
        """
        Generates lists containing the output gross voltage as a function of current density of the fuel cell.

        Parameters:
        ----------
        stack_temperature: float
            Fuel cell stack temperature (K)
        P_H2_input: float 
            Input partial pressure of hydrogen (bar)
        P_air: float 
            Input partial pressure of air (bar)
        RH: float 
            Relative humidity (0 to 1)
        air_excess_ratio: float
            Air excess ratio (above stoichometric)
        CD_end: float 
            Current Density to end evaluation at 
        no_points: float 
            Number of current densities to evaluate

        Returns: 
        -----------
        list: 
            current densities that the fuel cell was evaluated at 
        list: 
            output voltages of the fuel cell
        """
        current_densities = np.linspace(0.01, CD_end, no_points)  # Current densities from 0 to 2 A/cm^2 in steps of 0.01 A/cm^2
        voltages = []
        for i in current_densities: 
            p_drop_fc = self.calculate_P_drop_stack(i)
            v = self.calculate_voltage(i, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, p_drop_fc, degradation)[0]
            if v>0: 
                voltages.append(v)
            else: 
                voltages.append(np.nan)
        return current_densities, np.array(voltages)

    def generate_net_polarization_curve_data(self, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, CD_end, thermo_state, degradation=0, no_points = 200):
        """
        Generates lists containing the output net voltage as a function of current density of the fuel cell.

        Parameters:
        ----------
        stack_temperature: float
            Fuel cell stack temperature (K)
        P_H2_input: float 
            Input partial pressure of hydrogen (bar)
        P_air: float 
            Input partial pressure of air (bar)
        RH: float 
            Relative humidity (0 to 1)
        air_excess_ratio: float
            Air excess ratio (above stoichometric)
        CD_end: float 
            Current Density to end evaluation at 
        no_points: float 
            Number of current densities to evaluate

        Returns: 
        -----------
        list: 
            current densities that the fuel cell was evaluated at 
        list: 
            output voltages of the fuel cell
        """
        current_densities = np.linspace(0.01, CD_end, no_points)  # Current densities from 0 to 2 A/cm^2 in steps of 0.01 A/cm^2
        voltages = []
        for i in current_densities: 
            v = self.evaluate(i, stack_temperature, p_H2, FC_air_p, RH, air_excess_ratio, thermo_state, degradation)[1] / i / self.A
            if v>0: 
                voltages.append(v)
            else: 
                voltages.append(np.nan)
        return current_densities, np.array(voltages)