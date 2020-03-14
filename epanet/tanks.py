from epanet.coordinates import Coordinates
import shapefile
from epanet.layer_base import LayerBase


class Tanks(LayerBase):
    class Tank(object):
        def __init__(self, data):
            self.id = data["id"]
            self.elevation = data["elevation"] or 0
            self.capacity = data["capacity"] or 0
            if "max_level" in data:
                self.max_level = data["max_level"]
            else:
                self.max_level = 1.5

            if "init_level" in data:
                self.init_level = data["init_level"]
            else:
                self.init_level = self.max_level * 0.5

            if "min_level" in data:
                self.min_level = data["min_level"]
            else:
                self.min_level = self.max_level * 0.1

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

    def export_shapefile(self, f):
        if len(self.tanks) == 0:
            return
        filename = self.get_file_path(f)
        with shapefile.Writer(filename) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'N', 20)
            _shp.field('initiallev', 'N', 20)
            _shp.field('minimumlev', 'N', 20)
            _shp.field('maximumlev', 'N', 20)
            _shp.field('diameter', 'N', 20)
            _shp.field('minimumvol', 'N', 20)
            _shp.field('volumecurv', 'N', 20)
            for t in self.tanks:
                _shp.point(float(t.lon), float(t.lat))
                _shp.record(t.id, t.elevation, t.init_level, t.min_level, t.max_level,
                            t.diameter, t.min_vol, t.vol_curve)
            _shp.close()
        self.createProjection(filename)
