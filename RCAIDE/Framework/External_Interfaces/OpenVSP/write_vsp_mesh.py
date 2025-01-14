# write_vsp_mesh.py
# 
# Created:  Oct 2016, T. MacDonald
# Modified: Jan 2017, T. MacDonald
#           Feb 2017, T. MacDonald
#           Jan 2019, T. MacDonald
#           Jan 2020, T. MacDonald

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
import numpy as np
import time
import fileinput

# ---------------------------------------------------------------------------------------------------------------------- 
# write_vsp_mesh
# ---------------------------------------------------------------------------------------------------------------------- 
def write_vsp_mesh(geometry, tag, half_mesh_flag, growth_ratio, growth_limiting_flag):
    """
    Creates an STL surface mesh of a vehicle using OpenVSP

    Parameters
    ----------
    geometry : RCAIDE.Vehicle
        Vehicle to mesh, containing:
        - wings.main_wing.chords.mean_aerodynamic [m]
        - Other components with meshing sources
    tag : str
        Base name for output files
    half_mesh_flag : bool
        Whether to create a symmetry plane
    growth_ratio : float
        Growth ratio for mesh cell sizes
    growth_limiting_flag : bool
        Whether to use 3D growth limiting

    Returns
    -------
    None
        Creates output files:
        - <tag>.stl : Surface mesh
        - <tag>.key : Component key file
        - <tag>_premesh.vsp3 : VSP file with mesh settings

    Notes
    -----
    This function sets up and runs OpenVSP's CFD meshing to create a surface
    mesh suitable for CFD analysis.

    **Major Assumptions**
    * Vehicle geometry is suitable for meshing
    * Main wing is defined with mean aerodynamic chord
    * Component sources are properly defined
    * Mesh settings are appropriate for the geometry

    **Extra modules required**
    * OpenVSP (vsp or openvsp module)
    """
    
    # Reset OpenVSP to avoid including a previous vehicle
    vsp.ClearVSPModel()
    
    if 'turbofan' in geometry.networks:
        print('Warning: no meshing sources are currently implemented for the nacelle')

    # Turn on symmetry plane splitting to improve robustness of meshing process
    if half_mesh_flag == True:
        f = fileinput.input(tag + '.vsp3',inplace=1)
        for line in f:
            if 'SymmetrySplitting' in line:
                print(line[0:34] + '1' + line[35:-1])
            else:
                print(line)
    
    vsp.ReadVSPFile(tag + '.vsp3')
    
    # Set output file types and what will be meshed
    file_type = vsp.CFD_STL_TYPE + vsp.CFD_KEY_TYPE
    set_int   = vsp.SET_ALL

    vsp.SetComputationFileName(vsp.CFD_STL_TYPE, tag + '.stl')
    vsp.SetComputationFileName(vsp.CFD_KEY_TYPE, tag + '.key')
    
    # Set to create a tagged STL mesh file
    vehicle_cont = vsp.FindContainer('Vehicle',0)
    STL_multi    = vsp.FindParm(vehicle_cont, 'MultiSolid', 'STLSettings')
    vsp.SetParmVal(STL_multi, 1.0)
    
    vsp.SetCFDMeshVal(vsp.CFD_FAR_FIELD_FLAG,1)
    if half_mesh_flag == True:
        vsp.SetCFDMeshVal(vsp.CFD_HALF_MESH_FLAG,1)
        
    # Figure out the size of the bounding box
    vehicle_id = vsp.FindContainersWithName('Vehicle')[0]
    xlen = vsp.GetParmVal(vsp.FindParm(vehicle_id,"X_Len","BBox"))
    ylen = vsp.GetParmVal(vsp.FindParm(vehicle_id,"Y_Len","BBox"))
    zlen = vsp.GetParmVal(vsp.FindParm(vehicle_id,"Z_Len","BBox"))
    
    # Max length
    max_len = np.max([xlen,ylen,zlen])
    far_length = 10.*max_len
        
    vsp.SetCFDMeshVal(vsp.CFD_FAR_SIZE_ABS_FLAG,1)
    vsp.SetCFDMeshVal(vsp.CFD_FAR_LENGTH,far_length)
    vsp.SetCFDMeshVal(vsp.CFD_FAR_WIDTH,far_length)
    vsp.SetCFDMeshVal(vsp.CFD_FAR_HEIGHT,far_length)    
    vsp.SetCFDMeshVal(vsp.CFD_FAR_MAX_EDGE_LEN, max_len)
    vsp.SetCFDMeshVal(vsp.CFD_GROWTH_RATIO, growth_ratio)
    if growth_limiting_flag == True:
        vsp.SetCFDMeshVal(vsp.CFD_LIMIT_GROWTH_FLAG, 1.0)
    
    # Set the max edge length so we have on average 50 elements per chord length
    MAC     = geometry.wings.main_wing.chords.mean_aerodynamic
    min_len = MAC/50.
    vsp.SetCFDMeshVal(vsp.CFD_MAX_EDGE_LEN,min_len)
    
    # vsp.AddDefaultSources()   
    set_sources(geometry)
    
    vsp.Update()
    
    vsp.WriteVSPFile(tag + '_premesh.vsp3')
    
    print('Starting mesh for ' + tag + ' (This may take several minutes)')
    ti = time.time()
    vsp.ComputeCFDMesh(set_int,file_type)
    tf = time.time()
    dt = tf-ti
    print('VSP meshing for ' + tag + ' completed in ' + str(dt) + ' s')
    
