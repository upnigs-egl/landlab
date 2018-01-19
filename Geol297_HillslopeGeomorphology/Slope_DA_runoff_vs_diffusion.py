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
from landlab import RasterModelGrid, CLOSED_BOUNDARY, FIXED_VALUE_BOUNDARY
import matplotlib.pyplot as plt#import figure, show, plot, xlabel, ylabel, title,legend,subplots
import numpy as np
import seaborn as sn
import matplotlib as mpl


def bin_slopeDA(slope,DA):
    x=DA[np.isfinite(DA)==True]
    print DA[np.isfinite(DA)==False]
    y=slope[np.isfinite(DA)==True]
    xlogmin=-4#int(np.log10(np.nanmin(x)))
    xlogmax=int(np.log10(np.nanmax(x)))+1
    
    print xlogmin,xlogmax
    xbins=np.logspace(xlogmin,xlogmax,5*(xlogmax-xlogmin))
    digitzd=np.digitize(x,xbins)
    bin_means = [np.nanmean(y[digitzd == i]) for i in range(1, len(xbins))]
    
    return xbins[1:],bin_means

def mg_to_xygrid(mg):
    x = mg.node_vector_to_raster(mg.node_x)
    y = mg.node_vector_to_raster(mg.node_y)
    return x,y




#set plot defaults
mpl.rcParams['ytick.labelsize'] = 'x-small'
mpl.rcParams['xtick.labelsize'] = 'x-small'
mpl.rcParams['axes.labelsize'] = 'small'
mpl.rcParams['axes.titlesize'] = 'large'
mpl.rcParams['legend.fontsize'] = 'x-small'


#1) grid
nrows=100
ncols=100
nodeint=0.02      # in km 

#2) uplift rate
uplift_rate=0.001 
rock_density=2.7
sed_density=2.7



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


elevmin,elevmax=None,None
gradmin,gradmax=None,None
DAmin,DAmax=None,None



"""
------------------------------------------------
FIGURE 1 
------------------------------------------------
"""    

 

#3) linear diffusion
lin_dif=0.0002

#GRID SET-UP
#create model x-y grid    
mg = RasterModelGrid((ncols, nrows), nodeint)
#initialize with zero elevation values and random noise
z = mg.add_zeros('node', 'topographic__elevation')
np.random.seed(randno)
initial_roughness = np.random.rand(z.size)/10000.
z += initial_roughness
#set southcenter pixel to zero elevation
outlet=ncols/2

z[outlet]=0
#set boundary conditions of model grid (open only (fixed value) on south center pixel)
for edge in (mg.nodes_at_left_edge,mg.nodes_at_right_edge,mg.nodes_at_top_edge,mg.nodes_at_bottom_edge):
    mg.status_at_node[edge] = CLOSED_BOUNDARY
#set southcenter pixel to FIXED VALUE
mg.status_at_node[outlet]=1




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
    
#    color_list=np.linspace(1,0.3,nt)
    if i % 20 == 0:
        print(i*dt)
        

mg.set_watershed_boundary_condition(z,remove_disconnected=True)

fig=plt.figure(figsize=(8,6))
fig.suptitle('Kd='+str(lin_dif)+' Ks='+str(K_sp)+' U='+str(uplift_rate)+'\n\n')
ax1=fig.add_subplot(221)
ax2=fig.add_subplot(222,sharex=ax1,sharey=ax1)
ax3=fig.add_subplot(223,sharex=ax1,sharey=ax1)
ax4=fig.add_subplot(224)

ax=[ax1,ax2,ax3]

params=['topographic__elevation','topographic__steepest_slope', 'drainage_area']
pmin=[None,None,None]
pmax=[None,None,None]
cm='jet'
for p in range(len(params)):
    plt.sca(ax[p])
    im = imshow_grid(mg, params[p], grid_units = ['km','km'],cmap=cm,vmin=pmin[p], vmax=pmax[p])


gradient=mg.at_node['topographic__steepest_slope']
DA=mg.at_node['drainage_area']

ax4.loglog(DA,gradient,'r',marker='x',mew=.5,lw=0)

DAbins,slope_means=bin_slopeDA(gradient,DA)

ax4.loglog(DAbins,slope_means,'ko')


    
#
#
#
#
##plt.sca(ax1)
#plt.figure()
#cm="jet"
#im=plt.pcolor(xg,yg,elev.reshape(xg.shape),cmap=cm,vmin=elevmin, vmax=elevmax)
#
#
#im=plt.pcolormesh(xg,yg,elev.reshape(xg.shape),cmap=cm,vmin=elevmin, vmax=elevmax)

#im = imshow_grid(mg, 'topographic__elevation', grid_units = ['km','km'],
#                 var_name='elevation (km)', cmap=cm,vmin=elevmin, vmax=elevmax)
#ax1.set_title('elev')

