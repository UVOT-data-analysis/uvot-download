Code to download UVOT data
--------------------------

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge


This package contains Python code to search for UVOT images and/or download
them.  Its goal is to be a convenient method to do automated downloads
from `HEASARC
<https://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/swift.pl>`_.

Detailed explanations of keywords and defaults are in the docstrings of the two pieces of code, but this gives a brief overview of typical usage.

Use ``query_heasarc.py`` to determine what observations exist.  Here is an example for DDO68, using a 7 arcmin search radius.  (Note that the pointing accuracy of Swift is ~few arcmin, so take that into account when setting the search radius.)  To simply display a table:

    >>> import query_heasarc
    >>> query_heasarc.query_heasarc('DDO68', search_radius=7, display_table=True)
    |obsid      |start_time         |uvot_expo_w2|uvot_expo_m2|uvot_expo_w1|_offset|
    +-----------+-------------------+------------+------------+------------+-------+
    |00084312006|2018-01-23T16:47:57|   108.76300|   108.78500|   116.24300| 0.4555|
    |00084312010|2018-10-07T15:48:57|   240.77100|   240.78200|   241.77500| 0.7567|
    |00084312005|2016-09-30T17:23:58|   920.31100|   920.32200|   639.41300| 1.0193|
    |00084312011|2018-10-17T10:10:57|    43.76800|    43.75700|    32.71300| 1.0342|
    |00084312009|2018-10-06T20:43:57|   171.77200|   171.77200|   126.96700| 1.1702|
    |00084312013|2019-01-24T07:26:34|   122.70800|   122.77400|   151.26100| 1.3822|
    |00084312007|2018-01-28T08:27:57|    95.72200|    95.76600|    87.88800| 1.8064|
    |00084312015|2019-03-07T13:02:36|   170.72300|   170.77900|   159.10600| 2.1950|
    |00084312003|2016-01-11T06:48:57|   168.76000|   168.77100|   139.85300| 2.8399|
    |00084312001|2015-06-26T20:14:33|   147.77500|   147.76400|    51.36900| 2.8994|
    |00084312014|2019-02-24T18:56:36|   225.76700|   225.77800|   213.73000| 2.9978|
    |00084312012|2018-12-30T21:03:34|   272.76700|   272.76700|   256.39400| 3.0588|
    |00084312004|2016-06-25T02:29:58|   662.53800|   662.54900|   642.95400| 3.0910|


To save to a file instead (automatically named ``DDO68_heasarc_obs.dat``):

    >>> query_heasarc.query_heasarc('DDO68', search_radius=7, create_folder=False)

You can also query using coordinates (or any other format allowed on the HEASARC website).  Here is an example with NGC24 (which has observations) and Leoncino (which does not have observations).

    >>> query_heasarc.query_heasarc('00h09m56.5s -24d57m47s', search_radius=10, display_table=True)
    00h09m56.5s -24d57m47s
    
    |obsid      |start_time         |uvot_expo_w2|uvot_expo_m2|uvot_expo_w1|_offset|
    +-----------+-------------------+------------+------------+------------+-------+
    |00045594006|2012-10-21T10:01:58|  2162.60700|  2162.65100|  1952.97000| 0.7272|
    |00045594009|2012-11-09T23:56:59|    53.76300|    53.78500|    49.65900| 1.1321|
    |00045594011|2012-11-15T09:43:59|   174.77200|   174.77200|   171.60600| 1.5419|
    |00045594007|2012-10-24T10:07:59|     0.00000|     0.00000|     0.00000| 1.8431|
    |00045594008|2012-11-07T02:53:59|   247.53500|   247.54600|   200.19200| 1.9819|
    |00045594013|2012-11-18T17:55:59|  2100.60200|  2100.64600|  2012.14000| 2.0059|
    |00045594001|2011-09-19T10:38:00|   513.77000|   513.77000|   459.95100| 2.0234|
    |00045594010|2012-11-13T19:15:59|   133.77400|   133.77400|    79.34900| 2.2041|
    |00045594005|2012-04-25T11:29:00|  1381.29900|  1381.33200|  1267.16400| 2.3406|
    |00045594012|2012-11-16T22:32:59|   387.53100|   387.55300|   371.68800| 2.3504|
    |00045594004|2012-04-24T08:10:00|  2290.84200|  2290.89700|  2063.00100| 3.7228|
    |00045594003|2012-01-27T08:53:00|   131.66700|     0.00000|     0.00000| 4.6665|
    |00045594002|2011-09-20T22:16:00|     0.00000|     0.00000|     0.00000| 7.5074|
    
    No observations of 09h43m32.4s +33d26m58s found in HEASARC (check Quick Look page for any recent observations)


Use ``download_heasarc.py`` to use a saved table to download the data.

    >>> import download_heasarc
    >>> download_heasarc.download_heasarc('DDO68_heasarc_obs.dat')

If you've already downloaded some data, but new observations have been taken since then, ``download_heasarc`` will only download the new data (this can be overridden with ``download_all=True``).  FITS files from HEASARC are gzipped, so the code will also automatically unzip them (unless ``unzip=False``).



License
-------

This project is Copyright (c) Lea Hagen and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.


Contributing
------------

New contributions and contributors are always welcome!  Contact
@lea-hagen for more information.