# ----------------------------------------------------------------------------------------------------------------------     
# set_sources
# ---------------------------------------------------------------------------------------------------------------------- 
def set_sources(geometry):
    """
    Sets mesh sources on vehicle components

    Parameters
    ----------
    geometry : RCAIDE.Vehicle
        Vehicle containing components that need mesh sources:
        
        wings.*.
            - tag : str
            - Segments.*.percent_span_location : float
            - Segments.*.root_chord_percent : float
            - chords.root : float
            - chords.tip : float
            - vsp_mesh : optional settings
        
        fuselages.*.
            - tag : str
            - vsp_mesh.length : float (optional)
            - vsp_mesh.radius : float (optional)
            - lengths.total : float

    Notes
    -----
    Creates mesh sources similar to OpenVSP defaults but allows custom
    source parameters through the vsp_mesh attribute.

    **Major Assumptions**
    * Components can be identified by their tags
    * Wing segments cover full span if defined
    * Source parameters are appropriate for the geometry
    """     
    # Extract information on geometry type (for some reason it seems VSP doesn't have a simple 
    # way to do this)
    comp_type_dict = dict()
    comp_dict      = dict()
    for wing in geometry.wings:
        comp_type_dict[wing.tag] = 'wing'
        comp_dict[wing.tag] = wing
    for fuselage in geometry.fuselages:
        comp_type_dict[fuselage.tag] = 'fuselage'
        comp_dict[fuselage.tag] = fuselage
    # network sources have not been implemented
    #for network in geometry.networks:
        #comp_type_dict[network.tag] = 'turbojet'
        #comp_dict[network.tag] = network
        
    components = vsp.FindGeoms()
    
    # The default source values are (mostly) based on the OpenVSP scripts, wing for example:
    # https://github.com/OpenVSP/OpenVSP/blob/a5ac5302b320e8e318830663bb50ba0d4f2d6f64/src/geom_core/WingGeom.cpp
    
    for comp in components:
        comp_name = vsp.GetGeomName(comp)
        if comp_name not in comp_dict:
            continue
        comp_type = comp_type_dict[comp_name]
        # Nacelle sources are not implemented
        #if comp_name[0:8] == 'turbofan':
            #comp_type = comp_type_dict[comp_name[0:8]]
        #else:
            #comp_type = comp_type_dict[comp_name]
        if comp_type == 'wing':
            wing = comp_dict[comp_name]
            if len(wing.segments) == 0: # check if segments exist
                num_secs = 1
                use_base = True
            else:
                if wing.segments[0].percent_span_location == 0.: # check if first segment starts at the root
                    num_secs = len(wing.segments)
                    use_base = False
                else:
                    num_secs = len(wing.segments) + 1
                    use_base = True
                    
            u_start = 0.
            base_root = wing.chords.root
            base_tip  = wing.chords.tip            
            for ii in range(0,num_secs):
                if (ii==0) and (use_base == True): # create sources on root segment
                    cr = base_root
                    if len(wing.segments) > 0:
                        ct = base_root  * wing.segments[0].root_chord_percent
                        seg = wing.segments[ii]
                    else:
                        if 'vsp_mesh' in wing:
                            custom_flag = True
                        else:
                            custom_flag = False
                        ct = base_tip           
                        seg = wing
                    # extract CFD source parameters
                    if len(wing.segments) == 0:
                        wingtip_flag = True
                    else:
                        wingtip_flag = False
                    add_segment_sources(comp,cr, ct, ii, u_start, num_secs, custom_flag, 
                                  wingtip_flag,seg)                        
                elif (ii==0) and (use_base == False): 
                    cr = base_root * wing.segments[0].root_chord_percent
                    if num_secs > 1:
                        ct = base_root  * wing.segments[1].root_chord_percent
                    else:
                        ct = base_tip
                    # extract CFD source parameters
                    seg = wing.segments[ii]
                    if 'vsp_mesh' in wing.segments[ii]:
                        custom_flag = True
                    else:
                        custom_flag = False
                    wingtip_flag = False
                    add_segment_sources(comp,cr, ct, ii, u_start, num_secs, custom_flag, 
                                  wingtip_flag,seg)
                elif ii < num_secs - 1:
                    if use_base == True:
                        jj = 1
                    else:
                        jj = 0
                    cr = base_root * wing.segments[ii-jj].root_chord_percent
                    ct = base_root * wing.segments[ii+1-jj].root_chord_percent
                    seg = wing.segments[ii-jj]
                    if 'vsp_mesh' in wing.segments[ii-jj]:
                        custom_flag = True
                    else:
                        custom_flag = False
                    wingtip_flag = False
                    add_segment_sources(comp,cr, ct, ii, u_start, num_secs, custom_flag, 
                                  wingtip_flag,seg)                   
                else:     
                    if use_base == True:
                        jj = 1
                    else:
                        jj = 0                    
                    cr = base_root * wing.segments[ii-jj].root_chord_percent
                    ct = base_tip
                    seg = wing.segments[ii-jj]
                    if 'vsp_mesh' in wing.segments[ii-jj]:
                        custom_flag = True
                    else:
                        custom_flag = False
                    wingtip_flag = True
                    add_segment_sources(comp,cr, ct, ii, u_start, num_secs, custom_flag, 
                                  wingtip_flag,seg)  
                pass
                    
        elif comp_type == 'fuselage':
            fuselage = comp_dict[comp_name]
            if 'vsp_mesh' in fuselage:
                len1 = fuselage.vsp_mesh.length
                rad1 = fuselage.vsp_mesh.radius
            else:
                len1 = 0.1 * 0.5 # not sure where VSP is getting this value
                rad1 = 0.2 * fuselage.lengths.total
            uloc = 0.0
            wloc = 0.0
            vsp.AddCFDSource(vsp.POINT_SOURCE,comp,0,len1,rad1,uloc,wloc) 
            uloc = 1.0
            vsp.AddCFDSource(vsp.POINT_SOURCE,comp,0,len1,rad1,uloc,wloc) 
            pass
        
        # This is a stub for the nacelle implementation. It will create sources
        # as is but they will not be appropriate for the nacelle shape.
        
        #elif comp_type == 'turbofan':
            #network = comp_dict[comp_name[0:8]]
            #if network.has_key('vsp_mesh'):
                #len1 = network.vsp_mesh.length
                #rad1 = network.vsp_mesh.radius
            #else:
                #len1 = 0.1 * 0.5 # not sure where VSP is getting this value
            #uloc = 0.0
            #wloc = 0.0
            #vsp.AddCFDSource(vsp.POINT_SOURCE,comp,0,len1,rad1,uloc,wloc) 
            #uloc = 1.0
            #vsp.AddCFDSource(vsp.POINT_SOURCE,comp,0,len1,rad1,uloc,wloc) 
            #pass        
    
            
