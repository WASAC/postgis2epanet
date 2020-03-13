import argparse
from epanet.tasks import Tasks
from util.taskmanager import TaskManager
import atexit
import os
import json


def create_argument_parser():
    """
     Create the parameters for the script
    """
    parser = argparse.ArgumentParser(
        description="Create EPANET INP file each WSS/District from PostGIS database.",
        epilog="Example usage: python postgis2epanet.py -d yourdatabase -H localhost - p 5432 "
               "-u user -w securePassword -l list_of_distID(seperated by comma) -e(optional)"
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

    parser.add_argument("-e", "--elevation", action="store_true",
                        default=False,
                        help="If you use this option, the script is going to update elevation field of all layers.")

    parser.add_argument("-c", "--config", dest="config",
                        default="config.json",
                        help="Configuration file path. It should be put at the same folder of postgis2epanet.py")

    return parser.parse_args()


if __name__ == "__main__":
    args = create_argument_parser()
    root = os.path.dirname(os.path.abspath(__file__))
    args.config="{0}/{1}".format(root, args.config)
    t = Tasks(args)
    tasks = t.get_tasks()
    tm = TaskManager(tasks)
    tm.start()
    atexit.register(t.archive_all)
