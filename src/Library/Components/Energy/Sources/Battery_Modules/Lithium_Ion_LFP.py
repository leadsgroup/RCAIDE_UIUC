# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Ion_LFP
# 
# 
# Created: Nov 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core          import Units,Data
from .Generic_Battery_Module import  Generic_Battery_Module
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Lithium_Ion_LFP  import * 

# package imports 
import numpy as np  
import os
from scipy.interpolate  import NearestNDInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_LFP
# ----------------------------------------------------------------------------------------------------------------------  
class Lithium_Ion_LFP(Generic_Battery_Module):
    """ 26650 A123 Lithium Ion LFP cell.  
        """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None

        Source:
         # Cell Information 
           Datasheet: https://a123batteries.com/product_images/uploaded_images/26650.pdf
            
            Arora, Shashank, and Ajay Kapoor. “Experimental Study of Heat Generation 
            Rate during Discharge of LiFePO4 Pouch Cells of Different Nominal Capacities
            and Thickness.” Batteries 5, no. 4 (November 11, 2019): 70. 
            https://doi.org/10.3390/batteries5040070.        
        """
        # ----------------------------------------------------------------------------------------------------------------------
        #  Module Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.tag                                               = 'lithium_ion_lfp' 
        self.power_split_ratio                                 = None
        self.number_of_cells                                   = 1
        self.maximum_energy                                    = 0.0
        self.maximum_power                                     = 0.0
        self.maximum_voltage                                   = 0.0       
        
        # ----------------------------------------------------------------------------------------------------------------------
        #  Cell Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.cell.chemistry                   = 'LiFePO4'
        self.cell.diameter                    = 0.0185                                                    # [m]
        self.cell.height                      = 0.0653                                                    # [m]
        self.cell.mass                        = 0.03  * Units.kg                                          # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) \
                                                + (0.5*np.pi*self.cell.diameter**2)                       # [m^2]

        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height        # [m^3] 
        self.cell.density                     = self.cell.mass/self.cell.volume                           # [kg/m^3]
        self.cell.electrode_area              = 0.0342                                                    # [m^2]  # estimated 
                                                        
        self.cell.maximum_voltage             = 3.6                                                       # [V]
        self.cell.nominal_capacity            = 2.6                                                       # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                       # [V]
         
        self.cell.watt_hour_rating            = self.cell.nominal_capacity  * self.cell.nominal_voltage   # [Watt-hours]      
        self.cell.specific_energy             = self.cell.watt_hour_rating*Units.Wh/self.cell.mass        # [J/kg]
        self.cell.specific_power              = self.cell.specific_energy/self.cell.nominal_capacity      # [W/kg]   
        self.cell.resistance                  = 0.022                                                     # [Ohms]
                                                                                                            
        self.cell.specific_heat_capacity      = 1115                                                      # [J/kgK]                                                     
        self.cell.radial_thermal_conductivity = 0.475                                                     # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 37.6                                                      # [J/kgK]  

        battery_raw_data                      = load_battery_results()                                                   
        self.cell.discharge_performance_map   = create_discharge_performance_map(battery_raw_data)

        return                                     

    def energy_calc(self,state,bus,coolant_lines, t_idx, delta_t): 
        """Computes the state of the LFP battery cell.
           
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            self               : battery        [unitless]
            state              : temperature    [K]
            bus                : pressure       [Pa]
            discharge (boolean): discharge flag [unitless]
            
        Returns: 
            None
        """      
        stored_results_flag, stored_battery_tag =  compute_lfp_cell_performance(self,state,bus,coolant_lines, t_idx,delta_t) 
                        
        return stored_results_flag, stored_battery_tag
    
    def reuse_stored_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag):
        reuse_stored_lfp_cell_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag)
        return    
      
    def update_battery_age(self,segment, battery_conditions,increment_battery_age_by_one_day): 
        update_lfp_cell_age(self,segment, battery_conditions,increment_battery_age_by_one_day)
        return 
    
def create_discharge_performance_map(raw_data):
    '''Creates multiple surfaces from the data generated from 
        
    Assumptions:
        
        
    Source:
         Lin, Xinfan, Hector Perez, Jason B. Siegel, and Anna G. Stefanopoulou.
        “An Electro-Thermal Model for the A123 26650 LiFePO4 Battery.” 
        University of Michigan. Accessed November 11, 2024. 
        https://hdl.handle.net/2027.42/97341.
        
    
    Args: 
        None
        
    Returns:
        battery_data: ]
    '''    
    # Prepare lists for the data needed for interpolation
    c_rates = []
    temperatures = []
    discharge_capacities = []
    voltages = []

    # Iterate through the data structure to populate the lists
    for c_rate_key, temp_data in raw_data.items():
        c_rate = float(c_rate_key)  # Convert C-rate to float

        for temp_key, data in temp_data.items():
            initial_temp = int(temp_key.split()[-1])  # Extract temperature as an integer

            # Extend lists with the discharge, voltage, and other data
            discharge_capacities.extend(data['discharge'])
            voltages.extend(data['voltage'])
            c_rates.extend([c_rate] * len(data['discharge']))
            temperatures.extend([initial_temp] * len(data['discharge']))

    # Convert lists to numpy arrays
    points = np.array([c_rates, temperatures, discharge_capacities]).T
    values = np.array(voltages)

    # Create the interpolant
    battery_data = NearestNDInterpolator(points, values) # Can be replaced by a Linear Interpolator for a better fit but computation time increases by 30 times. 

    return battery_data  

def load_battery_results(): 
    '''Load experimental raw data of LFP cells 
        
    Assumptions:
        
        
    Source:
        
    
    Args: 
        None
        
    Returns:
        battery_data: raw data from battery   [unitless]
    '''    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, 'lfp_raw_data.res')

    # Load the raw_data using RCAIDE.load()
    raw_data = RCAIDE.load(full_path)

    return raw_data