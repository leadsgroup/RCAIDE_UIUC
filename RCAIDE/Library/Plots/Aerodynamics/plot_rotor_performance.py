## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_rotor_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Library-Plots-Performance-Aerodynamics
def plot_rotor_performance(rotor, title=None, show_figure = True,save_figure=False, save_filename='Rotor_Performance', file_type=".png"):
    """Plots a summary of rotor performance 
    
    Assumptions:
    None

    Source: 
    None
    
    Inputs
    rotor   - rotor data structure 
    
    Outputs:
    Plots

    Properties Used:
    N/A
    """
    # unpack
    outputs = rotor.outputs
    r_distribution = outputs.disc_radial_distribution[0, :, 0]
    
    # 2d plots
    fig = make_subplots(rows=2, cols=2)
    
    df1a = pd.DataFrame(dict(x=r_distribution, y=outputs.disc_axial_velocity[0, :, 0])) # label='Axial'
    df1b = pd.DataFrame(dict(x=r_distribution, y=outputs.disc_tangential_velocity[0, :, 0]))  # label='Tangential'
    df2a = pd.DataFrame(dict(x=r_distribution, y=outputs.disc_axial_induced_velocity[0, :, 0])) # label='Axial'
    df2b = pd.DataFrame(dict(x=r_distribution, y=outputs.disc_tangential_induced_velocity[0, :, 0])) # label='Tangential'
    df3  = pd.DataFrame(dict(x=r_distribution, y=outputs.disc_thrust_distribution[0, :, 0]))
    df4  = pd.DataFrame(dict(x=r_distribution, y=outputs.disc_torque_distribution[0, :, 0]))
    
    fig.append_trace(go.Line(df1a, name='Axial', legendgroup='1',showlegend=True), row=1, col=1)
    fig.append_trace(go.Line(df1b, name='Tangential', legendgroup='1',showlegend=True), row=1, col=1)
    fig.append_trace(go.Line(df2a, name='Axial', legendgroup='2',showlegend=True), row=1, col=2)    
    fig.append_trace(go.Line(df2b, name='Tangential', legendgroup='2',showlegend=True), row=1, col=2)     
    fig.append_trace(go.Line(df3, name='Thrust', legendgroup='3',showlegend=False), row=2, col=1)    
    fig.append_trace(go.Line(df4, name='Torque', legendgroup='4',showlegend=False), row=2, col=2)        
    
    fig.update_xaxes(title_text="Radial Station", row=1, col=1)
    fig.update_yaxes(title_text="Velocity", row=1, col=1)
    fig.update_xaxes(title_text="Radial Station", row=1, col=2)
    fig.update_yaxes(title_text="Induced Velocity", row=1, col=2)
    fig.update_xaxes(title_text="Radial Station", row=2, col=1)
    fig.update_yaxes(title_text="Thrust, N", row=2, col=1)
    fig.update_xaxes(title_text="Radial Station", row=2, col=2)
    fig.update_yaxes(title_text="Torque, N-m", row=2, col=2)
    
    fig.update_layout(title_text="Rotor Performance", height=700)
    
    if save_figure:
        fig.write_image(save_filename + '_2D' + file_type) 
    
    if show_figure:
        fig.write_html( save_filename + '.html', auto_open=True)
    return fig 
 