# ----------------------------------------------------------------------------------------------------------------------         
# add_segment_sources
# ---------------------------------------------------------------------------------------------------------------------- 
def add_segment_sources(comp, cr, ct, ii, u_start, num_secs, custom_flag, wingtip_flag, seg):
    """
    Adds mesh sources to a wing segment

    Parameters
    ----------
    comp : str
        OpenVSP component ID
    cr : float
        Root chord length [m]
    ct : float
        Tip chord length [m]
    ii : int
        Segment index
    u_start : float
        Starting u-coordinate
    num_secs : int
        Number of sections
    custom_flag : bool
        Whether to use custom source parameters
    wingtip_flag : bool
        Whether this is a wingtip segment
    seg : RCAIDE.Library.Components.Wings.Segment
        Wing segment containing optional vsp_mesh parameters

    Notes
    -----
    Creates line sources along segment leading/trailing edges with
    appropriate sizing parameters.

    **Major Assumptions**
    * Source parameters scale with chord length if not custom
    * Segment geometry is suitable for line sources
    * Custom parameters are properly defined if used
    """     
    if custom_flag == True:
        len1 = seg.vsp_mesh.inner_length
        len2 = seg.vsp_mesh.outer_length
        rad1 = seg.vsp_mesh.inner_radius
        rad2 = seg.vsp_mesh.outer_radius
    else:
        len1 = 0.01 * cr
        len2 = 0.01 * ct
        rad1 = 0.2 * cr
        rad2 = 0.2 * ct
    uloc1 = ((ii+1)+u_start-1 +1)/(num_secs+2) # index additions are shown explicitly for cross-referencing with VSP code
    wloc1 = 0.5
    uloc2 = ((ii+1)+u_start +1)/(num_secs+2)
    wloc2 = 0.5
    vsp.AddCFDSource(vsp.LINE_SOURCE,comp,0,len1,rad1,uloc1,wloc1,len2,rad2,uloc2,wloc2)
    wloc1 = 0.
    wloc2 = 0.
    TE_match = True
    if (custom_flag == True) and ('matching_TE' in seg.vsp_mesh):
        if seg.vsp_mesh.matching_TE == False: # use default values if so
            vsp.AddCFDSource(vsp.LINE_SOURCE,comp,0,0.01 * cr,0.2 * cr,uloc1,wloc1,0.01 * ct,0.2 * ct,uloc2,wloc2) 
            TE_match = False
        else:
            vsp.AddCFDSource(vsp.LINE_SOURCE,comp,0,len1,rad1,uloc1,wloc1,len2,rad2,uloc2,wloc2)
    else:
        vsp.AddCFDSource(vsp.LINE_SOURCE,comp,0,len1,rad1,uloc1,wloc1,len2,rad2,uloc2,wloc2)  
    if wingtip_flag == True:
        len1 = len2
        rad1 = rad2
        wloc1 = 0.0
        wloc2 = 0.5
        uloc1 = uloc2
        if TE_match == False: # to match not custom TE if indicated
            len1 = 0.01 * ct
            rad1 = 0.2 * ct
        vsp.AddCFDSource(vsp.LINE_SOURCE,comp,0,len1,rad1,uloc1,wloc1,len2,rad2,uloc2,wloc2)    
    
if __name__ == '__main__':
    write_vsp_mesh(tag,True)
