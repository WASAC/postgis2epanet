import os
import datetime
import argparse
from database import Database
from district import Districts
from epanet.coordinates import Coordinates
from epanet.pipes import Pipes
from epanet.reservoirs import Reservoirs
from epanet.tanks import Tanks
from epanet.pumps import Pumps
from epanet.options import Options


def create_argument_parser():
    """
     Create the parameters for the script
    """
    parser = argparse.ArgumentParser(
        description="Create a QField datasets from PostGIS database.",
        epilog="Example usage: python postgis2qfield.py -d yourdatabase -H localhost - p 5432 "
               "-u user -w securePassword -l list_of_distID(seperated by comma)"
    )
    parser.add_argument("-d", "--database", dest="database",
                        type=str, required=True,
                        help="The database to connect to")

    # Python doesn't let you use -h as an option for some reason
    parser.add_argument("-H", "--host", dest="host",
                        default="localhost", type=str,
                        help="Database host. Defaults to 'localhost'")

    parser.add_argument("-p", "--port", dest="port",
                        default="5432", type=str,
                        help="Password for the database user")

    parser.add_argument("-u", "--user", dest="user",
                        default="postgres", type=str,
                        help="Database user. Defaults to 'postgres'")

    parser.add_argument("-w", "--password", dest="password",
                        type=str, required=True,
                        help="Password for the database user")

    parser.add_argument("-l", "--dist_id", dest="dist_id",
                        default="", type=str,
                        help="List of district ID which you want to export. For example, '51,52,53'")

    return parser.parse_args()


if __name__ == "__main__":
    args = create_argument_parser()
    db = Database(args)
    districts_obj = Districts(args.dist_id)
    districts = districts_obj.get_wss_list_each_district(db)
    main_dir = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_epanet_data"
    for dist in districts:
        export_dir = "{0}/{1}".format(main_dir, dist.dist_id)
        os.makedirs(export_dir, exist_ok=True)
        for wss_id in dist.wss_id_list.split(","):
            with open("{0}/{1}.inp".format(export_dir, wss_id), 'a') as f:
                coords = Coordinates(wss_id)
                coords.get_data(db)

                reservoirs = Reservoirs(wss_id, coords)
                reservoirs.get_data(db)

                tanks = Tanks(wss_id, coords)
                tanks.get_data(db)

                pipes = Pipes(wss_id, coords)
                pipes.get_data(db)

                pumps = Pumps(wss_id, coords, pipes.pipes)
                pumps.get_data(db)

                options = Options()

                coords.export_junctions(f)
                reservoirs.export(f)
                tanks.export(f)
                pipes.export(f)
                pumps.export(f)
                options.export(f)
                coords.export_coordinates(f)
