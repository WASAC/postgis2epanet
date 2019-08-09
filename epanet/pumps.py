import shapefile


class Pumps(object):
    class Pump(object):
        def __init__(self, id, lon, lat, flow, head):
            self.id = "Pump-" + str(id)
            self.lon = round(lon, 6)
            self.lat = round(lat, 6)
            self.parameter = "Head " + str(id)
            self.curve = Pumps.PumpCurve(id, flow, head)
            self.node1 = ""
            self.node2 = ""

        def set_node(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

        @staticmethod
        def create_header(f):
            f.writelines("[PUMPS]\n")
            f.writelines(";{0}\t{1}\t{2}\t{3}\n"
                         .format("ID\t".expandtabs(16),
                                 "Node1\t".expandtabs(16),
                                 "Node2\t".expandtabs(16),
                                 "Parameters\t".expandtabs(12)
                                 ))

        def add(self, f):
            f.writelines(" {0}\t{1}\t{2}\t{3}\t;\n"
                         .format("{0}\t".format(self.id).expandtabs(16),
                                 "{0}\t".format(str(self.node1)).expandtabs(16),
                                 "{0}\t".format(str(self.node2)).expandtabs(16),
                                 "{0}\t".format(str(self.parameter)).expandtabs(12)
                                 ))

    class PumpCurve(object):
        def __init__(self, id, flow, head):
            self.id = id
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

    def get_data(self, db):
        query = " SELECT pumpingstation_id as id, st_x(geom) as lon, st_y(geom) as lat, head_pump, discharge_pump  "
        query += " FROM pumping_station WHERE wss_id={0} ".format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            id = data[0]
            lon = data[1]
            lat = data[2]
            head = data[3]
            discharge = data[4]
            pump = Pumps.Pump(id, lon, lat, discharge, head)
            self.pumps.append(pump)

            target_key = ",".join([str(pump.lon), str(pump.lat)])
            if target_key in self.coords.coordMap and self.coords.coordMap[target_key]:
                coord = self.coords.coordMap[target_key]
                nodeid = coord.id
                del_pipe_idx = -1
                for p in self.pipes:
                    if nodeid == p.node1 or nodeid == p.node2:
                        pump.set_node(p.node1, p.node2)
                        del_pipe_idx = self.pipes.index(p)
                if del_pipe_idx > -1:
                    del self.pipes[del_pipe_idx]

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
        with shapefile.Writer("{0}/{1}_{2}".format(f.name.replace(".inp", ""), self.wss_id, "pumps")) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('node1', 'C', 254)
            _shp.field('node2', 'C', 254)
            _shp.field('head', 'C', 254)
            _shp.field('flow', 'C', 254)
            _shp.field('power', 'N', 20, 9)
            _shp.field('curveID', 'C', 254)
            for p in self.pumps:
                node1 = self.coords.get_coord_by_id(p.node1)
                node2 = self.coords.get_coord_by_id(p.node2)
                _shp.line([[[float(node1.lon), float(node1.lat)], [float(node2.lon), float(node2.lat)]]])
                _shp.record(p.id, p.node1, p.node2, p.curve.head, p.curve.flow, None, p.curve.id)
            _shp.close()
