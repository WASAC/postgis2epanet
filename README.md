# PostGIS2EPANET

## postgis2epanet.py

A simple tool for exporting from a PostGIS table to EPANET INP file (You can find specification of INP file from [here](https://github.com/OpenWaterAnalytics/EPANET/wiki/Input-File-Format)) in Rwanda. Assumes 
[Python 3.6+](http://www.python.org/download/), 
[psycopg2](http://initd.org/psycopg/download/), 
[Shapely](https://github.com/Toblerity/Shapely), 
are already installed and in your ````PATH````.

The following is example of installation procedures by pip installation.
````
pip install psycopg2
pip install Shapely-1.6.4.post1-cp37-cp37m-win_amd64.whl
````
Shapely can be downloaded from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/). You can chose the file depends on your platform(32bit or 64bit, Python version, etc).

The tool was designed for RWSS department of WASAC in Rwanda.

####Example usage:

To export ````water pipeline network````from database ````rwss_assets```` as user ````user```` to EPANET INP fila(.inp) for each WSS and Districts:

Before running the script, kindly check the database settings at command line parameters.
````
python postgis2epanet.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword
````

If you want to filter only specific dictricts, use ````-l```` parameter to list ID of district by comma(,)

````
python postgis2inventoryreport.py -l 51,52,53
````

This script was developed by ````Jin IGARASHI, JICA Expert```` from ````The Project for Strengthening Operation and Maintenance of Rural Water Supply Systems in Rwanda- RWASOM````.