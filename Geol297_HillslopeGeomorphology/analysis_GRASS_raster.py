#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:59:48 2018

@author: dynaslopeconda
"""

import numpy as np
import matplotlib.pyplot as plt


#FUNCTIONS
def import_grass_raster_ascii(fname,dtype,filling_values=np.nan,skip_header=6,delimiter=' ',missing_values='*' ):
    return np.genfromtxt(fname,dtype,skip_header=skip_header,delimiter=delimiter,missing_values=missing_values,filling_values=filling_values)

def get_input_maps(maptypes,locationfolder):
    map_list=[]
    for m in maptypes:
##        fname=raw_input('Type file name of '+m+' map: ')
        try:
            print locationfolder+'/'+m
            mp=import_grass_raster_ascii(locationfolder+'/'+m,dtype=float,filling_values=np.nan,skip_header=6,delimiter=' ',missing_values='*' )
            print m, mp.shape
            if m=='flowacc':
                mp=np.where(np.isfinite(mp),mp,np.zeros(mp.shape))
                mp=np.where(mp>0,mp,mp*np.nan)#removing pixels where drainage source includes areas outside the map (negative values)
                mp=np.log10(np.abs(mp))
        except:
            mp=np.array([])
            print m,'file does not exist'
        map_list.append(mp)
    return map_list

  
plt.close('all')

#0 DEFAULT VALUES
maptypes=['elev', 'grad', 'asp', 'crosc', 'feature', 'flowacc', 'basins']  #input names of raster files here
mapunits=['m','deg','deg azimuth', 'm^-1','feature type', 'log num pixels','id']
mapcolors=['terrain','inferno','Greys','coolwarm','jet','plasma','gist-rainbow']  #colormaps corresponding to map files (see https://matplotlib.org/examples/color/colormaps_reference.html)
loc_list=['location1','location2']#,'location3'] #input corresponding folder names for each map location

#%%
#1 READING INPUT MAPS
map_list=[]
for l in range(len(loc_list)):
    map_list.append(get_input_maps(maptypes,loc_list[l]))
map_list=np.array(map_list)



#%%
#2 PLOTTING MAPS
which_loc=[0,1]     #### Input location number/s here (separate with comma)
which_map=[4,6]     #### Input map number/s here (separate with comma)
which_area=[50,-1]  #### Input basin/subarea number/s (corresponding to location) here; use -1 to plot all  (separate with comma)
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
            inArea=np.where(map_list[l,6]==which_area[l],map_list[l,m],map_list[l,m]*np.nan)
        try:
            im=mapax[l].imshow(inArea,cmap=plt.get_cmap(mapcolors[m]),vmin=mapmin,vmax=mapmax)
        except:
            im=mapax[l].imshow(inArea,vmin=mapmin,vmax=mapmax)
        mapax[l].axis('equal')
    cbaxes = mapfig.add_axes([0.85, 0.1, 0.03, 0.8]) 
    plt.subplots_adjust(right=0.8)
    plt.colorbar(im,cax=cbaxes)


#%%    
#3 PLOTTING HISTOGRAMS
which_loc=[0,1]         #### Input location number/s here (separate with comma)
which_map=[1,3,5]       #### Input map number/s here (separate with comma)
which_area=[50,-1]      #### Input basin/subarea number/s (corresponding to location) here; use -1 to plot all  (separate with comma)
nhistbins=20
plt.close('all')
for m in which_map:
    histfig,histax=plt.subplots(ncols=1,nrows=len(which_loc),sharex=True)#sharey=True)
    for l in which_loc:
        if which_area[l]==-1:
            inArea=map_list[l,m]
        else:
            inArea=np.where(map_list[l,6]==which_area[l],map_list[l,m],map_list[l,m]*np.nan)
        histax[l].hist(inArea[np.isfinite(inArea)],bins=nhistbins,normed=True,label=loc_list[l]+' '+str(which_area[l]))
#        histax[l].set_title(loc_list[l]+' '+str(which_area[l]))
        histax[l].legend()
    histax[l].set_xlabel(maptypes[m]+', '+mapunits[m])
 



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
        print mapcolors[which_mapZ[m]]
        sc=scatax[l].scatter(inAreaX[np.isfinite(inAreaZ)],inAreaY[np.isfinite(inAreaZ)],c=inAreaZ[np.isfinite(inAreaZ)],cmap=plt.get_cmap(mapcolors[which_mapZ[m]]),vmin=mapmin,vmax=mapmax,marker='+',alpha=0.1)#,c=inAreaZ,cmap=plt.get_cmap(mapcolors[which_mapZ[m]]))

    cbaxes = scatfig.add_axes([0.85, 0.1, 0.03, 0.8]) 
    plt.subplots_adjust(right=0.8)
    plt.colorbar(sc,cax=cbaxes)    
#%%     
    
    
    
  
    



    


##4 PLOTTING SCATTERPLOTS OF 2 MAPS AND AT LEAST TWO AREAS
#which_mapX=5     #### Input map number here to plot in X axis(one value only)
#which_mapY=1     #### Input map number here to plot in Y axis(one value only)
#which_mapZ=4     #### Input map number here to plot as Z value (one value only)
#which_area=[50,208]   #### Input basin numbers here (at least two values)
#
#fig,ax=plt.subplots(nrows=len(which_area),ncols=1,sharex=True,sharey=True)
#for w in range(len(which_area)):
#    both_Finite=np.isfinite(map_list[which_mapX])*np.isfinite(map_list[which_mapY])
#    mapX_inArea=np.where(map_list[-1]==which_area[w],map_list[which_mapX],map_list[which_mapX]*np.nan)
#    mapY_inArea=np.where(map_list[-1]==which_area[w],map_list[which_mapY],map_list[which_mapY]*np.nan)
##    ax[w].plot(mapX_inArea[both_Finite],mapY_inArea[both_Finite],'+',mew=0.1,alpha=0.5) 
#    ax[w].scatter(mapX_inArea[both_Finite],mapY_inArea[both_Finite],c=map_list[which_mapZ][both_Finite],cmap=plt.get_cmap(mapcolors[which_mapZ]),marker='+',alpha=0.5)
#    

plt.show()







##while True:
####    for m in range(len(map_list))
####        print m map_list[m] 
##    which_map=int(raw_input('which map?'))
##    which_mapX=int(raw_input('which mapX?'))
##    which_mapY=int(raw_input('which mapY?'))
##    which_area=[50,208]
##    #generate_map(map_list,[1,3,5],mapdatatransform,mapcolors)
##    generate_histogram(which_map,which_area,map_list,nhistbins=20)
##    #generate_scatterplot(which_mapX,which_mapY,which_area,map_list)
##    plt.show()

##
##
###defining input files
##area_subset='basins'
##area_subset_dtype=int
##
##param1='crosc'
##param1_dtype=float
##
##param2='grad'
##param2_dtype=float
##
###defining analysis subarea
##sub_a=[50,208]
##
##
###importing input files to arrays 
##a=import_grass_raster_ascii(area_subset,area_subset_dtype,filling_values=-1)
##
##p1=import_grass_raster_ascii(param1,param1_dtype)
##p1max=np.nanmax(p1)
##p1min=np.nanmin(p1)
##
##p2=import_grass_raster_ascii(param2,param2_dtype)
##p2max=np.nanmax(p2)
##p2min=np.nanmin(p2)
##
##print a.shape
##print p1.shape
##print p2.shape
##
###plotting maps,whole area
##plot_list=[p1, p2]
###plot_list=[np.tan(np.radians(p1)),np.log10(np.abs(p2))]
###fig,ax=plot_maps(plot_list)
###analyze_plots(plot_list)
###plt.show()
##
##
###
###
##for s in sub_a:
##    #defining mask for subarea
##    cur_sub_a=np.where(a==s,1,np.nan)
##    subplot_list=[]
##    subplot_pts_list=[]
##    for p in range(len(plot_list)):
##        #masking map
##        cur_sub_map=plot_list[p]*cur_sub_a
##        cur_sub_pts=cur_sub_map#[np.isfinite(cur_sub_map)]
##        subplot_list.append(cur_sub_map)
##        subplot_pts_list.append(cur_sub_pts)
##    #plotting maps
##    fig,ax=plot_maps(subplot_list)
##    analyze_plots(subplot_pts_list)
###    
###        
##    
##        
#plt.show()
    




