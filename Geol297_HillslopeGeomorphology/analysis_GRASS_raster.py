#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:59:48 2018

@author: dynaslopeconda
"""

import numpy as np
import matplotlib.pyplot as plt


#DEFAULT VALUES
transformtypes=['get absolute values', 'log trasform', 'convert to degrees to tangent_theta']
mapdatatransform=[[1,0,0], #elev
                  [1,1,1], #grad
                  [0,0,0], #aspect
                  [0,0,0], #crosc
                  [0,0,0], #features
                  [1,1,0], #flowacc
                  [0,0,0]] #basins

#FUNCTIONS
def import_grass_raster_ascii(fname,dtype,filling_values=np.nan,skip_header=6,delimiter=' ',missing_values='*' ):
    return np.genfromtxt(fname,dtype,skip_header=skip_header,delimiter=delimiter,missing_values=missing_values,filling_values=filling_values)

def get_input_maps(maptypes):
    map_list=[]
    for m in maptypes:
##        fname=raw_input('Type file name of '+m+' map: ')
        try:
            mp=import_grass_raster_ascii(m,dtype=float,filling_values=np.nan,skip_header=6,delimiter=' ',missing_values='*' )
            print m, mp.shape
            if m=='flowacc':
                mp=np.where(np.isfinite(mp),mp,np.zeros(mp.shape))
                print mp,mp.shape#converting NaNs, infs to zero
                mp=np.where(mp>0,mp,mp*np.nan)#removing pixels where drainage source includes areas outside the map (negative values)
                print mp,mp.shape
                mp=np.log10(np.abs(mp))
                print mp.shape
        except:
            mp=np.array([])
            print m,'file does not exist'
        map_list.append(mp)
    return map_list

##def do_data_transform(mp,which_transform):
##    newmap=mp
##    if which_transform[0]==1:newmap=np.abs(newmap)
##    if which_transform[2]==1:newmap=np.tan(np.radians(np.abs(newmap)))
##    if which_transform[1]==1:newmap=np.log10(np.abs(newmap))
##    return newmap
##
##def prompt_change_transform(mdt=mapdatatransform,mt=maptypes,tt=transformtypes):
##    change=raw_input('Change default data transform? <y>, <n>? ')
##    if change in ['y','Y']:
##        for m in range(len(mt)):
##            mdt[m]=raw_input('Input transform for '+mt[m]+' e.g.,'+str(mdt[m])+'('+tt[m]+' : ')
##        return mdt
##    else:
##        return mdt
##        
##            
##
##def generate_map(which_map,map_list,mapdatatransform,mapcolors):
##    dat=do_data_transform(map_list[which_map],mapdatatransform[which_map])
##    im=ax[w].imshow(dat,cmap=plt.get_cmap(mapcolors[which_map[w]]))
##    plt.axis=('scaled')
##    plt.colorbar(im,ax=plt.gca())
##    return 
##
##    fig,ax=plt.subplots(ncols=1,nrows=len(which_map),sharex=True,sharey=True)
##    for w in range(len(which_map)):
##        dat=do_data_transform(map_list[which_map[w]],mapdatatransform[which_map[w]])
##        im=ax[w].imshow(dat,cmap=plt.get_cmap(mapcolors[which_map[w]]))
##        ax[w].axis=('scaled')
##        plt.colorbar(im,ax=ax[w])
##
##        
##    return fig,ax
##
##    
##
##def generate_histogram(which_map,which_area,map_list,nhistbins=20):
##    fig,ax=plt.subplots(nrows=len(which_area),ncols=1,sharex=True)
##    for w in range(len(which_area)):
##        map_inArea=np.where(map_list[-1]==which_area[w],map_list[which_map],map_list[which_map]*np.nan)
##        dat=do_data_transform(map_inArea[np.isfinite(map_inArea)],mapdatatransform[which_map])
##        ax[w].hist(dat,bins=nhistbins)
##        
##def generate_scatterplot(which_mapX,which_mapY,which_area,map_list):
##    fig,ax=plt.subplots(nrows=len(which_area),ncols=1,sharex=True,sharey=True)
##    for w in range(len(which_area)):
##
##        
##        both_Finite=np.isfinite(map_list[which_mapX])*np.isfinite(map_list[which_mapY])
##
##        mapX_inArea=np.where(map_list[-1]==which_area[w],map_list[which_mapX],map_list[which_mapX]*np.nan)
##        mapY_inArea=np.where(map_list[-1]==which_area[w],map_list[which_mapY],map_list[which_mapY]*np.nan)
##
##        datX=do_data_transform(mapX_inArea[both_Finite],mapdatatransform[which_mapX])
##        datY=do_data_transform(mapY_inArea[both_Finite],mapdatatransform[which_mapY])
##        
##        ax[w].plot(datX,datY,'+',mew=0.1,alpha=0.5)        
##        
##
##def plot_maps(plot_list):
##    fig,ax=plt.subplots(nrows=1,ncols=len(plot_list),sharex=True,sharey=True)
##    for p in range(len(plot_list)):
##        ax[p].imshow(plot_list[p])
##        ax[p].axis=('scaled')
##    return fig,ax
##
##def analyze_plots(plot_list,nhistbins=20):
##    fig=plt.figure()
##    ax1=fig.add_subplot(221)
##    ax1.hist(plot_list[0][np.isfinite(plot_list[0])],bins=nhistbins)
##    ax2=fig.add_subplot(222)
##    ax2.hist(plot_list[1][np.isfinite(plot_list[1])],bins=nhistbins)
##    ax3=fig.add_subplot(212)
##    ax3.plot(plot_list[1],plot_list[0],'+',mew=0.1)
##
##    
plt.close('all')

#0 DEFAULT VALUES
maptypes=['elev', 'grad', 'asp', 'crosc', 'feature', 'flowacc', 'basins']  #input names of raster files here
mapcolors=['terrain','inferno','Greys','coolwarm','jet','plasma','tab10']


#1 READING INPUT MAPS
map_list=get_input_maps(maptypes)


##2 PLOTTING MAPS
#which_map=3  #### Input map number here (one value only)
#print "Range is from "+str(np.nanmin(map_list[which_map]))+" to "+str(np.nanmax(map_list[which_map]))
#mmin=float(raw_input("Input minimum value for plot "))
#mmax=float(raw_input("Input maximum value for plot "))
#try:
#    im=plt.imshow(map_list[which_map],cmap=plt.get_cmap(mapcolors[which_map]),vmin=mmin,vmax=mmax)
#except:
#    im=plt.imshow(map_list[which_map],vmin=mmin,vmax=mmax)
#plt.colorbar(im,ax=plt.gca())
#
#
##3 PLOTTING HISTOGRAMS OF AT LEAST TWO AREAS
#which_map=1     #### Input map number here (one value only)
#which_area=[50,208]   #### Input basin numbers here (at least two values)
#nhistbins=20
#fig,ax=plt.subplots(nrows=len(which_area),ncols=1,sharex=True)
#for w in range(len(which_area)):
#    map_inArea=np.where(map_list[-1]==which_area[w],map_list[which_map],map_list[which_map]*np.nan)
#    ax[w].hist(map_inArea[np.isfinite(map_inArea)],bins=nhistbins)


#4 PLOTTING SCATTERPLOTS OF 2 MAPS AND AT LEAST TWO AREAS
which_mapX=5     #### Input map number here to plot in X axis(one value only)
which_mapY=1     #### Input map number here to plot in Y axis(one value only)
which_mapZ=4     #### Input map number here to plot as Z value (one value only)
which_area=[50,208]   #### Input basin numbers here (at least two values)

fig,ax=plt.subplots(nrows=len(which_area),ncols=1,sharex=True,sharey=True)
for w in range(len(which_area)):
    both_Finite=np.isfinite(map_list[which_mapX])*np.isfinite(map_list[which_mapY])
    mapX_inArea=np.where(map_list[-1]==which_area[w],map_list[which_mapX],map_list[which_mapX]*np.nan)
    mapY_inArea=np.where(map_list[-1]==which_area[w],map_list[which_mapY],map_list[which_mapY]*np.nan)
#    ax[w].plot(mapX_inArea[both_Finite],mapY_inArea[both_Finite],'+',mew=0.1,alpha=0.5) 
    ax[w].scatter(mapX_inArea[both_Finite],mapY_inArea[both_Finite],c=map_list[which_mapZ][both_Finite],cmap=plt.get_cmap(mapcolors[which_mapZ]),marker='+',alpha=0.5)
    

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
    




