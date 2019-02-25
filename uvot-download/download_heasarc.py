import numpy as np
import os
import glob
import subprocess
import pdb


def download_heasarc(heasarc_files, unzip=True, download_all=False):
    """
    Using the observation table from query_heasarc, create a download script,
    download the data, and unzip everything.  All files will be saved into the
    same directory as the HEASARC observation table.

    Parameters
    ----------
    heasarc_files : string or list of strings
        Name(s) of the file(s) with the observation table(s) generated by
        query_heasarc.py

    unzip : boolean (default=True)
        Choose whether to unzip all of the downloaded files

    download_all : boolean (default=False)
        If True, download all data.  If False, only download new data (as
        determined by existence of a folder with the relevant obsid).

    """

    # check if input is string or list
    if type(heasarc_files) == str:
        file_list = [heasarc_files]
    if type(heasarc_files) == list:
        file_list = heasarc_files


    for filename in file_list:

        # galaxy name
        gal_name = os.path.realpath(filename).split('/')[-2]
    
        # read in the query output
        with open(filename, 'r') as fh:
            rows_list = fh.readlines()

        # the file has 2 lines if there aren't any observations
        if len(rows_list) == 2:
            print("No observations of " + gal_name + " were found in HEASARC.")
            dir_path = os.path.dirname(filename)
            r = glob.glob(dir_path)
            #for i in r:
            #    os.remove(i)
            continue

        # extract the columns that were saved
        table_cols = [col.strip() for col in rows_list[1].split('|') if (col != '' and col != '\n')]
        # the last one is always '_offset', which we don't care about
        table_cols = table_cols[0:-1]

        #important inputs for loadtxt:
        #comments: comments out last line that lists number of observations returned for an object
        #skiprows: skips first two rows in data.dat that are just for formatting

        #obslist = np.loadtxt(filename, dtype = 'str', delimiter = '|',
        #                         comments = 'S', skiprows = 2, usecols = (1,2)).tolist()
        obslist = np.loadtxt(filename, dtype = 'str', delimiter = '|',
                                 skiprows=3, comments='B',
                                 usecols = tuple(np.arange(0,len(table_cols))+1) ).tolist()
        id_list = list()

        #if obslist is empty:
        #    continue to next obj in obj_list, though if there's nothing that comes next, will it just end the program?

        # path where things will get saved
        save_path = '/'.join( os.path.realpath(filename).split('/')[:-1] )

        # prefix for all of the wget commands
        wget_prefix = "wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np -R 'index*' -erobots=off --directory-prefix="+save_path+" --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/swift/data/obs/"

        # path+name for download file
        download_file = save_path + '/download.scr'
        
        # make sure download script doesn't exist
        if os.path.isfile(download_file):
            os.remove(download_file)
            

        #condition that handles cases where HEASARC query returns only one row or zero rows
        if type(obslist[0]) == str:
            #print(obslist)
            obsid = obslist[0]
            starttime = obslist[1]
            start_month = starttime[0:7]
            start_month = start_month.replace('-','_')
            id_list.append(obsid)

        #    string addition to make wget commands for data download
            wget_uvot = wget_prefix + start_month + '//' + obsid + "/uvot/"
            wget_auxil = wget_prefix + start_month + '//' + obsid + "/auxil/"

            # only add this observation to the script if:
            # - folder for this obsid doesn't exist
            # - folder does exist, but download_all is True
            if (not os.path.isdir(save_path+'/'+obsid)) or (os.path.isdir(save_path+'/'+obsid) and download_all==True):
                with open(download_file, 'a') as download_scr:
                    download_scr.write(wget_uvot + '\n')
                    download_scr.write(wget_auxil + '\n')
            
        elif len(obslist[0]) == 0:
            print("* Search of table swiftmastr around "+gal_name+" returns 0 rows.")
            print("* Looks like there's no observation data for this object.")
            print("* Check to make sure that this object has been observed. Moving on...")
            continue

        else:
            for i in range(len(obslist)):
                #print(obslist[i])
                obsid = obslist[i][table_cols.index('obsid')]
                starttime = obslist[i][table_cols.index('start_time')]
        
                start_month = starttime[0:7]
                start_month = start_month.replace('-','_')
                id_list.append(obsid)
        
            #    string addition to make wget commands for data download
                wget_uvot = wget_prefix + start_month + '//' + obsid + "/uvot/"
                wget_auxil = wget_prefix + start_month + '//' + obsid + "/auxil/"

                # only add this observation to the script if:
                # - folder for this obsid doesn't exist
                # - folder does exist, but download_all is True
                if (not os.path.isdir(save_path+'/'+obsid)) or (os.path.isdir(save_path+'/'+obsid) and download_all==True):
                    with open(download_file, 'a') as download_scr:
                        download_scr.write(wget_uvot + '\n')
                        download_scr.write(wget_auxil + '\n')

        #run the download script here and put the results in the directories created at the beginning of the list


        # run download script
        # (but only if there are items to download)
        if os.path.isfile(download_file):
            print("* running download script for "+gal_name)
            os.system('sh '+download_file)
        else:
            print('* no new observations of '+gal_name+' to download')

        #unzip all the downloaded data
        if unzip:
            print('* unzipping files')
            for i in id_list:
                gz_files = glob.glob(save_path+'/'+i+'/**/*.gz', recursive=True)
                for gz in gz_files:
                    # only unzip if the unzipped file doesn't exist
                    if not os.path.isfile(gz[:-3]):
                        subprocess.run('gunzip '+gz, shell=True)
    

