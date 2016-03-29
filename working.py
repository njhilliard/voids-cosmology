#!/usr/bin/python

import requests

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

    # Nate's api key. Should work for you
    apikey = 'ada2ceae1a5d78e2f2bc6edb6c5183dd'

    Isim=3 # simulation 3 is low resolution
    snapNum = 134 # last num in Ill-1, 3rd to last in Ill-3

    #cosmology
    H0=70.
    h=H0/100.


    ##determine how many subhalos in simulation (also, accessing the subhalo catalogue)
    url='http://www.illustris-project.org/api/Illustris-'+str(Isim)+'/snapshots/'+str(snapNum)+'/subhalos/'
    subhalocat=get(url, {'limit':10000})

    subhalos =  subhalocat['results']
    subhal_m = []
    for i in range(len(subhalos)):
        subhal_m.append(subhalos[i]['mass_log_msun'])
    print len(subhal_m)
