import os
import shutil
import datetime
from util.database import Database
from util.district import Districts
from util.wss import WaterSupplySystems
from epanet.common import Common
from epanet.coordinates import Coordinates
from epanet.pipes import Pipes
from epanet.reservoirs import Reservoirs
from epanet.tanks import Tanks
from epanet.pumps import Pumps
from epanet.valves import Valves
from epanet.connections import Connections


class Tasks(object):
    def __init__(self, args):
        self.db = Database(args)
        districts_obj = Districts(args.dist_id)
        self.districts = districts_obj.get_wss_list_each_district(self.db)
        self.main_dir = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_epanet_data"
        self.exportdir_list = []
        wss_list_obj = WaterSupplySystems()
        wss_list_obj.update_elevations(self.db)
        self.wss_list = wss_list_obj.get_wss_list(self.db)

    def get_tasks(self):
        obj_list = []
        for dist in self.districts:
            export_dir = "{0}/{1}_{2}".format(self.main_dir, dist.dist_id, dist.district)
            self.exportdir_list.append(export_dir)
            os.makedirs(export_dir, exist_ok=True)
            for wss_id in dist.wss_id_list.split(","):
                wss = self.wss_list[str(wss_id)]
                obj_list.append(Tasks.Task(self.db, dist, export_dir, wss))
        return obj_list

    def archive(self, directory):
        shutil.make_archive(directory, 'zip', root_dir=directory)
        shutil.rmtree(directory)

    def archive_all(self):
        for path in self.exportdir_list:
            self.archive(path)
        self.archive(self.main_dir)

    class Task(object):
        def __init__(self, db, district, export_dir, wss):
            self.db = db
            self.dist = district
            self.export_dir = export_dir
            self.wss_id = wss.wss_id
            self.wss_name = wss.wss_name
            self.export_file = "{0}/{1}_{2}.inp".format(export_dir, self.wss_id, self.wss_name)

        def execute(self):
            with open(self.export_file, 'a', encoding='UTF-8') as f:
                coords = Coordinates(self.wss_id)
                coords.get_data(self.db)

                conns = Connections(self.wss_id)
                conns.get_data(self.db)
                coords.add_demands(conns.connections)

                reservoirs = Reservoirs(self.wss_id, coords)
                reservoirs.get_data(self.db)

                tanks = Tanks(self.wss_id, coords)
                tanks.get_data(self.db)

                pipes = Pipes(self.wss_id, coords)
                pipes.get_data(self.db)

                pumps = Pumps(self.wss_id, coords, pipes.pipes)
                pumps.get_data(self.db)

                valves = Valves(self.wss_id, coords, pipes.pipes)
                valves.get_data(self.db)

                common = Common()
                common.start(f, "{0} {1} WSS in {2} District".format(self.wss_id, self.wss_name, self.dist.district))
                coords.export_junctions(f)
                reservoirs.export(f)
                tanks.export(f)
                #join lists of pipes id which duplicates from pumps and valves.
                del_pipes_id = []
                del_pipes_id.extend( pumps.get_del_pipes_id_for_inp())
                del_pipes_id.extend(valves.get_del_pipes_id_for_inp())
                pipes.export(f, del_pipes_id)
                pumps.export(f)
                valves.export(f)
                common.export_tags(f)
                pumps.export_curve(f)
                common.export_options(f)
                coords.export_coordinates(f)
                common.end(f)

                # join lists of coordinate id which duplicates from pumps and valves.
                del_coords_id = []
                del_coords_id.extend(pumps.get_del_coords_id_for_inp())
                del_coords_id.extend(valves.get_del_coords_id_for_inp())
                coords.export_shapefile(f, del_coords_id)
                pipes.export_shapefile(f)
                tanks.export_shapefile(f)
                reservoirs.export_shapefile(f)
                pumps.export_shapefile(f)
                valves.export_shapefile(f)
                shutil.copy("./templates/template_qgs_project.qgz", "{0}/{1}_{2}.qgz".format(f.name.replace(".inp", ""), self.wss_id, self.wss_name))
