from epanet.layer_base import LayerBase


class Valves(LayerBase):
    class Valve(object):
        def __init__(self, data):
            self.id = "{0}-{1}".format(data["valve_type"], str(data["id"]))
            self.lon = round(data["lon"], 6)
            self.lat = round(data["lat"], 6)
            self.diameter = float(data["diameter"] or 0.0)
            self.valve_type = data["valve_type"]
            self.setting = 0
            self.minor_loss = 0.0
            self.node1 = ""
            self.node2 = ""
            self.elevation = data["elevation"]

        def set_node(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

    def __init__(self, wss_id, coords, pipes, config):
        super().__init__("valves", wss_id, config)
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
        query = self.get_sql().format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            valve = Valves.Valve(data)
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