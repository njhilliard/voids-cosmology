#!/usr/bin/env python
import os
import illustris_python as il
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.optimize as so
from scipy import stats
from mayavi import mlab

def plot_subhalo_3d_density_pts(subhalos, voids, v_size):
    x = [xyz[0] for xyz in subhalos['SubhaloPos']]
    y = [xyz[1] for xyz in subhalos['SubhaloPos']]
    z = [xyz[2] for xyz in subhalos['SubhaloPos']]
    w = np.log10(subhalos['SubhaloMass'])
    fig = mlab.figure('DensityPlot')
    fig.scene.disable_render = True
    pts2 = mlab.points3d(voids[0], voids[1], voids[2], opacity=0.5,\
                         scale_factor=v_size)
    pts = mlab.points3d(x[::30], y[::30], z[::30], w.tolist()[::30],\
                        scale_factor=200)
    mask = pts.glyph.mask_points
    mask.maximum_number_of_points = len(x)
    mask.on_ratio = 1
    pts.glyph.mask_input_points = True
    fig.scene.disable_render = False
    mlab.axes()
    mlab.show()

def dist2point(point, points):
    point = point.flatten()
    points = np.asarray(points)
    dir_vecs = points - point
    dists = np.sqrt(np.sum((dir_vecs)**2, axis=1))
    return dists, dir_vecs
    

if __name__ == '__main__':
    #add "export ILLUSTRISAPIKEY='insert your api key here'"
    #  to your .bashrc
    apikey = os.environ['ILLUSTRISAPIKEY']

    Isim=1 # simulation 3 is low resolution
    snapNum = 135 

    basePath='./Illustris-'+str(Isim)+'/'
    fields = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel']
    subhalos = il.groupcat.loadSubhalos(basePath,snapNum,fields=fields)

    H, edges = np.histogramdd(subhalos['SubhaloPos'], bins=(6,6,6),\
                              weights=subhalos['SubhaloMass'])
    cube_length = edges[0][1]-edges[0][0]
    mass_cutoff = .01 * H.max()
    void_cntr = (np.asarray(np.where(H < mass_cutoff)) + 0.5)\
                * cube_length
    #void_cntr = (np.asarray(np.where(H == H.max())) + 0.5)\
                #* cube_length
    centers = [(edges[i][:6] + (0.5 * cube_length)).tolist()\
                for i in range(3)]
    for i in centers[0]:
        for j in centers[1]:
            for k in centers[2]:
                centers.append([i,j,k])
    centers = centers[3:]
    
    hubbles = []
    easy = 216
    for center in centers[:easy]:
        ctr_sbhal = np.argmin(dist2point(np.asarray([center]),\
                                         subhalos['SubhaloPos'])[0])
        dists, dir_vecs = dist2point(subhalos['SubhaloPos'][ctr_sbhal],\
                                     subhalos['SubhaloPos'])
        vel_diffs = subhalos['SubhaloVel']\
                    - subhalos['SubhaloVel'][ctr_sbhal].flatten()
        with np.errstate(invalid='ignore'):
            vels = np.einsum('ij,ij->i', dir_vecs, vel_diffs) / dists
        vels = np.nan_to_num(vels)
        dists = dists * 106.5/75000
        invoid_idx = np.where(dists < 20)
        vels = vels[invoid_idx]
        dists = dists[invoid_idx]
        hubbles.append(so.curve_fit(lambda x, m: m*x, dists, vels)[0][0])
    plt.plot(np.asarray(H).flatten()[:easy], hubbles, 'ro')
    plt.show()
        
    
    #ctr_sbhal = np.argmin(\
                     #dist2point(void_cntr, subhalos['SubhaloPos'])[0])
    #dists,dir_vecs = dist2point(subhalos['SubhaloPos'][ctr_sbhal],\
                                #subhalos['SubhaloPos'])
    #vel_diffs = subhalos['SubhaloVel']\
                #- subhalos['SubhaloVel'][ctr_sbhal].flatten()
    #with np.errstate(invalid='ignore'):
        #vels = np.einsum('ij,ij->i', dir_vecs, vel_diffs) / dists
    #vels = np.nan_to_num(vels)
    #dists = dists * 106.5/75000
    #invoid_idx = np.where(dists < 20)
    #vels = vels[invoid_idx]
    #dists = dists[invoid_idx]
    #print(so.curve_fit(lambda x, m: m*x, dists, vels)[0][0])
    #print(stats.linregress(np.sqrt(np.sum((dir_vecs)**2,axis=1)), vels))
    #plt.plot(dists, vels, 'ro')
    #plt.xlim((0, 14000))
    #plt.show()
    #print(subhalos['SubhaloPos'][ctr_sbhal])
    #print(void_cntr)

    #plot_subhalo_3d_density_pts(subhalos, void_cntr, cube_length)

    #print(subhalos['SubhaloPos'].shape)
    
