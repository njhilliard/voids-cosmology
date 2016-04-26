#!/usr/bin/env python
import os
import illustris_python as il
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import stats
from mayavi import mlab

def plot_subhalo_3d_density_pts(subhalos, voids, v_size):
    x = [xyz[0] for xyz in subhalos['SubhaloPos']]
    y = [xyz[1] for xyz in subhalos['SubhaloPos']]
    z = [xyz[2] for xyz in subhalos['SubhaloPos']]
    w = np.log10(subhalos['SubhaloMass'])
    fig = mlab.figure('DensityPlot')
    fig.scene.disable_render = True
    pts2 = mlab.points3d(voids[0], voids[1], voids[2],scale_factor=v_size)
    pts = mlab.points3d(x[::30], y[::30], z[::30], w.tolist()[::30],
scale_factor=200)
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

    Isim=1 # simulation 3 is low resolution
    snapNum = 135 

    basePath='./Illustris-'+str(Isim)+'/'
    fields = ['SubhaloMass', 'SubhaloPos']
    subhalos = il.groupcat.loadSubhalos(basePath,snapNum,fields=fields)

    H, edges = np.histogramdd(subhalos['SubhaloPos'], bins=(6,6,6),\
                              weights=subhalos['SubhaloMass'])
    cube_length = edges[0][1]-edges[0][0]
    mass_cutoff = .01 * H.max()
    void_cubes = (np.asarray(np.where(H < mass_cutoff)) + 0.5)\
                 * cube_length
    plot_subhalo_3d_density_pts(subhalos, void_cubes, cube_length)

    #print(subhalos['SubhaloPos'].shape)
    
