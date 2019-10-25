import shapefile
from epanet.layer_base import LayerBase


class Valves(LayerBase):
    class Valve(object):
        def __init__(self, id, lon, lat, elevation, diameter, valve_type):
            self.id = "{0}-{1}".format(valve_type, str(id))
            self.lon = round(lon, 6)
            self.lat = round(lat, 6)
            self.diameter = float(diameter or 0.0)
            self.valve_type = valve_type
            self.setting = 0
            self.minor_loss = 0.0
            self.node1 = ""
            self.node2 = ""
            self.elevation = elevation

        def set_node(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

        @staticmethod
        def create_header(f):
            f.writelines("[VALVES]\n")
            f.writelines(";{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n"
                         .format("ID\t".expandtabs(20),
                                 "Node1\t".expandtabs(16),
                                 "Node2\t".expandtabs(16),
                                 "Diameter\t".expandtabs(12),
                                 "Type\t".expandtabs(12),
                                 "Setting\t".expandtabs(12),
                                 "MinorLoss\t".expandtabs(12),
                                 ))

        def add(self, f):
            f.writelines(" {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t;\n"
                         .format("{0}\t".format(self.id).expandtabs(20),
                                 "{0}\t".format(str(self.node1)).expandtabs(20),
                                 "{0}\t".format(str(self.node2)).expandtabs(20),
                                 "{0}\t".format(str(self.diameter)).expandtabs(12),
                                 "{0}\t".format(str(self.valve_type)).expandtabs(12),
                                 "{0}\t".format(str(self.setting)).expandtabs(12),
                                 "{0}\t".format(str(self.minor_loss)).expandtabs(12)
                                 ))

    def __init__(self, wss_id, coords, pipes):
        super().__init__("valves", wss_id)
        self.coords = coords
        self.pipes = pipes
        self.valves = []
        self.del_pipes_id = []
        self.del_coords_id = []

    def get_del_pipes_id_for_inp(self):
        return self.del_pipes_id

    def get_del_coords_id_for_inp(self):
        return self.del_coords_id

    def get_data(self, db):
        query = " SELECT a.chamber_id, st_x(a.geom) as lon, st_y(a.geom) as lat, " \
                "a.elevation, max(b.pipe_size) as diameter, " \
                "case a.chamber_type when 'Valve chamber' then 'TCV' when 'PRV chamber' then 'PRV' END as valve_type " \
                " FROM chamber a INNER JOIN pipeline b ON st_intersects(a.geom, b.geom) " \
                " WHERE a.wss_id = {0} and a.chamber_type IN ('Valve chamber', 'PRV chamber') " \
                " GROUP BY chamber_id, lon, lat, elevation ".format(self.wss_id)
        result = db.execute(query)
        for data in result:
            id = data[0]
            lon = data[1]
            lat = data[2]
            elevation = data[3]
            diamater = data[4]
            valve_type = data[5]
            valve = Valves.Valve(id, lon, lat, elevation, diamater, valve_type)
            self.valves.append(valve)

            target_key = ",".join([str(valve.lon), str(valve.lat)])
            if target_key in self.coords.coordMap and self.coords.coordMap[target_key]:
                coord = self.coords.coordMap[target_key]
                nodeid = coord.id
                self.del_coords_id.append(coord.id)
                del_pipe_idx = -1
                for p in self.pipes:
                    if nodeid == p.node1 or nodeid == p.node2:
                        valve.set_node(p.node1, p.node2)
                        del_pipe_idx = p.id
                if del_pipe_idx != -1:
                    self.del_pipes_id.append(del_pipe_idx)

    def export(self, f):
        Valves.Valve.create_header(f)
        for v in self.valves:
            v.add(f)
        f.writelines("\n")

    def export_shapefile(self, f):
        if len(self.valves) == 0:
            return
        filename = self.get_file_path(f)
        with shapefile.Writer(filename) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'C', 254)
            _shp.field('diameter', 'N', 20, 9)
            _shp.field('type', 'C', 254)
            _shp.field('setting', 'C', 254)
            _shp.field('minorloss', 'N', 20, 9)
            for v in self.valves:
                _shp.point(float(v.lon), float(v.lat))
                _shp.record(v.id, v.elevation, v.diameter, v.valve_type, v.setting, v.minor_loss)
            _shp.close()
        self.createProjection(filename)