#plt.sca(ax2)
#cm="jet"
#im = imshow_grid(mg, 'topographic__steepest_slope', grid_units = ['km','km'],
#                 var_name='gradient (m/m)', cmap=cm,vmin=gradmin, vmax=gradmax)
#ax2.set_title('gradient')
#
#plt.sca(ax3)
#cm="jet"
#DA=mg.at_node['drainage_area']
#im=plt.imshow(np.log10(DA).reshape(nrows,ncols),cmap=cm)
##im = imshow_grid(mg, 'drainage_area', grid_units = ['km','km'],
##                 norm=mpl.colors.LogNorm(), var_name='drainage area (km^2)', 
##                 cmap=cm,vmin=DAmin, vmax=DAmax)
#ax3.set_title('drainage area')
#
#plt.sca(ax4)
#cm="jet"
#im = imshow_grid(mg, 'drainage_area', grid_units = ['km','km'],
#                 var_name='drainage area (km^2)', cmap=cm,vmin=DAmin, vmax=DAmax)
#ax4.set_title('drainage area')


#
# DA=mg.at_node['drainage_area']
#    slope=mg.at_node['topographic__steepest_slope']

#fig.tight_layout()



#"""
#------------------------------------------------
#FIGURE 2
#------------------------------------------------
#"""    
#
#
##3) linear diffusion
#lin_dif=0.0001 
#
##GRID SET-UP
##create model x-y grid    
#mg = RasterModelGrid((ncols, nrows), nodeint)
##initialize with zero elevation values and random noise
#z = mg.add_zeros('node', 'topographic__elevation')
#np.random.seed(randno)
#initial_roughness = np.random.rand(z.size)/10000.
#z += initial_roughness
##set south edge to zero elevation
#z[-ncols:]-=initial_roughness[-ncols:]
##set boundary conditions of model grid (open only (fixed value) on south (bottom) edge)
#for edge in (mg.nodes_at_bottom_edge):
#    mg.status_at_node[edge] = FIXED_VALUE_BOUNDARY
#for edge in (mg.nodes_at_left_edge,mg.nodes_at_right_edge,mg.nodes_at_top_edge):
#    mg.status_at_node[edge] = CLOSED_BOUNDARY
#
#
##PROCESS SET-UP
##initialize linear diffuser component
#lin_diffuse = LinearDiffuser(mg, linear_diffusivity=lin_dif)
##iniitalize erosion by run-off
#fr = FlowRouter(mg)
#sp = FastscapeEroder(mg,K_sp=K_sp, m_sp=m_sp, n_sp=n_sp)
#
#
#
#fig=plt.figure(figsize=(8,6))
#fig.suptitle('Kd='+str(lin_dif)+' Ks='+str(K_sp)+' U='+str(uplift_rate)+'\n\n')
#ax1=fig.add_subplot(221)
#ax2=fig.add_subplot(222)
#ax3=fig.add_subplot(223,sharey=ax1)
#ax4=fig.add_subplot(224,sharey=ax1)
#
#
#
#ucolr=sn.color_palette("BrBG", nt//20+1)
#
#j=0
#for i in range(nt):
#    fr.run_one_step() 
#    sp.run_one_step(dt)
#    lin_diffuse.run_one_step(dt)
#    z[mg.core_nodes] += uplift_rate * dt  # add the uplift
#    
##    color_list=np.linspace(1,0.3,nt)
#    if i % 20 == 0:
#        print(i*dt)
#        
#        elev_rast = mg.node_vector_to_raster(z)
#        
#        
##        plot mean elevation vs time
#        curax=ax1
#        curax.plot(i*dt,np.mean(elev_rast),'o',color=ucolr[j],mec='k',mew=0.5)
#        curax.set_xlabel('time',fontsize='small')
##        curax.set_xticklabels(['t'+str(q) for q in range(len(curax.get_xticklabels()))])
#        curax.set_ylabel('mean grid elev, km',fontsize='small')
#        curax.set_title('a')
#        
##        plot section line
#        curax=ax3
#        xcoord_rast = mg.node_vector_to_raster(mg.node_x)
#        nrows = mg.number_of_node_rows
#        im = curax.plot(xcoord_rast[int(nrows // 2),1:-1], elev_rast[int(nrows // 2),1:-1],color=ucolr[j])
#        curax.set_xlabel('distance, km',fontsize='small')
#        curax.set_ylabel('profile elev, km',fontsize='small')
#        curax.set_title('c')
#        
#        curax=ax4
#        ycoord_rast = mg.node_vector_to_raster(mg.node_y)
#        ncols = mg.number_of_node_columns
#        im = curax.plot(ycoord_rast[1:-1,int(ncols // 2)], elev_rast[1:-1,int(ncols // 2)],color=ucolr[j])
#        curax.set_xlabel('distance, km',fontsize='small')
#        curax.set_ylabel('profile elev, km',fontsize='small')
#        curax.set_title('d')
#        curax.set_ylim(-0.005,0.065)
#        
#        j=j+1
#
#
#plt.sca(ax2)
#cm="jet"
#im = imshow_grid(mg, 'topographic__elevation', grid_units = ['km','km'],
#                 var_name='Elevation (km)', cmap=cm,vmin=0, vmax=0.06)
#ax2.axhline(y=1,lw=0.5,color='k',ls=':',label='profile c')
#ax2.axvline(x=1,lw=0.5,color='k',ls='--',label='profile d')
#ax2.set_title('b')
#ax2.legend()
#
#
#fig.tight_layout()
#
#
#
#
#
plt.show()