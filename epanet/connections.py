from epanet.layer_base import LayerBase


class Connections(LayerBase):
    class Connection(object):
        def __init__(self, data):
            self.id = data["id"]
            self.type = data["type"]
            self.lon = round(data["lon"], 6)
            self.lat = round(data["lat"], 6)
            self.no_user = data["no_user"]
            self.demands = round(data["demands"], 9)

    def __init__(self, wss_id, config):
        super().__init__("connections", wss_id, config)
        self.connections = []

    def get_data(self, db):
        query = self.get_sql().format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            c = Connections.Connection(data)
            self.connections.append(c)
