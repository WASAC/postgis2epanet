from epanet.coordinates import Coordinates
import shapefile
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

    def export_shapefile(self, f):
        if len(self.reservoirs) == 0:
            return
        filename = self.get_file_path(f)
        with shapefile.Writer(filename) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('head', 'N', 20)
            _shp.field('pattern', 'C', 254)
            for r in self.reservoirs:
                _shp.point(float(r.lon), float(r.lat))
                _shp.record(r.id, r.elevation, '')
            _shp.close()
        self.createProjection(filename)
