# PostGIS2EPANET

## postgis2epanet.py

A simple tool for exporting from a PostGIS table to EPANET INP file (You can find specification of INP file from [here](https://github.com/OpenWaterAnalytics/EPANET/wiki/Input-File-Format)) in Rwanda. Assumes 
[Python 3.6+](http://www.python.org/download/), 
[psycopg2](http://initd.org/psycopg/download/), 
[Shapely](https://github.com/Toblerity/Shapely), 
[PyShp](https://github.com/GeospatialPython/pyshp),
[light-progress](https://pypi.org/project/light-progress/),
are already installed and in your ````PATH````.

The following is example of installation procedures by pip installation.
````
pip install psycopg2
pip install Shapely-1.6.4.post1-cp37-cp37m-win_amd64.whl
pip install pyshp
pip install light-progress
````
Shapely can be downloaded from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/). You can chose the file depends on your platform(32bit or 64bit, Python version, etc).

The tool was designed for RWSS department of WASAC in Rwanda.

***
###Example usage:

To export ````water pipeline network````from database ````rwss_assets```` as user ````user```` to EPANET INP fila(.inp) for each WSS and Districts:

Before running the script, kindly check the database settings at command line parameters.
````
python postgis2epanet.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword
````

If you want to filter only specific dictricts, use ````-l```` parameter to list ID of district by comma(,)

````
python postgis2inventoryreport.py -l 51,52,53
````

***
###What shall we do after creating INP file?
There are 2 options as follow.
1. Use EPANET application to do analysis. You can directly import INP file to EPANET.
1. Use QGIS to analyse by ````QEPANET```` Plugin.
    1. Import Shapefiles for each WSS to QGIS3.
    1. Install ````QEPANET```` Plugin on QGIS3.
    1. Do analysis by ````QEPANET````
1. Use QGIS to analyse by both ````ImportEpanetInpFiles```` and ````QEPANET```` Plugin.
    1. Install ````ImportEpanetInpFiles```` plugin to import INP file to QGIS3.
    1. You can rename column name as following table.
    1. Install ````QEPANET```` to do analysis. 

Table. Renaming columnname for QEPANET from ImportEpanetInpFiles plugin

|Layer|Old column name|New column name|
|:---|:---|:---|
|Junctions|ID|DC_ID|
|Junctions|Demand1|DEMAND|
|Junctions|Pattern1|PATTERN|
|Pipes|ID|DC_ID|
|Pipes|NodeFrom|NODE1|
|Pipes|NodeTo|NODE2|
|Reservoirs|ID|DC_ID|
|Reservoirs|Pattern1|PATTERN|
|Tanks|ID|DC_ID|
|Tanks|InitLevel|INITIALLEV|
|Tanks|MinLevel|MINIMUMLEV|
|Tanks|MaxLevel|MAXIMUMLEV|
|Tanks|MinVolume|MINIMUMVOL|
|Pumps|ID|DC_ID|
|Pumps|NodeFrom|Initi|
|Pumps|NodeTo|NODE2|
|Valves|ID|DC_ID|
|Valves|NodeFrom|NODE1|
|Valves|NodeTo|NODE2|


***
This script was developed by ````Jin IGARASHI, JICA Expert```` from ````The Project for Strengthening Operation and Maintenance of Rural Water Supply Systems in Rwanda (RWASOM)````.