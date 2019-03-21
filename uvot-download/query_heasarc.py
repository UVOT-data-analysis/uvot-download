import numpy as np
import os
import argparse
import sys
import urllib.request
import subprocess

import pdb

def query_heasarc(input_obj, list_opt=False, search_radius=7.0,
                      create_folder=True,
                      table_params=['obsid','start_time','uvot_expo_w2','uvot_expo_m2','uvot_expo_w1'],
                      display_table=False):
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

    display_table : boolean (default=False)
        If True, instead of saving the table to a file, display it in the
        terminal window.  Useful for quick checks of observations.

    """

    #condition that handles either a list of entries from a file that needs to be loaded or a single object put into a list
    if list_opt is not False:
        obj_list = np.loadtxt(input_obj, dtype = 'str').tolist()
        #print('expect a list and do list things')
    else:
        if type(input_obj) == str:
            obj_list = [input_obj]
        if type(input_obj) == list:
            obj_list = input_obj

    # ensure defaults are in table_params
    for col in ['obsid','start_time','uvot_expo_w2','uvot_expo_m2','uvot_expo_w1']:
        if col not in table_params:
            table_params.append(col)    
    
    for obj in obj_list:

        # replace any spaces with underscores for saving things
        obj_nospace = obj.replace(' ','_')

        #make new folders for each of the objects
        if (create_folder == True) and (display_table == False):
            if not os.path.exists(obj_nospace):
                os.mkdir(obj_nospace)

        # file name to save the table
        if create_folder:
            output_file = obj_nospace + '/heasarc_obs.dat'
        else:
            output_file = obj_nospace+'_heasarc_obs.dat'

        # but if it's going to be displayed, the end of the command needs modifying
        if display_table == False:
            save_cmd = ' > ' + output_file
        else:
            save_cmd = ''

        # command to generate HEASARC query
        #cmd = 'browse_extract_wget.pl table=swiftmastr position=' \
        #              + obj + ' radius='+str(search_radius) \
        #              +' fields=obsid,start_time outfile=data.dat'

        NR_list = ['NED','SIMBAD']
            
        for NR in NR_list:
            cmd = 'wget -O - -o /dev/null --no-check-certificate ' + "'" \
              'https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3query.pl?' + \
              'tablehead='+urllib.request.quote('name=BATCHRETRIEVALCATALOG_2.0 swiftmastr') + \
              '&Action=Query' + \
              '&Coordinates='+urllib.request.quote("'Equatorial: R.A. Dec'") + \
              '&Equinox=2000' + \
              '&Radius='+str(search_radius) + \
              '&NR='+NR + \
              '&GIFsize=0' + \
              '&Fields=&varon='+'&varon='.join(table_params) + \
              '&Entry='+urllib.request.quote(obj) + \
              '&displaymode=BatchDisplay' + "'" + save_cmd

            # run the command
            wget_output = subprocess.run(cmd + save_cmd, stdout=subprocess.PIPE, shell=True)
              
            # read in the query output to make sure it worked
            if display_table == False:
                with open(output_file, 'r') as hf:
                    rows_list = hf.readlines()
            else:
                rows_list = wget_output.stdout.decode('utf-8').split('\n')

            # error -> try other name resolver
            if ('ERROR' in rows_list[0].upper()) and (NR != NR_list[-1]):
                print('could not resolve '+obj+' with '+NR+', trying next name resolver')
                continue
            # error, but already tried all name resolvers
            elif ('ERROR' in rows_list[0].upper()) and (NR == NR_list[-1]):
                print('could not resolve '+obj+' with '+NR)
                print('failed to resolve '+obj)
                continue
            # no error -> finish
            else:
                if len(rows_list) == 3:
                    print('No observations of '+obj+' found in HEASARC (check Quick Look page for any recent observations)')
                if (display_table == True) and (len(rows_list) > 3):
                    print('\n'+obj+'\n')
                    for row in rows_list[1:-2]:
                        print(row)
                    print('')
                break


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
