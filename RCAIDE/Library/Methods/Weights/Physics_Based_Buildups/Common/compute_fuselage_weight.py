# RCAIDE/Library/Methods/Weights/Buildups/Common/compute_fuselage_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# RCAIDE imports   
from RCAIDE.Library.Attributes.Materials import Bidirectional_Carbon_Fiber, Carbon_Fiber_Honeycomb, Paint, Unidirectional_Carbon_Fiber, Acrylic, Steel

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute boom weight
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_fuselage_weight(fuse, maxSpan, MTOW, maximum_g_load=3.8, landing_impact_factor=3.5, safety_factor=1.5):
    """
    Calculates the structural mass of a fuselage for an eVTOL vehicle using a physics-based approach that considers 
    bending moments, torsional loads, and material properties.

    Parameters
    ----------
    fuse : RCAIDE.Components.Fuselages.Fuselage()
        Fuselage data structure
            - lengths.total : float
                Total length of fuselage [m]
            - width : float
                Maximum width of fuselage [m]
            - heights.maximum : float
                Maximum height of fuselage [m]
            - keel_materials : Data()
                Material properties for structural keel
                    - root_bending_moment_carrier : Material()
                        Material for primary bending loads
                    - shear_carrier : Material()
                        Material for shear loads
                    - bearing_carrier : Material()
                        Material for bearing loads
            - materials.bolt_materials.landing_pad_bolt : Material()
                Material properties for landing gear attachment bolts
            - skin_materials : list
                List of materials used in fuselage skin
            - canopy_materials : list
                List of materials used in canopy
    maxSpan : float
        Maximum wingspan [m]
    MTOW : float
        Maximum takeoff weight [kg]
    maximum_g_load : float, optional
        Maximum load factor during flight (default 3.8)
    landing_impact_factor : float, optional
        Maximum load multiplier on landing (default 3.5)
    safety_factor : float, optional
        Design safety factor (default 1.5)

    Returns
    -------
    weight : float
        Total fuselage structural weight [kg]

    Notes
    -----
    The function calculates weight contributions from multiple components including skin, 
    bulkheads, canopy, and structural keel.

    **Major Assumptions**
        * Structural keel takes primary bending and torsional loads
        * Ellipsoid approximation for fuselage wetted area
        * If materials not specified, defaults to:
            - Unidirectional carbon fiber for root bending
            - Bidirectional carbon fiber for shear and bearing
            - Steel for landing pad bolts
            - Standard composite stack for skin (1.2995 kg/m²)
            - Acrylic for canopy (3.7465 kg/m²)

    **Theory**
    Key calculations include:
    .. math::
        S_{wet} = 4\\pi * (\\frac{(L*W/4)^{1.6} + (L*H/4)^{1.6} + (W*H/4)^{1.6}}{3})^{1/1.6}

        L_{max} = N_{g} * MTOW * g * SF

        M_{lift} = L_{max} * L/2

        M_{bend} = L_{max}/2 * span/2

    where:
        - :math:`S_{wet}` = wetted area
        - :math:`L_{max}` = maximum lift load
        - :math:`M_{lift}` = lifting moment
        - :math:`M_{bend}` = bending moment

    References
    ----------
    [1] Project Vahana Conceptual Trade Study

    See Also
    --------
    RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport.compute_fuselage_weight
    RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common.compute_boom_weight
    """

    #-------------------------------------------------------------------------------
    # Unpack Inputs
    #------------------------------------------------------------------------------- 
    fLength = fuse.lengths.total
    fWidth  = fuse.width
    fHeight = fuse.heights.maximum
    G_max   = maximum_g_load
    LIF     = landing_impact_factor
    SF      = safety_factor

    #-------------------------------------------------------------------------------
    # Unpack Material Properties
    #-------------------------------------------------------------------------------

    try:
        rbmMat = fuse.keel_materials.root_bending_moment_carrier
    except AttributeError:
        rbmMat = Unidirectional_Carbon_Fiber()
    rbmDen = rbmMat.density
    rbmUTS = rbmMat.ultimate_tensile_strength

    try:
        shearMat = fuse.keel_materials.shear_carrier
    except AttributeError:
        shearMat = Bidirectional_Carbon_Fiber()
    shearDen = shearMat.density
    shearUSS = shearMat.ultimate_shear_strength

    try:
        bearingMat = fuse.keel_materials.bearing_carrier
    except AttributeError:
        bearingMat = Bidirectional_Carbon_Fiber()
    bearingDen = bearingMat.density
    bearingUBS = bearingMat.ultimate_bearing_strength

    try:
        boltMat = fuse.materials.bolt_materials.landing_pad_bolt
    except AttributeError:
        boltMat = Steel()
    boltUSS = boltMat.ultimate_shear_strength


    # Calculate Skin & Canopy Weight Per Unit Area (arealWeight) based on material

    try:
        skinArealWeight = np.sum([(mat.minimum_gage_thickness * mat.density) for mat in fuse.skin_materials])
    except AttributeError:
        skinArealWeight = 1.2995 # Stack of bidirectional CFRP, Honeycomb Core, Paint

    try:
        canopyArealWeight = np.sum([(mat.minimum_gage_thickness * mat.density) for mat in fuse.canopy_materials])
    except AttributeError:
        canopyArealWeight = 3.7465 # Acrylic

    # Calculate fuselage area (using assumption of ellipsoid), and weight:

    S_wet = 4 * np.pi * (((fLength * fWidth/4)**1.6
        + (fLength * fHeight/4)**1.6
        + (fWidth * fHeight/4)**1.6)/3)**(1/1.6)
    skinMass = S_wet * skinArealWeight

    # Calculate the mass of a structural bulkhead

    bulkheadMass = 3 * np.pi * fHeight * fWidth/4 * skinArealWeight

    # Calculate the mass of a canopy

    canopyMass = S_wet/8 * canopyArealWeight

    # Calculate keel mass needed to carry lifting moment

    L_max       = G_max * MTOW * 9.8 * SF  # Max Lifting Load
    M_lift      = L_max * fLength/2.       # Max Moment Due to Lift
    beamWidth   = fWidth/3.                # Allowable Keel Width
    beamHeight  = fHeight/10.              # Allowable Keel Height

    beamArea    = M_lift * beamHeight/(4*rbmUTS*(beamHeight/2)**2)
    massKeel    = beamArea * fLength * rbmDen

    # Calculate keel mass needed to carry wing bending moment shear

    M_bend      = L_max/2 * maxSpan/2                           # Max Bending Moment
    beamArea    = beamHeight * beamWidth                        # Enclosed Beam Area
    beamThk     = 0.5 * M_bend/(shearUSS * beamArea)            # Beam Thickness
    massKeel   += 2*(beamHeight + beamWidth)*beamThk*shearDen

    # Calculate keel mass needed to carry landing impact load assuming

    F_landing   = SF * MTOW * 9.8 * LIF * 0.6403        # Side Landing Force
    boltArea    = F_landing/boltUSS                     # Required Bolt Area
    boltDiam    = 2 * np.sqrt(boltArea/np.pi)           # Bolt Diameter
    lamThk      = F_landing/(boltDiam*bearingUBS)       # Laminate Thickness
    lamVol      = (np.pi*(20*lamThk)**2)*(lamThk/3)     # Laminate Pad volume
    massKeel   += 4*lamVol*bearingDen                   # Mass of 4 Pads

    # Calculate total mass as the sum of skin mass, bulkhead mass, canopy pass,
    # and keel mass. Called weight by RCAIDE convention

    weight = skinMass + bulkheadMass + canopyMass + massKeel

    return weight