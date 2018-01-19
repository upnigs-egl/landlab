"""
This module produces two figures representing landscapes with different 
relative process rates, particularly diffusion vs run-off. 
The landscape evolution model has uplift, linear diffusion, and run-off components. 

Settings for (1)Grid , (2)uplift rate, (4)run-off, and (5)Model run are constant. 
Settings for (3)linear diffusion are varied to get different
relative process rates for the two figures. 
"""

from landlab.components import LinearDiffuser,FlowRouter, FastscapeEroder
from landlab.plot import imshow_grid
from landlab import RasterModelGrid, CLOSED_BOUNDARY, FIXED_VALUE_BOUNDARY,FIXED_GRADIENT_BOUNDARY
import matplotlib.pyplot as plt#import figure, show, plot, xlabel, ylabel, title,legend,subplots
import numpy as np
import seaborn as sn
import matplotlib as mpl


#set plot defaults
mpl.rcParams['ytick.labelsize'] = 'x-small'
mpl.rcParams['xtick.labelsize'] = 'x-small'
mpl.rcParams['axes.labelsize'] = 'small'
mpl.rcParams['axes.titlesize'] = 'large'
mpl.rcParams['legend.fontsize'] = 'x-small'

#1) grid
nrows=25
ncols=25
nodeint=0.02      # in km 

#2) uplift rate
uplift_rate=0.0001 
rock_density=2.7
sed_density=2.7

#3) linear diffusion
lin_dif=0.0001

#4) run-off
K_sp=0.3
m_sp=0.5
n_sp=1.

#5)model run
total_t=150            #number of years (000)
dt=0.4                 #number of years (000)  
nt=int(total_t // dt)   #number of time steps 

#6) random seed
randno=23456


#GRID SET-UP
#create model x-y grid    
mg = RasterModelGrid((ncols, nrows), nodeint)
#initialize with zero elevation values and random noise
z = mg.add_zeros('node', 'topographic__elevation')
np.random.seed(randno)
initial_roughness = np.random.rand(z.size)/100000.
z += initial_roughness
#set southcenter pixel to zero elevation
#outlet=26
#
#z[outlet]=0
#set boundary conditions of model grid (open only (fixed value) on south (bottom) edge)
for edge in (mg.nodes_at_left_edge,mg.nodes_at_right_edge,mg.nodes_at_top_edge):
    mg.status_at_node[edge] = CLOSED_BOUNDARY

##set southwest pixel to FIXED VALUE
#mg.status_at_node[outlet]=FIXED_VALUE_BOUNDARY
#mg.status_at_node[outlet]=FIXED_VALUE_BOUNDARY

#PROCESS SET-UP
#initialize linear diffuser component
lin_diffuse = LinearDiffuser(mg, linear_diffusivity=lin_dif)
#iniitalize erosion by run-off
fr = FlowRouter(mg)
sp = FastscapeEroder(mg,K_sp=K_sp, m_sp=m_sp, n_sp=n_sp)
for i in range(nt):
    fr.run_one_step() 
    sp.run_one_step(dt)
    lin_diffuse.run_one_step(dt)
    z[mg.core_nodes] += uplift_rate * dt  # add the uplift
    if i % 20 == 0:
        print(i*dt)
plt.figure()
imshow_grid(mg, 'topographic__elevation', cmap='jet')
plt.figure()
imshow_grid(mg, mg.status_at_node, cmap='jet')
mg.set_watershed_boundary_condition(z,return_outlet_id=True)
plt.figure()
imshow_grid(mg, 'drainage_area', cmap='jet')
plt.figure()
imshow_grid(mg, mg.status_at_node, cmap='jet')

#imshow_grid(mg, mg.status_at_node, color_for_closed='blue')
