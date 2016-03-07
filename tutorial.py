import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from StringIO import StringIO
import h5py
import astropy.table as atpy
import requests
import os


def get(path, params=None):

    #code for customized requests from: http://www.mobify.com/blog/http-requests-are-hard/

    # Use a `Session` instance to customize how `requests` handles making HTTP requests.
    session = requests.Session()

    # `mount` a custom adapter that retries failed connections for HTTP and HTTPS requests.
    session.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
    session.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))
 
    # make HTTP GET request to path
    headers = {"api-key":str(apikey)}
    r = session.get(path, params=params, headers=headers)

    # raise exception if response code is not HTTP SUCCESS (200)
    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json() # parse json responses automatically

    if 'content-disposition' in r.headers:
        filename = r.headers['content-disposition'].split("filename=")[1]
        with open(filename, 'wb') as f:
            f.write(r.content)
        return filename # return the filename string

    return r


if __name__ == '__main__':

    '''
    Illustris web API details and example scripts:
    http://www.illustris-project.org/data/docs/api/
    '''
    
    #api key, available after registering on http://www.illustris-project.org/data/
    apikey=''

    #simulation
    Isim=3
    #NB: useful to test code on lower resolution run like I3

    #snapshot number, snapNum=135 -> z=0 
    snapNum = 135

    #cosmology
    H0=70.
    h=H0/100.


    #ID of FOF group we'll use for the examples
    groupID=100



    '''
    Ex: Halo Catalogues
    '''

    ##determine how many subhalos in simulation (also, accessing the subhalo catalogue)
    url='http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/subhalos/'
    #print url
    subhalocat=get(url)
    #print subhalocat
    #print subhalocat.keys()
    #print subhalocat['count']

    ##get info on a specific group
    url='http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/halos/'+str(groupID)+'/info.json'
    group_prop=get(url)
    #print group_prop
    #print group_prop.keys()
    #print group_prop['Group'].keys()
    
    ##group's bcg ID
    bcg_subfindID=group_prop['Group']['GroupFirstSub']
    #print bcg_subfindID

    ##all subfind subhalos of group
    Nsubs=group_prop['Group']['GroupNsubs']
    subhalobound_IDlist=np.arange(bcg_subfindID,bcg_subfindID+Nsubs)
    #print Nsubs
    #print subhalobound_IDlist
    
    ##make some plots with the group's subhalo members
    Msub_arr=[]
    rmag_arr=[]
    for subhaloID in subhalobound_IDlist:
        url='http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/subhalos/'+str(subhaloID)+'/info.json'
        subhalo_prop=get(url)
        #print url
        #print subhalo_prop.keys()
        #exit()
        subhalo_prop=subhalo_prop['Subhalo']
        subhalo_Mtot=subhalo_prop['SubhaloMass']*(10.**10.)*(h**-1.)
        Msub_arr.append(subhalo_Mtot)
        subhalo_rmag=subhalo_prop['SubhaloStellarPhotometrics'][5]
        rmag_arr.append(subhalo_rmag)

    ##histogram of subhalo masses
    #plt.hist(Msub_arr,5)
    #plt.xlabel('M$_{\mathrm{tot,bound}}$ [M$_{\odot}$]')
    #plt.ylabel('N')
    #plt.show()
    
    ##histogram of subhalo r-mags
    ##NB: not all subhalos have photometry!
    #print rmag_arr
    ind=np.where(np.array(rmag_arr)<1e+36)[0] #identify subhalos with photometry
    rmag_arr=np.array(rmag_arr)[ind] #only use subhalos with photometry
    #plt.hist(rmag_arr,6)
    #plt.xlabel('r-mag')
    #plt.ylabel('N')
    #plt.show()
    


    '''
    Ex: Merger trees
    '''
    ##MPB merger tree for bcg -- NB: MPB specified in url
    url='http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/subhalos/'+str(bcg_subfindID)+'/sublink/mpb.hdf5'
    mpb_filename=get(url)
    
    ##put tree data into another (my favorite) data structure: astropy tables
    tree=atpy.Table()
    with h5py.File(mpb_filename) as ft:
        for key in ft.keys():
            tree.add_column(atpy.Column(name=str(key),data=np.array(ft[str(key)])))
    #print tree.columns

    ##remove tree file - hdf5 files remain in working directory otherwise
    if os.path.isfile('./sublink_mpb_'+str(bcg_subfindID)+'.hdf5')==True:
        os.remove('./sublink_mpb_'+str(bcg_subfindID)+'.hdf5')

    ##z=0 index in tree   
    ind_z0=np.where(tree['SnapNum']==135)[0][0] 

    finalmass_bcg=np.sum(tree['SubhaloMassInRadType'][ind_z0])
    fracmass_bcg=np.array([np.sum(x) for x in tree['SubhaloMassInRadType']])/finalmass_bcg
    
    finalmass_group=tree['Group_M_Crit200'][ind_z0]
    fracmass_group=tree['Group_M_Crit200']/finalmass_group

    ##plot the mass assembly of bcg, parent group
    
    ##mass assembly for bcg
    #plt.plot(tree['SnapNum'],fracmass_bcg)
    #plt.xlabel('Snapshot number')
    #plt.ylabel('Fraction of z=0 subhalo mass assembled')

    ##mass assembly for parent group of bcg
    #plt.plot(tree['SnapNum'],fracmass_group)
    #plt.xlabel('Snapshot number')
    #plt.ylabel('Fraction of z=0 group M200 assembled')

    #plt.show()
 


    '''
    Ex: Snapshots
    '''
    ##pull a cutout of snapshot data for bcg
    snap_params={'stars':'Coordinates,GFM_StellarPhotometrics'}
    url = 'http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/subhalos/'+str(bcg_subfindID)+'/cutout.hdf5'
    part_filename=get(url,snap_params) #get and save hdf5 file 

    part = atpy.Table()
    with h5py.File(part_filename) as f:
        for key in f['PartType4'].keys():
            part.add_column(atpy.Column(name=str(key),data=np.array(f['PartType4'][str(key)])))   
    #print part.columns

    ##remove snapshot before proceeding
    if os.path.isfile('./cutout_'+str(bcg_subfindID)+'.hdf5')==True:
        os.remove('./cutout_'+str(bcg_subfindID)+'.hdf5')



        
    '''
    Ex: Synthetic image of a galaxy 
    '''
    Isim=1 #mocks only exist for I1!
    subhaloID=10
    url='http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/subhalos/'+str(subhaloID)+'/stellar_mocks/image.png'

    response=get(url)
    file_object=StringIO(response.content)
    #plt.imshow(mpimg.imread(file_object))
    #plt.show()




