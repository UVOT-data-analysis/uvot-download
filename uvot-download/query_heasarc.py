import numpy as np
import os
import argparse
import sys
import urllib.request

import pdb

def query_heasarc(input_obj, list_opt=None, search_radius=7.0,
                      create_folder=True, table_params=['obsid','start_time']):
    """
    Find observations of a target in HEASARC

    Parameters
    ----------
    input_obj : string or list of strings
        Name(s) of object(s) to search for; ignored if list_opt is set

    list_opt : string (default=None)
        Set to name of file that contains one column of object name(s)

    search_radius : float (default=7.0)
        Search radius (arcmin)

    create_folder : boolean (default=True)
        choose whether to create a sub-folder for the object(s) or save the
        table into the current directory

    table_params : list of strings (default=['obsid','start_time'])
        List of parameters to extract from the observing information.  The
        default params will be included in all queries.  More info (including
        allowed params) here:
        https://heasarc.gsfc.nasa.gov/W3Browse/swift/swiftmastr.html

    """

    #condition that handles either a list of entries from a file that needs to be loaded or a single object put into a list
    if list_opt is not None:
        obj_list = np.loadtxt(input_obj, dtype = 'str').tolist()
        #print('expect a list and do list things')
    else:
        obj_list = [input_obj]

    # ensure 'obsid' and 'start_time' are in table_params
    if 'obsid' not in table_params:
        table_params.append('obsid')
    if 'start_time' not in table_params:
        table_params.append('start_time')
    
    
    for obj in obj_list:

        #make new folders for each of the objects
        if create_folder:
            if not os.path.exists(obj):
                os.mkdir(obj)

        # file name to save the table
        if create_folder:
            output_file = obj + '/heasarc_obs.dat'
        else:
            output_file = obj+'_heasarc_obs.dat'

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
              '&Fields=&varon='+'&varon='.join(table_params) + \
              '&Entry='+urllib.request.quote(obj) + \
              '&displaymode=BatchDisplay' + \
              "' > " + output_file
              
        os.system(cmd)



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
