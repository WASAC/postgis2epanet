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
## Example usage:

To export ````water pipeline network````from database ````rwss_assets```` as user ````user```` to EPANET INP file(.inp) and ESRI Shapefiles for each WSS and Districts:

Before running the script, kindly check the database settings at command line parameters.
````
python postgis2epanet.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword
````

If you want to filter only specific dictricts, use ````-l```` parameter to list ID of district by comma(,)

````
python postgis2epanet.py -l 51,52,53
````

***
## Result of the Script:

A ZIP archive file as below will be created through this script.
````
20190813_170355_epanet_data.zip
````

After extracting ZIP archive, you will find other ZIP archive for each Districts as follows.
````
C:.
    21_Nyanza.zip
    22_Gisagara.zip
    23_Nyaruguru.zip
    24_Huye.zip
    25_Nyamagabe.zip
    26_Ruhango.zip
    27_Muhanga.zip
    28_Kamonyi.zip
    (skip)
````

Let us extract 24_Huye.zip here, you will see the following files as below. 
Name of file and folder is ID for water supply system. You can use INP file for EPANET, and you can also use Shapefiles for QGIS plugin.
````
C:.
│  2041.inp   <- This INP file is for EPANET application
│  20410.inp
│  20411.inp
│  (skip)
│  
├─2041  <- These Shapefiles under WSS_ID folder are for QGIS Plugin.
│      2041_junctions.dbf
│      2041_junctions.shp
│      2041_junctions.shx
│      2041_pipes.dbf
│      2041_pipes.shp
│      2041_pipes.shx
│      2041_reservoirs.dbf
│      2041_reservoirs.shp
│      2041_reservoirs.shx
│      2041_tanks.dbf
│      2041_tanks.shp
│      2041_tanks.shx
│      
├─20410
│      20410_junctions.dbf
│      20410_junctions.shp
│      20410_junctions.shx
│      (skip)
````

***
## How can we analyse after creating INP file/Shapefiles?
There are 3 options as follows.
1. Use EPANET application to do analysis. You can directly import INP file to EPANET.
    <br>![result](https://github.com/JinIgarashi/postgis2epanet/blob/master/images/how_to_use_qwater.jpg)
1. Use QGIS to analyse by ````QWater```` Plugin.
    <br>![result](https://github.com/JinIgarashi/postgis2epanet/blob/master/images/How%20to%20use%20QWater%20for%20EPANET%20on%20QGIS%20plugin.gif)
    1. You can double-click .qgz file to launch QGIS3.
    1. Install ````QWater```` Plugin on QGIS3. See manual of QWater [here](https://github.com/jorgealmerio/QWater/blob/master/tutorial_en.md).
    1. To do settings of layers again.
    1. To do make model again.
    1. If necessary, you can revise the following values for some layers.
        1.diameter of pipes (some diameter might be missing)
        1.demand of junctions (some no of users might be missing)
        1.water level & diameter of tanks (our DB don't have water level and diameter information, so I put the same values as default)
    1. Do analysis by ````QWater````
    <br>![result](https://github.com/JinIgarashi/postgis2epanet/blob/master/images/How%20to%20use%20QWater%20for%20EPANET%20on%20QGIS%20plugin.gif)

1. If you want to import existing INP file to QWater, please use both ````ImportEpanetInpFiles```` and ````QWater```` Plugin.
    1. Install ````ImportEpanetInpFiles```` plugin to import INP file to QGIS3.
    1. You can rename column name as following table.
    1. Install ````QWater```` to do analysis. 

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