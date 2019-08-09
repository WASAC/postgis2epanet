import os
import shutil
import datetime
from util.database import Database
from util.district import Districts
from epanet.common import Common
from epanet.coordinates import Coordinates
from epanet.pipes import Pipes
from epanet.reservoirs import Reservoirs
from epanet.tanks import Tanks
from epanet.pumps import Pumps


class Tasks(object):
    def __init__(self, args):
        self.db = Database(args)
        districts_obj = Districts(args.dist_id)
        self.districts = districts_obj.get_wss_list_each_district(self.db)
        self.main_dir = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_epanet_data"

    def get_tasks(self):
        obj_list = []
        for dist in self.districts:
            export_dir = "{0}/{1}".format(self.main_dir, dist.dist_id)
            os.makedirs(export_dir, exist_ok=True)
            for wss_id in dist.wss_id_list.split(","):
                obj_list.append(Tasks.Task(self.db, dist, export_dir, wss_id))
        return obj_list

    def archive(self):
        shutil.make_archive(self.main_dir, 'zip', root_dir=self.main_dir)
        shutil.rmtree(self.main_dir)

    class Task(object):
        def __init__(self, db, district, export_dir, wss_id):
            self.db = db
            self.dist = district
            self.export_dir = export_dir
            self.export_file = "{0}/{1}.inp".format(export_dir, wss_id)
            self.wss_id = wss_id

        def execute(self):
            with open(self.export_file, 'a') as f:
                coords = Coordinates(self.wss_id)
                coords.get_data(self.db)

                reservoirs = Reservoirs(self.wss_id, coords)
                reservoirs.get_data(self.db)

                tanks = Tanks(self.wss_id, coords)
                tanks.get_data(self.db)

                pipes = Pipes(self.wss_id, coords)
                pipes.get_data(self.db)

                pumps = Pumps(self.wss_id, coords, pipes.pipes)
                pumps.get_data(self.db)

                common = Common()
                common.start(f, "{0} WSS in {1} District".format(self.wss_id, self.dist.district))
                coords.export_junctions(f)
                reservoirs.export(f)
                tanks.export(f)
                pipes.export(f)
                pumps.export(f)
                common.export_tags(f)
                pumps.export_curve(f)
                common.export_options(f)
                coords.export_coordinates(f)
                common.end(f)

                coords.export_shapefile(f)
                pipes.export_shapefile(f)
                tanks.export_shapefile(f)
                reservoirs.export_shapefile(f)
                pumps.export_shapefile(f)
