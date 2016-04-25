#!/usr/bin/env python
import os
import illustris_python as il
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import stats
from mayavi import mlab

def plot_subhalo_3d_density_pts(subhalos):
    x = [xyz[0] for xyz in subhalos['SubhaloPos']]
    y = [xyz[1] for xyz in subhalos['SubhaloPos']]
    z = [xyz[2] for xyz in subhalos['SubhaloPos']]
    w = np.log10(subhalos['SubhaloMass'])
    fig = mlab.figure('DensityPlot')
    fig.scene.disable_render = True
    #pts = mlab.points3d(x[::10], y[::10], z[::10], w[::10],scale_factor=300)
    pts = mlab.points3d(x, y, z, w.tolist(), scale_factor=250)
    mask = pts.glyph.mask_points
    mask.maximum_number_of_points = len(x)
    mask.on_ratio = 1
    pts.glyph.mask_input_points = True
    fig.scene.disable_render = False
    mlab.axes()
    mlab.show()

if __name__ == '__main__':
    #add "export ILLUSTRISAPIKEY='insert your api key here'"
    #  to your .bashrc
    apikey = os.environ['ILLUSTRISAPIKEY']

    Isim=3 # simulation 3 is low resolution
    snapNum = 134 # last num in Ill-1, 3rd to last in Ill-3

    basePath='./Illustris-'+str(Isim)+'/'
    fields = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel']
    subhalos = il.groupcat.loadSubhalos(basePath,snapNum,fields=fields)

    #H, edges = np.histogramdd(subhalos['SubhaloPos'], bins=(50,50,50),\
                              #weights=subhalos['SubhaloMass'])
    #print(np.asarray(edges).shape)

    plot_subhalo_3d_density_pts(subhalos)

    #print(subhalos['SubhaloPos'].shape)
    
