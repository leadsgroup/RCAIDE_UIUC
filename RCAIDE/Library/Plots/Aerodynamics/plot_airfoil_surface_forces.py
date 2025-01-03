## @ingroup Library-Plots-Performance-Aerodynamics  
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_airfoil_surface_forces.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 
from RCAIDE.Framework.Core import Units  
import matplotlib.pyplot as plt    

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------     
def plot_airfoil_surface_forces(ap, 
                              save_figure = False, 
                              arrow_color = 'red',
                              save_filename = 'Airfoil_Cp_Distribution', 
                              show_figure = True, 
                              file_type = ".png"):
    """
    Generate plots showing pressure forces on airfoil surface using arrows.

    Parameters
    ----------
    ap : Data
        Airfoil properties data structure containing:
            - x : array
                Airfoil surface x-coordinates
            - y : array
                Airfoil surface y-coordinates
            - cp : array
                Pressure coefficients at surface points
            - normals : array
                Surface normal vectors [nx, ny]
            - AoA : array
                Angles of attack [rad]
            - Re : array
                Reynolds numbers

    save_figure : bool, optional
        Save figure to file if True, default False

    arrow_color : str, optional
        Color specification for force arrows, default 'red'

    save_filename : str, optional
        Name for saved figure file, default 'Airfoil_Cp_Distribution'

    show_figure : bool, optional
        Display figure if True, default True

    file_type : str, optional
        File extension for saved figure, default ".png"

    Returns
    -------
    fig : matplotlib.figure.Figure

    Notes
    -----
    Creates a figure showing:
        - Airfoil profile
        - Pressure force vectors as arrows normal to surface
        - Arrow length proportional to local pressure coefficient
        - Arrows point inward for negative Cp (suction)
        - Arrows point outward for positive Cp (pressure)

    A separate figure is created for each combination of angle of
    attack and Reynolds number.

    **Definitions**
    
    'Surface Normal'
        Unit vector perpendicular to airfoil surface

    See Also
    --------
    RCAIDE.Library.Plots.Common.set_axes : Standardized axis formatting
    RCAIDE.Library.Analysis.Aerodynamics.compute_pressure_forces : Analysis module
    """        
    
    # determine dimension of angle of attack and reynolds number 
    n_cpts   = len(ap.AoA)
    nAoA     = len(ap.AoA[0])
    n_pts    = len(ap.x[0,0,:])- 1 
     

    for i in range(n_cpts):     
        for j in range(nAoA): 
            label =  '_AoA_' + str(round(ap.AoA[i][j]/Units.degrees,2)) + '_deg_Re_' + str(round(ap.Re[i][j]/1000000,2)) + 'E6'
            fig   = plt.figure('Airfoil_Pressure_Normals' + label )
            axis = fig.add_subplot(1,1,1) 
            axis.plot(ap.x[0,0,:], ap.y[0,0,:],'k-')   
            for k in range(n_pts):
                dx_val = ap.normals[i,j,k,0]*abs(ap.cp[i,j,k])*0.1
                dy_val = ap.normals[i,j,k,1]*abs(ap.cp[i,j,k])*0.1
                if ap.cp[i,j,k] < 0:
                    plt.arrow(x= ap.x[i,j,k], y=ap.y[i,j,k] , dx= dx_val , dy = dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
                else:
                    plt.arrow(x= ap.x[i,j,k]+dx_val , y= ap.y[i,j,k]+dy_val , dx= -dx_val , dy = -dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
    
    
    return fig 

