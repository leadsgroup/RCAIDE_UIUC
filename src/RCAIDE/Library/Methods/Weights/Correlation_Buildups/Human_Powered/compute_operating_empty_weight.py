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
def compute_operating_empty_weight(vehicle,settings=None):
    """ Computes weights estimates for human powered aircraft
    
    Assumptions:
       All of this is from AIAA 89-2048, units are in kg. These weight estimates
       are from the MIT Daedalus and are valid for very lightweight
       carbon fiber composite structures. This may need to be solved iteratively since
       gross weight is an input.
       
    Source: 
        MIT Daedalus
                       
    Inputs:
        wing - a data dictionary with the fields:
            Sw -       wing area                                                       [meters**2]
            bw -       wing span                                                       [meters]
            cw -       average wing chord                                              [meters]
            deltaw -   average rib spacing to average chord ratio                      [dimensionless]
            Nwr -      number of wing surface ribs (bw**2)/(deltaw*Sw)                 [dimensionless]
            t_cw -     wing airfoil thickness to chord ratio                           [dimensionless]
            Nwer -     number of wing end ribs (2*number of individual wing panels -2) [dimensionless]
            
        horizontal - a data dictionary with the fields:
            Sts -      tail surface area                                               [meters]
            bts -      tail surface span                                               [meters]
            cts -      average tail surface chord                                      [meters]
            deltawts - average rib spacing to average chord ratio                      [dimensionless]
            Ntsr -     number of tail surface ribs (bts^2)/(deltats*Sts)               [dimensionless]
            t_cts -    tail airfoil thickness to chord ratio                           [dimensionless]
            
        vertical - a data dictionary with the fields:
            Sts -      tail surface area                                               [meters]
            bts -      tail surface span                                               [meters]
            cts -      average tail surface chord                                      [meters]
            deltawts - average rib spacing to average chord ratio                      [dimensionless]
            Ntsr -     number of tail surface ribs (bts**2)/(deltats*Sts)              [dimensionless]
            t_cts -    tail airfoil thickness to chord ratio                           [dimensionless]
            
        aircraft - a data dictionary with the fields:    
            nult -     ultimate load factor                                            [dimensionless]
            GW -       aircraft gross weight                                           [kilogram]
            qm -       dynamic pressure at maneuvering speed                           [Pascals]
            Ltb -      tailboom length                                                 [meters]
    
    Outputs:
        Wws -      weight of wing spar                                                 [kilogram]
        Wtss -     weight of tail surface spar                                         [kilogram]
        Wwr -      weight of wing ribs                                                 [kilogram]
        Wtsr -     weight of tail surface ribs                                         [kilogram]
        Wwer -     weight of wing end ribs                                             [kilogram]
        WwLE -     weight of wing leading edge                                         [kilogram]
        WtsLE -    weight of tail surface leading edge                                 [kilogram]
        WwTE -     weight of wing trailing edge                                        [kilogram]
        Wwc -      weight of wing covering                                             [kilogram]
        Wtsc -     weight of tail surface covering                                     [kilogram]
        Wtb -      tailboom weight                                                     [kilogram]
                
    Properties Used:
        N/A
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