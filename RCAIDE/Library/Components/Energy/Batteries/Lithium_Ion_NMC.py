## @ingroup Library-Compoments-Energy-Batteries
# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Ion_LiNiMnCoO2_18650.py
# 
# 
# Created:  Mar 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core                                         import Units , Data
from .Lithium_Ion_Generic                                           import Lithium_Ion_Generic   
from RCAIDE.Library.Methods.Energy.Sources.Battery.Lithium_Ion_NMC  import compute_nmc_cell_performance, update_nmc_cell_age

# package imports 
import numpy as np
import os 
from scipy.interpolate  import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_NMC
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Energy-Batteries 
class Lithium_Ion_NMC(Lithium_Ion_Generic):
    """ 18650 lithium-nickel-manganese-cobalt-oxide battery cells.
    """       
    
    def __defaults__(self):   
        """This sets the default values.
    
        Assumptions:
            Convective Thermal Conductivity Coefficient corresponds to forced
            air cooling in 35 m/s air 
        
        Source: 
            convective  heat transfer coefficient, h 
            Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical 
            lithium ion battery during discharge cycle." Energy Conversion and Management
            52.8-9 (2011): 2973-2981.
            
            thermal conductivity, k 
            Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
            System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
            (2019): 6077-6107.
            
            specific heat capacity, Cp
            (axial and radial)
            Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
            System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
            (2019): 6077-6107.
            
            # Electrode Area
            Muenzel, Valentin, et al. "A comparative testing study of commercial
            18650-format lithium-ion battery cells." Journal of The Electrochemical
            Society 162.8 (2015): A1592.
        
        """    
        self.tag                              = 'lithium_ion_nmc'  

        self.cell.diameter                    = 0.0185                                                   # [m]
        self.cell.height                      = 0.0653                                                   # [m]
        self.cell.mass                        = 0.048 * Units.kg                                         # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) + (0.5*np.pi*self.cell.diameter**2)  # [m^2]
        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height 
        self.cell.density                     = self.cell.mass/self.cell.volume                          # [kg/m^3]  
        self.cell.electrode_area              = 0.0342                                                   # [m^2] 
                                                                                               
        self.cell.maximum_voltage             = 4.2                                                      # [V]
        self.cell.nominal_capacity            = 3.55                                                     # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                      # [V] 
        self.cell.charging_voltage            = self.cell.nominal_voltage                                # [V] 
        
        self.watt_hour_rating                 = self.cell.nominal_capacity  * self.cell.nominal_voltage  # [Watt-hours]      
        self.specific_energy                  = self.watt_hour_rating*Units.Wh/self.cell.mass            # [J/kg]
        self.specific_power                   = self.specific_energy/self.cell.nominal_capacity          # [W/kg]   
        self.resistance                       = 0.025                                                    # [Ohms]
                                                                                                         
        self.specific_heat_capacity           = 1108                                                     # [J/kgK]  
        self.cell.specific_heat_capacity      = 1108                                                     # [J/kgK]    
        self.cell.radial_thermal_conductivity = 0.4                                                      # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 32.2                                                     # [J/kgK] # estimated  
                                              
        battery_raw_data                      = load_battery_results()                                                   
        self.discharge_performance_map        = create_discharge_performance_map(battery_raw_data)  
         
        return  
    
    def energy_calc(self,state,bus,discharge= True): 
        """Computes the state of the NMC battery cell.
           
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
        compute_nmc_cell_performance(self,state,bus,discharge) 
        
        return 
    
    def compute_voltage(self,battery_conditions):  
        """ Computes the voltage of a single NMC cell or a battery pack of NMC cells   
        
        Assumptions:
            None
        
        Source:
            None
    
        Args:
            self               : battery          [unitless] 
            battery_conditions : state of battery [unitless]
            
        Returns: 
            None
        """              
        return battery_conditions.pack.voltage_under_load 
    
    def update_battery_age(self,battery_conditions,increment_battery_age_by_one_day = False):  
        """ This is an aging model for 18650 lithium-nickel-manganese-cobalt-oxide batteries.   
        
        Assumptions:
            None
        
        Source:
            None
    
        Args:
            self                                      : battery            [unitless] 
            battery_conditions                        : state of battery   [unitless]
            increment_battery_age_by_one_day (boolean): day increment flag [unitless]  
            
        Returns: 
            None
        """        
        update_nmc_cell_age(self,battery_conditions,increment_battery_age_by_one_day) 
        
        return  

def create_discharge_performance_map(raw_data):
    """ Creates discharge and charge response surface for a LiNiMnCoO2 battery cell   
        
        Assumptions:
            None
        
        Source:
            None
            
        Args:
            raw_data     : cell discharge curves                  [unitless]   
            
        Returns: 
            battery_data : response surface of battery properties [unitless]  
        """   
    # Process raw data   
    processed_data = Data() 
    processed_data.Voltage        = np.zeros((5,6,15,2)) # current , operating temperature , SOC vs voltage      
    processed_data.Temperature    = np.zeros((5,6,15,2)) # current , operating temperature , SOC vs temperature 

    # Reshape  Data          
    raw_data.Voltage 
    for i, Amps in enumerate(raw_data.Voltage):
        for j , Deg in enumerate(Amps):
            min_x    = 0 
            max_x    = max(Deg[:,0])
            x        = np.linspace(min_x,max_x,15)
            y        = np.interp(x,Deg[:,0],Deg[:,1])
            vec      = np.zeros((15,2))
            vec[:,0] = x/max_x
            vec[:,1] = y
            processed_data.Voltage[i,j,:,:]= vec   

    for i, Amps in enumerate(raw_data.Temperature):
        for j , Deg in enumerate(Amps):
            min_x    = 0   
            max_x    = max(Deg[:,0])
            x        = np.linspace(min_x,max_x,15)
            y        = np.interp(x,Deg[:,0],Deg[:,1])
            vec      = np.zeros((15,2))
            vec[:,0] = x/max_x
            vec[:,1] = y
            processed_data.Temperature[i,j,:,:]= vec  
    
    # Create performance maps  
    battery_data             = Data() 
    amps                    = np.linspace(0, 8, 5)
    temp                    = np.linspace(0, 50, 6) +  272.65
    SOC                     = np.linspace(0, 1, 15)
    battery_data.Voltage     = RegularGridInterpolator((amps, temp, SOC), processed_data.Voltage,bounds_error=False,fill_value=None)
    battery_data.Temperature = RegularGridInterpolator((amps, temp, SOC), processed_data.Temperature,bounds_error=False,fill_value=None) 
     
    return battery_data  

def load_battery_results(): 
    '''Load experimental raw data of NMC cells 
        
       Assumptions:
           Ideal gas
           
       Source:
           Automotive Industrial Systems Company of Panasonic Group, Technical Information of 
           NCR18650G, URL https://www.imrbatteries.com/content/panasonic_ncr18650g.pdf
    
       Args: 
           None
           
       Returns:
           battery_data: raw data from battery   [unitless]
    '''    
    ospath    = os.path.abspath(__file__)
    separator = os.path.sep
    rel_path  = os.path.dirname(ospath) + separator     
    return RCAIDE.load(rel_path+ 'NMC_Raw_Data.res')
