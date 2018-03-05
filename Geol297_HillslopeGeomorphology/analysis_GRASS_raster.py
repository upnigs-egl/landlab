#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:59:48 2018

@author: dynaslopeconda
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import cmocean

#%%
#FUNCTIONS
def import_grass_raster_ascii(fname,dtype,filling_values=np.nan,skip_header=6,delimiter=' ',missing_values='*' ):
    return np.genfromtxt(fname,dtype,skip_header=skip_header,delimiter=delimiter,missing_values=missing_values,filling_values=filling_values)

def get_input_maps(maptypes,locationfolder):
    map_list=[]
    for m in maptypes:
        try:
            mp=import_grass_raster_ascii(locationfolder+'/'+m,dtype=float,filling_values=np.nan,skip_header=6,delimiter=' ',missing_values='*' )
            if m=='flowacc':
#                mp=np.where(np.isfinite(mp),mp,np.zeros(mp.shape))
#                mp=np.where(mp>0,mp,mp*np.nan)#removing pixels where drainage source includes areas outside the map (negative values)
#                mp=np.log10(np.abs(mp))
                mp=np.log10(np.where(np.isfinite(mp),np.where(mp>0,mp,mp*np.nan),mp)) #removing pixels where drainage source includes areas outside the map (negative values)
            if m=='asp':
                mp=np.where(np.isfinite(mp),np.where(mp>0,mp,360+mp),mp)
            print locationfolder+'/'+m, mp.shape
        except:
            mp=np.array([])
            print '\n',locationfolder+'/'+m, mp.shape, 'file does not exist'
        map_list.append(mp)
    return map_list

def discrete_feature_color():
    # make a color map of fixed colors
    cmap = colors.ListedColormap(['0.5','black','blue','green','yellow', 'red'])
    bounds=[1,2,3,4,5,6,7]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    return cmap,norm

  

#%%
# 0 DEFAULT VALUES
maptypes=['elev', 'grad', 'asp', 'crosc', 'feature', 'flowacc', 'basins']           #input names of raster files here
mapunits=['m','deg','deg azimuth', 'm^-1','type', 'log num pixels','id']
mapcolors=['terrain','inferno','Greys','coolwarm','jet','plasma','gist_rainbow']    #colormaps corresponding to map files (see https://matplotlib.org/examples/color/colormaps_reference.html)
loc_list=['location1','location2']#,'location3']                                       #input corresponding folder names for each map location
loc_name_list=['study area A','study area B']#,'study area C']                        #input corresponding names of locations
#%%
# 1 READING INPUT MAPS
map_list=[]
for l in range(len(loc_list)):
    map_list.append(get_input_maps(maptypes,loc_list[l]))
map_list=np.array(map_list)
plt.close('all')

#%%
# 2 PLOTTING MAPS
which_loc=[0,1]     #### Input location number/s here (separate with comma)
which_map=[0,2]     #### Input map number/s here (separate with comma)
which_area=[-1,-1]  #### Input basin/subarea number/s (corresponding to location) here; use -1 to plot all  (separate with comma)
loc_name_list=['A','B']#,'C'] 
plt.close('all')
for m in which_map:
    mapmax=np.max([np.nanmax(map_list[l,m]) for l in which_loc])
    mapmin=np.min([np.nanmin(map_list[l,m]) for l in which_loc])
#    print "Range is from "+str(mapmin)+" to "+str(mapmax)
#    mmin=float(raw_input("Input minimum value for plot "))
#    mmax=float(raw_input("Input maximum value for plot "))
    if m==3:
        ext=0.6*np.max([abs(mapmin),abs(mapmax)])
        mapmin=ext*-1
        mapmax=ext
    mapfig,mapax=plt.subplots(ncols=1,nrows=len(which_loc))#,sharex=True,sharey=True)
    for l in which_loc:
        if which_area[l]==-1:
            inArea=map_list[l,m]
        else:
            try:
                inArea=np.where(map_list[l,6]==which_area[l],map_list[l,m],map_list[l,m]*np.nan)
            except:
                print 'Basin/subarea ',which_area[l],' not found.'
                inArea=map_list[l,m]
        if m==4:
            cmap,norm=discrete_feature_color(),None
        elif m==2:
            cmap,norm=cmocean.cm.phase,None
        else:cmap,norm=plt.get_cmap(mapcolors[m]),None
        try:
            im=mapax[l].imshow(inArea,cmap=cmap,norm=norm,vmin=mapmin,vmax=mapmax)
        except:
            im=mapax[l].imshow(inArea,vmin=mapmin,vmax=mapmax)
        mapax[l].axis('equal')
        mapax[l].set_title(loc_name_list[l]+' '+str(which_area[l]))
    cbaxes = mapfig.add_axes([0.85, 0.1, 0.03, 0.8]) 
    cb=plt.colorbar(im,cax=cbaxes)
    if m==4:
        labels = ['plane','pit','channel','pass','ridge','peak']
        loc    = np.arange(1,8,1) - .5
        cb.set_ticks(loc)
        cb.set_ticklabels(labels)
    mapfig.tight_layout()
    plt.subplots_adjust(right=0.8,top=0.85)
    plt.suptitle(maptypes[m]+', '+mapunits[m])
    


