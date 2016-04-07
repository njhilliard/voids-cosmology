#!/usr/bin/env python
import os
import illustris_python as il

if __name__ == '__main__':
    #add "export ILLUSTRISAPIKEY='insert your api key here'"
    #  to your .bashrc
    apikey = os.environ['ILLUSTRISAPIKEY']

    Isim=3 # simulation 3 is low resolution
    snapNum = 134 # last num in Ill-1, 3rd to last in Ill-3

    basePath='./Illustris-'+str(Isim)+'/'
    fields = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel']
    subhalos = il.groupcat.loadSubhalos(basePath,snapNum,fields=fields)

    print(subhalos['count'])
