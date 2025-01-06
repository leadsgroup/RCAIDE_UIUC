# RCAIDE/Library/Plots/Aerodynamics/plot_rotor_disc_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units

# python imports   
import matplotlib.pyplot as plt 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------      
def plot_rotor_disc_performance(prop, outputs, i=0, title=None, save_figure=False):
    """
    Generate plots of rotor disc aerodynamic performance distributions.

    Parameters
    ----------
    prop : Data
        Rotor properties data structure

    outputs : Data
        Rotor analysis outputs containing:

        - disc_azimuthal_distribution : array
            Azimuthal angles around disc [rad]
        - disc_radial_distribution : array
            Radial positions on disc [m]
        - disc_thrust_distribution : array
            Local thrust distribution
        - disc_torque_distribution : array
            Local torque distribution
        - disc_effective_angle_of_attack : array
            Local effective angle of attack [rad]
        - disc_axial_induced_velocity : array
            Local axial induced velocity [m/s]
        - disc_tangential_induced_velocity : array
            Local tangential induced velocity [m/s]

    i : int, optional
        Time index for plotting, default 0

    title : str, optional
        Custom plot title, default None

    save_figure : bool, optional
        Save figure to file if True, default False

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure containing five polar subplots:

        - Thrust distribution
        - Torque distribution
        - Local blade angle
        - Axial velocity
        - Tangential velocity

    Notes
    -----
    All plots use:

    - Polar coordinates (azimuth, radius)
    - Jet colormap for contours
    - Consistent number of contour levels
    - Colorbar showing scale

    **Definitions**

    'Thrust Distribution'
        Local thrust force per unit area
    
    'Torque Distribution'
        Local torque per unit area
    
    'Effective Angle'
        Local blade angle relative to inflow
    
    'Induced Velocity'
        Flow velocity induced by rotor
    """
     
    # Now plotting:
    psi  = outputs.disc_azimuthal_distribution[i,:,:]
    r    = outputs.disc_radial_distribution[i,:,:]
    psi  = np.append(psi,np.atleast_2d(np.ones_like(psi[:,0])).T*2*np.pi,axis=1)
    r    = np.append(r,np.atleast_2d(r[:,0]).T,axis=1)
    
    T    = outputs.disc_thrust_distribution[i]
    Q    = outputs.disc_torque_distribution[i]
    alf  = (outputs.disc_effective_angle_of_attack[i])/Units.deg
    va   = outputs.disc_axial_induced_velocity[i]
    vt   = outputs.disc_tangential_induced_velocity[i]
        
    
    T    = np.append(T,np.atleast_2d(T[:,0]).T,axis=1)
    Q    = np.append(Q,np.atleast_2d(Q[:,0]).T,axis=1)
    alf  = np.append(alf,np.atleast_2d(alf[:,0]).T,axis=1)
    
    va   = np.append(va, np.atleast_2d(va[:,0]).T, axis=1)
    vt   = np.append(vt, np.atleast_2d(vt[:,0]).T, axis=1)
    
    lev = 101
    cm  = 'jet'
    
    # plot the grid point velocities
    fig  = plt.figure(figsize=(12,8))
    ax0  = fig.add_subplot(231, polar=True)
    p0   = ax0.contourf(psi, r, T,lev,cmap=cm)
    ax0.set_title('Thrust Distribution',pad=15)      
    ax0.set_rorigin(0)
    ax0.set_yticklabels([])
    plt.colorbar(p0, ax=ax0)
     
    ax1  = fig.add_subplot(232, polar=True)   
    p1   = ax1.contourf(psi, r, Q,lev,cmap=cm) 
    ax1.set_title('Torque Distribution',pad=15) 
    ax1.set_rorigin(0)
    ax1.set_yticklabels([])    
    plt.colorbar(p1, ax=ax1)
     
    ax2  = fig.add_subplot(233, polar=True)       
    p2   = ax2.contourf(psi, r, alf,lev,cmap=cm) 
    ax2.set_title('Local Blade Angle (deg)',pad=15) 
    ax2.set_rorigin(0)
    ax2.set_yticklabels([])
    plt.colorbar(p2, ax=ax2)
 
    ax3  = fig.add_subplot(234, polar=True)       
    p3   = ax3.contourf(psi, r, va,lev,cmap=cm) 
    ax3.set_title('Axial Velocity',pad=15) 
    ax3.set_rorigin(0)
    ax3.set_yticklabels([])
    plt.colorbar(p3, ax=ax3)    
     
    ax4  = fig.add_subplot(235, polar=True)       
    p4   = ax4.contourf(psi, r, vt,lev,cmap=cm) 
    ax4.set_title('Tangential Velocity',pad=15) 
    ax4.set_rorigin(0)
    ax4.set_yticklabels([])
    plt.colorbar(p4, ax=ax4)    
  
    return fig 