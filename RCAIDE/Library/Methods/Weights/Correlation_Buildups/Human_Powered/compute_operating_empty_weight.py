# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Human_Powered/compute_operating_empty_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import  RCAIDE
from RCAIDE.Framework.Core import Data 
from .  import compute_fuselage_weight
from .  import compute_tail_weight
from .  import compute_wing_weight 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Vertical Tail Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle, settings=None):
    """
    Computes operating empty weight for human-powered aircraft using MIT Daedalus 
    correlations. Integrates weights of all major structural components.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle instance containing:
            - wings : list
                Aircraft wings with:
                    - areas.reference : float
                        Wing area [m²]
                    - spans.projected : float
                        Wing span [m]
                    - chords.mean_aerodynamic : float
                        Mean chord [m]
                    - number_ribs : int
                        Number of wing ribs
                    - thickness_to_chord : float
                        t/c ratio
                    - number_end_ribs : int
                        Number of wing end ribs
            - flight_envelope : FlightEnvelope
                - ultimate_load : float
                    Ultimate load factor
                - maximum_dynamic_pressure : float
                    Maximum dynamic pressure [Pa]
            - mass_properties : MassProperties
                - max_takeoff : float
                    Maximum takeoff weight [kg]
            - Ltb : float
                Tailboom length [m]
    settings : Settings, optional
        Configuration settings (not used in this method)

    Returns
    -------
    output : Data
        Container with weight breakdown:
            - empty : Data
                - structural : Data
                    - wings : float
                        Total wing structure weight [kg]
                    - fuselage : float
                        Fuselage structure weight [kg]
                - total : float
                    Total operating empty weight [kg]

    Notes
    -----
    Uses empirical correlations developed from the MIT Daedalus human-powered aircraft project.

    **Major Assumptions**
        * Ultra-lightweight carbon fiber composite construction
        * Minimal structural margins
        * Simple tubular structures
        * No pressurization requirements
        * Single-pilot configuration
        * Low-speed flight regime
        * Weight must be solved iteratively since gross weight is an input

    **Theory**
    Total weight is computed by summing:
        * Main wing weight (including ribs, spars, covering)
        * Horizontal tail weight
        * Vertical tail weight
        * Fuselage/tailboom weight

    Each component uses specialized correlations accounting for:
        * Minimum gauge constraints
        * Basic systems integration
        * Structural load paths
        * Assembly requirements

    References
    ----------
    [1] Langford, J. "The Daedalus project - A summary of lessons learned", 
        AIAA Paper 89-2048, 1989.

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_wing_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_tail_weight
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_fuselage_weight
    """ 
    
    #Unpack
    
    nult   = vehicle.flight_envelope.ultimate_load
    gw     = vehicle.mass_properties.max_takeoff
    qm     = vehicle.flight_envelope.maximum_dynamic_pressure
    
    for wing in vehicle.wings:
        if isinstance(wing,RCAIDE.Library.Components.Wings.Main_Wing):
            Sw      = wing.areas.reference
            bw      = wing.spans.projected
            cw      = wing.chords.mean_aerodynamic
            Nwr     = wing.number_ribs
            t_cw    = wing.thickness_to_chord
            Nwer    = wing.number_end_ribs
            W_wing = compute_wing_weight(Sw,bw,cw,Nwr,t_cw,Nwer,nult,gw)
            wing.mass_properties.mass = W_wing
    
        # Horizontal Tail weight
        elif isinstance(wing,RCAIDE.Library.Components.Wings.Horizontal_Tail): 
            S_h    = wing.areas.reference
            b_h    = wing.spans.projected
            chs    = wing.chords.mean_aerodynamic
            Nhsr   = wing.number_ribs
            t_ch   = wing.thickness_to_chord
            W_ht  = compute_tail_weight(S_h,b_h,chs,Nhsr,t_ch,qm)
            wing.mass_properties.mass = W_ht

        # Vertical Tail weight 
        elif isinstance(wing,RCAIDE.Library.Components.Wings.Vertical_Tail):     
            S_v    = wing.areas.reference
            b_v    = wing.spans.projected
            cvs    = wing.chords.mean_aerodynamic
            Nvsr   = wing.number_ribs
            t_cv   = wing.thickness_to_chord
            W_vt   = compute_tail_weight(S_v,b_v,cvs,Nvsr,t_cv,qm)
            wing.mass_properties.mass = W_vt

    for fuselage in vehicle.fuselages: 
        Ltb     = vehicle.Ltb  
        W_tb   = compute_fuselage_weight(S_h,qm,Ltb)
        fuselage.mass_properties.mass = W_tb
    
    output                                  = Data()
    output.empty                            = Data()  
    output.empty.structural                 =  Data()
    output.empty.structural.wings           = W_wing +  W_ht +  W_vt
    output.empty.structural.fuselage        = W_tb  
    output.empty.total = W_ht + W_tb + W_vt + W_wing
    
    return output