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
            f.writelines(";{0}{1}{2}{3}\n"
                         .format("ID\t".expandtabs(20),
                                 "Node1\t".expandtabs(15),
                                 "Node2\t".expandtabs(15),
                                 "Parameters\t".expandtabs(10)
                                 ))

        def add(self, f):
            f.writelines("{0}{1}{2}{3}\n"
                         .format("{0}\t".format(self.id).expandtabs(20),
                                 "{0}\t".format(str(self.node1)).expandtabs(15),
                                 "{0}\t".format(str(self.node2)).expandtabs(15),
                                 "{0}\t".format(str(self.parameter)).expandtabs(10)
                                 ))

    class PumpCurve(object):
        def __init__(self, id, flow, head):
            self.id = id
            self.flow = flow
            self.head = head

        @staticmethod
        def create_header(f):
            f.writelines("[CURVES]\n")
            f.writelines(";{0}{1}{2}\n"
                         .format("ID\t".expandtabs(20),
                                 "X-Value\t".expandtabs(15),
                                 "Y-Value\t".expandtabs(15)
                                 ))

        def add(self, f):
            f.writelines("{0}{1}{2}\n"
                         .format("{0}\t".format(self.id).expandtabs(20),
                                 "{0}\t".format(str(self.flow)).expandtabs(15),
                                 "{0}\t".format(str(self.head)).expandtabs(15)
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

        Pumps.PumpCurve.create_header(f)
        for p in self.pumps:
            p.curve.add(f)
        f.writelines("\n")
