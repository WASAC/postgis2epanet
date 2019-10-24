import shapefile
from epanet.layer_base import LayerBase


class Pumps(LayerBase):
    class Pump(object):
        def __init__(self, id, lon, lat, elevation, flow, head):
            self.id = "Pump-" + str(id)
            self.lon = round(lon, 6)
            self.lat = round(lat, 6)
            self.curve = Pumps.PumpCurve(id, flow, head)
            self.parameter = "Head " + str(self.curve.id)
            self.node1 = ""
            self.node2 = ""
            self.elevation = elevation

        def set_node(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

        @staticmethod
        def create_header(f):
            f.writelines("[PUMPS]\n")
            f.writelines(";{0}\t{1}\t{2}\t{3}\n"
                         .format("ID\t".expandtabs(20),
                                 "Node1\t".expandtabs(20),
                                 "Node2\t".expandtabs(20),
                                 "Parameters\t".expandtabs(12)
                                 ))

        def add(self, f):
            f.writelines(" {0}\t{1}\t{2}\t{3}\t;\n"
                         .format("{0}\t".format(self.id).expandtabs(20),
                                 "{0}\t".format(str(self.node1)).expandtabs(20),
                                 "{0}\t".format(str(self.node2)).expandtabs(20),
                                 "{0}\t".format(str(self.parameter)).expandtabs(12)
                                 ))

    class PumpCurve(object):
        def __init__(self, id, flow, head):
            self.id = "curve_{0}".format(id)
            self.flow = flow
            self.head = head

        @staticmethod
        def create_header(f):
            f.writelines("[CURVES]\n")
            f.writelines(";{0}\t{1}\t{2}\n"
                         .format("ID\t".expandtabs(16),
                                 "X-Value\t".expandtabs(12),
                                 "Y-Value\t".expandtabs(12)
                                 ))

        def add(self, f):
            f.writelines(" {0}\t{1}\t{2}\t;\n"
                         .format("{0}\t".format(self.id).expandtabs(16),
                                 "{0}\t".format(str(self.flow)).expandtabs(12),
                                 "{0}\t".format(str(self.head)).expandtabs(12)
                                 ))

    def __init__(self, wss_id, coords, pipes):
        self.wss_id = wss_id
        self.coords = coords
        self.pipes = pipes
        self.pumps = []
        self.del_pipes_id = []
        self.del_coords_id = []

    def get_del_pipes_id_for_inp(self):
        return self.del_pipes_id

    def get_del_coords_id_for_inp(self):
        return self.del_coords_id

    def get_data(self, db):
        query = " SELECT pumpingstation_id as id, st_x(geom) as lon, st_y(geom) as lat, " \
                "elevation, head_pump, discharge_pump  "
        query += " FROM pumping_station WHERE wss_id={0} ".format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            id = data[0]
            lon = data[1]
            lat = data[2]
            elevation = data[3]
            head = data[4]
            discharge = data[5]
            pump = Pumps.Pump(id, lon, lat, elevation, discharge, head)
            self.pumps.append(pump)

            target_key = ",".join([str(pump.lon), str(pump.lat)])
            if target_key in self.coords.coordMap and self.coords.coordMap[target_key]:
                coord = self.coords.coordMap[target_key]
                nodeid = coord.id
                self.del_coords_id.append(coord.id)
                del_pipe_idx = -1
                for p in self.pipes:
                    if nodeid == p.node1 or nodeid == p.node2:
                        pump.set_node(p.node1, p.node2)
                        del_pipe_idx = p.id
                if del_pipe_idx != -1:
                    self.del_pipes_id.append(del_pipe_idx)

    def export(self, f):
        Pumps.Pump.create_header(f)
        for p in self.pumps:
            p.add(f)
        f.writelines("\n")

    def export_curve(self, f):
        Pumps.PumpCurve.create_header(f)
        for p in self.pumps:
            p.curve.add(f)
        f.writelines("\n")

    def export_shapefile(self, f):
        if len(self.pumps) == 0:
            return
        filename = "{0}/{1}_{2}".format(f.name.replace(".inp", ""), self.wss_id, "pumps")
        with shapefile.Writer(filename) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'C', 254)
            _shp.field('head', 'C', 254)
            _shp.field('flow', 'C', 254)
            _shp.field('power', 'N', 20, 9)
            _shp.field('properties', 'C', 254)
            for p in self.pumps:
                _shp.point(float(p.lon), float(p.lat))
                _shp.record(p.id, p.elevation, p.curve.head, p.curve.flow, None, "POWER {0}".format(str(1)))
            _shp.close()
        self.createProjection(filename)