#%%    
# 3 PLOTTING HISTOGRAMS
which_loc=[0,1]         #### Input location number/s here (separate with comma)
which_map=[1,3]       #### Input map number/s here (separate with comma)
which_area=[78,50]      #### Input basin/subarea number/s (corresponding to location) here; use -1 to plot all  (separate with comma)
nhistbins=20

plt.close('all')
for m in which_map:
    histfig,histax=plt.subplots(ncols=1,nrows=len(which_loc),sharex=True)#sharey=True)
    for l in which_loc:
        if which_area[l]==-1:
            inArea=map_list[l,m]
        else:
            inArea=np.where(map_list[l,6]==which_area[l],map_list[l,m],map_list[l,m]*np.nan)
        histax[l].hist(inArea[np.isfinite(inArea)],bins=nhistbins,normed=True,label=loc_name_list[l]+' '+str(which_area[l]))
        histax[l].set_title(loc_name_list[l]+' '+str(which_area[l]))
        histax[l].set_ylabel('normed frequency')
    histax[l].set_xlabel(maptypes[m]+', '+mapunits[m])
    histfig.tight_layout()
    



#%%    
#4 PLOTTING SCATTER PLOTS
which_loc=[0,1]         #### Input location number/s here (separate with comma)
which_mapX=[1,5]       #### Input map number/s here (separate with comma)
which_mapY=[3,1]       #### Input map number/s here (separate with comma)
which_mapZ=[4,3]       #### Input map number/s here (separate with comma)
which_area=[78,50]      #### Input basin/subarea number/s (corresponding to location) here; use -1 to plot all  (separate with comma)

    

plt.close('all')
for m in range(len(which_mapX)):
    mapmax=np.max([np.nanmax(map_list[l,which_mapZ[m]]) for l in which_loc])
    mapmin=np.min([np.nanmin(map_list[l,which_mapZ[m]]) for l in which_loc])
    if which_mapZ[m]==3:
        ext=0.5*np.max([abs(mapmin),abs(mapmax)])
        mapmin=ext*-1
        mapmax=ext
    isFinite=np.isfinite(map_list[l,which_mapX[m]])*np.isfinite(map_list[l,which_mapY[m]])*np.isfinite(map_list[l,which_mapZ[m]])
    scatfig,scatax=plt.subplots(ncols=1,nrows=len(which_loc),sharex=True,sharey=True)
    for l in which_loc:
        inAreaX=map_list[l,which_mapX[m]][isFinite]
        inAreaY=map_list[l,which_mapY[m]][isFinite]
        inAreaZ=map_list[l,which_mapZ[m]][isFinite]
        if which_area[l]!=-1:
            inAreaX=np.where(map_list[l,6][isFinite]==which_area[l],inAreaX,inAreaX*np.nan)
            inAreaY=np.where(map_list[l,6][isFinite]==which_area[l],inAreaY,inAreaY*np.nan)
            inAreaZ=np.where(map_list[l,6][isFinite]==which_area[l],inAreaZ,inAreaZ*np.nan)
            print inAreaZ[np.isfinite(inAreaZ)].shape
        else:
            print inAreaZ.shape
        if which_mapZ[m]==4:cmap,norm=discrete_feature_color()
        else:cmap,norm=plt.get_cmap(mapcolors[which_mapZ[m]]),None
        sc=scatax[l].scatter(inAreaX[np.isfinite(inAreaZ)],
                 inAreaY[np.isfinite(inAreaZ)],
                 c=inAreaZ[np.isfinite(inAreaZ)],
                 cmap=cmap,norm=norm, 
                 vmin=mapmin,vmax=mapmax,
                 marker='.',s=2)
        scatax[l].set_ylabel(maptypes[which_mapY[m]]+', '+mapunits[which_mapY[m]])
    scatax[l].set_xlabel(maptypes[which_mapX[m]]+', '+mapunits[which_mapX[m]])
    cbaxes = scatfig.add_axes([0.85, 0.1, 0.03, 0.8]) 
    cb=plt.colorbar(sc,cax=cbaxes)
    if which_mapZ[m]==4:
        labels = ['plane','pit','channel','pass','ridge','peak']
        loc    = np.arange(1,8,1) - .5
        cb.set_ticks(loc)
        cb.set_ticklabels(labels)
    scatfig.tight_layout()
    plt.subplots_adjust(right=0.8)    
#%%

plt.show()     
 


