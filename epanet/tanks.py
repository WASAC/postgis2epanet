from epanet.coordinates import Coordinates
from epanet.layer_base import LayerBase


class Tanks(LayerBase):
    class Tank(object):
        def __init__(self, data):
            self.id = data["id"]
            self.elevation = data["elevation"] or 0
            self.capacity = data["capacity"] or 0
            self.max_level = data["max_level"] or 1.5
            self.init_level = data["init_level"] or 0.75
            self.min_level = data["min_level"] or 0.15
            self.lon = round(data["lon"], 6)
            self.lat = round(data["lat"], 6)
            self.diameter = 5
            self.min_vol = self.capacity
            self.vol_curve = ""

    def __init__(self, wss_id, coords, config):
        super().__init__("tanks", wss_id, config)
        self.coords = coords
        self.tanks = []

    def get_data(self, db):
        query = self.get_sql().format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            t = Tanks.Tank(data)
            self.tanks.append(t)
            coord = Coordinates.Coordinate(data)
            self.coords.add_coordinate(coord)