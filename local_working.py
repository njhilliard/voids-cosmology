#!/usr/bin/env python
import os
import illustris_python as il
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plot_subhalo_pts(subhalos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [xyz[0] for xyz in subhalos['SubhaloPos']]
    ys = [xyz[1] for xyz in subhalos['SubhaloPos']]
    zs = [xyz[2] for xyz in subhalos['SubhaloPos']]
    ax.scatter(xs, ys, zs)
    plt.show()

if __name__ == '__main__':
    #add "export ILLUSTRISAPIKEY='insert your api key here'"
    #  to your .bashrc
    apikey = os.environ['ILLUSTRISAPIKEY']

    Isim=3 # simulation 3 is low resolution
    snapNum = 134 # last num in Ill-1, 3rd to last in Ill-3

    basePath='./Illustris-'+str(Isim)+'/'
    fields = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel']
    subhalos = il.groupcat.loadSubhalos(basePath,snapNum,fields=fields)

    H, edges = np.histogramdd(subhalos['SubhaloPos'], bins=(50,50,50),\
                              weights=subhalos['SubhaloMass'])

    plot_subhalo_pts(subhalos)

    #print(subhalos['SubhaloPos'].shape)
    
