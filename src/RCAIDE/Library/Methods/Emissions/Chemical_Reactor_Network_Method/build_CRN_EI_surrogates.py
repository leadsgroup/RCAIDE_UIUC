# RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network_Method/build_CRN_EI_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import  Data 

# package imports 
from scipy.interpolate  import RegularGridInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  build_CRN_EI_surrogates
# ---------------------------------------------------------------------------------------------------------------------- 
def build_CRN_EI_surrogates(emissions):
     
    surrogates                            = emissions.surrogates
    training                              = emissions.training  
    pressure_data                         = training.pressure         
    temperature_data                      = training.temperature      
    air_mass_flowrate_data                = training.air_mass_flowrate
    fuel_to_air_ratio_data                = training.fuel_to_air_ratio

    surrogates.EI_CO2                     = RegularGridInterpolator((pressure_data ,temperature_data, air_mass_flowrate_data, fuel_to_air_ratio_data),training.EI_CO2 ,method = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.EI_CO                      = RegularGridInterpolator((pressure_data ,temperature_data, air_mass_flowrate_data, fuel_to_air_ratio_data),training.EI_CO  ,method = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.EI_H2O                     = RegularGridInterpolator((pressure_data ,temperature_data, air_mass_flowrate_data, fuel_to_air_ratio_data),training.EI_H2O ,method = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.EI_NO                      = RegularGridInterpolator((pressure_data ,temperature_data, air_mass_flowrate_data, fuel_to_air_ratio_data),training.EI_NO  ,method = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.EI_NO2                     = RegularGridInterpolator((pressure_data ,temperature_data, air_mass_flowrate_data, fuel_to_air_ratio_data),training.EI_NO2 ,method = 'linear',   bounds_error=False, fill_value=None) 
   
    return