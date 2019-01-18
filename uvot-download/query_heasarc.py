import numpy as np
import os
import stat
import argparse
import sys
import glob
import urllib.request
import subprocess

import pdb

def query_heasarc(input_obj, list_opt=None, search_radius=7.0):
    """
    Find observations of a target in HEASARC, create download script, and download the data

    Parameters
    ----------
    input_obj : string or list of strings
        Name(s) of object(s) to search for; ignored if list_opt is set

    list_opt : string (default=None)
        Set to name of file that contains one column of object name(s)

    search_radius : float (default=7.0)
        Search radius (arcmin)

    """

    #condition that handles either a list of entries from a file that needs to be loaded or a single object put into a list
    if list_opt is not None:
        obj_list = np.loadtxt(input_obj, dtype = 'str').tolist()
        #print('expect a list and do list things')
    else:
        obj_list = [input_obj]
    
    for obj in obj_list:

        #make new folders for each of the objects
        if not os.path.exists(obj):
            os.mkdir(obj)

        # command to generate HEASARC query
        #cmd = 'browse_extract_wget.pl table=swiftmastr position=' \
        #              + obj + ' radius='+str(search_radius) \
        #              +' fields=obsid,start_time outfile=data.dat'
        cmd = 'wget -O - -o /dev/null --no-check-certificate ' + "'" \
              'https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3query.pl?' + \
              'tablehead='+urllib.request.quote('name=BATCHRETRIEVALCATALOG_2.0 swiftmastr') + \
              '&Action=Query' + \
              '&Coordinates='+urllib.request.quote("'Equatorial: R.A. Dec'") + \
              '&Equinox=2000' + \
              '&Radius='+str(search_radius) + \
              '&NR=SIMBAD' + \
              '&GIFsize=0' + \
              '&Fields=&varon='+'&varon='.join(['obsid','start_time']) + \
              '&Entry='+urllib.request.quote(obj) + \
              '&displaymode=BatchDisplay' + "' > data.dat"
              
        os.system(cmd)

        # read in the query output
        with open('data.dat', 'r') as fh:
            rows_list = fh.readlines()

        if len(rows_list) == 1:
            print("No observations of " + obj + " were found in HEASARC.")
            dir_path = '*/*/*/' + gal
            r = glob.glob(dir_path)
            for i in r:
                os.remove(i)
            continue

        #run browse_extract with all of the parameters needed to make data.dat

        #important inputs for loadtxt:
        #comments: comments out last line that lists number of observations returned for an object
        #skiprows: skips first two rows in data.dat that are just for formatting

        #obslist = np.loadtxt('data.dat', dtype = 'str', delimiter = '|',
        #                         comments = 'S', skiprows = 2, usecols = (1,2)).tolist()
        obslist = np.loadtxt('data.dat', dtype = 'str', delimiter = '|',
                                 skiprows=3, comments='B', usecols = (1,2)).tolist()
        id_list = list()

        #if obslist is empty:
        #    continue to next obj in obj_list, though if there's nothing that comes next, will it just end the program?

        # prefix for all of the wget commands
        wget_prefix = "wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/swift/data/obs/"

        # make sure download script doesn't exist
        if os.path.isfile('download.scr'):
            os.remove('download.scr')
            

        #consideration for a case where target that does not exist in heasarc
        if len(obslist[0]) > 2:
            #print(obslist)
            obsid = obslist[0]
            starttime = obslist[1]
            start_month = starttime[0:7]
            start_month = start_month.replace('-','_')
            id_list.append(obsid)

        #    string addition to make wget commands for data download
            wget_uvot = wget_prefix + start_month + '//' + obsid + "/uvot/"
            wget_auxil = wget_prefix + start_month + '//' + obsid + "/auxil/"

            with open('download.scr', 'a') as download_scr:
                download_scr.write(wget_uvot + '\n')
                download_scr.write(wget_auxil + '\n')
                download_scr.write('mv '+obsid+' '+obj+'/ \n')
            
        else:
            for i in range(len(obslist)):
                #print(obslist[i])
                [obsid, starttime] = obslist[i]
        
                start_month = starttime[0:7]
                start_month = start_month.replace('-','_')
                id_list.append(obsid)
        
            #    string addition to make wget commands for data download
                wget_uvot = wget_prefix + start_month + '//' + obsid + "/uvot/"
                wget_auxil = wget_prefix + start_month + '//' + obsid + "/auxil/"

                with open('download.scr', 'a') as download_scr:
                    download_scr.write(wget_uvot + '\n')
                    download_scr.write(wget_auxil + '\n')
                    download_scr.write('mv '+obsid+' '+obj+'/ \n')

        #run the download script here and put the results in the directories created at the beginning of the list

        #make download script executable
        print("* running download script for "+obj)
        os.system('sh download.scr')

        #unzip all the downloaded data
        os.system('gunzip */*/*.gz')
        os.system('gunzip */*/*/*.gz')
        os.chdir('..')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_obj', nargs="?", help="Accepts either the object name as a string or a text file with a list of object names", default='')
    parser.add_argument('-l','--list', help="query_heasarc will expect the name of a text file that contains a list of objects.", action='store_true', default=False)
    args = parser.parse_args()

    if not args.input_obj:
        print('Please specify an object or list of objects you would like to search for.') 
        sys.exit()

    query_heasarc(args.input_obj, list_opt=args.list)

if __name__ =="__main__":
    main()
