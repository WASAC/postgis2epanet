from epanet.coordinates import Coordinates
from epanet.layer_base import LayerBase


class Reservoirs(LayerBase):
    class Reservoir(object):
        def __init__(self, data):
            # self.id = "{0}-{1}".format(data["source_type"], str(data["id"])).replace(" ", "-")
            self.id = data["id"]
            self.elevation = data["elevation"] or 0
            self.pattern = ""
            self.lon = round(data["lon"], 6)
            self.lat = round(data["lat"], 6)

    def __init__(self, wss_id, coords, config):
        super().__init__("reservoirs", wss_id, config)
        self.coords = coords
        self.reservoirs = []

    def get_data(self, db):
        query = self.get_sql().format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            r = Reservoirs.Reservoir(data)
            self.reservoirs.append(r)
            coord = Coordinates.Coordinate(data)
            self.coords.add_coordinate(coord)