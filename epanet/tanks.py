from epanet.coordinates import Coordinates


class Tanks(object):
    class Tank(object):
        def __init__(self, id, elevation, capacity, lon, lat):
            self.id = "Tank-" + str(id)
            self.elevation = elevation or 0
            self.capacity = capacity or 0
            self.lon = round(lon, 6)
            self.lat = round(lat, 6)
            self.diameter = 50
            self.min_vol = 0
            self.vol_curve = ""

        @staticmethod
        def create_header(f):
            f.writelines("[TANKS]\n")
            f.writelines(";{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n"
                         .format("ID\t".expandtabs(16),
                                 "Elevation\t".expandtabs(12),
                                 "InitLevel\t".expandtabs(12),
                                 "MinLevel\t".expandtabs(12),
                                 "MaxLevel\t".expandtabs(12),
                                 "Diameter\t".expandtabs(12),
                                 "MinVol\t".expandtabs(12),
                                 "VolCurve"
                                 ))

        def add(self, f):
            f.writelines(" {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t;\n"
                         .format("{0}\t".format(self.id).expandtabs(16),
                                 "{0}\t".format(str(self.elevation)).expandtabs(12),
                                 "{0}\t".format(str(self.capacity * 0.5)).expandtabs(12),
                                 "{0}\t".format(str(self.capacity * 0.1)).expandtabs(12),
                                 "{0}\t".format(str(self.capacity)).expandtabs(12),
                                 "{0}\t".format(str(self.diameter)).expandtabs(12),
                                 "{0}\t".format(str(self.min_vol)).expandtabs(12),
                                 "{0}\t".format(str(self.vol_curve)).expandtabs(16)
                                 ))

    def __init__(self, wss_id, coords):
        self.wss_id = wss_id
        self.coords = coords
        self.tanks = []
        self.epsg_utm = 32736

    def get_data(self, db):
        query = " SELECT reservoir_id as id, st_x(geom) as lon, st_y(geom) as lat, elevation, capacity,  "
        query += " st_x(st_transform(geom,{0})) as lon_utm, st_y(st_transform(geom,{0})) as lat_utm  "\
            .format(self.epsg_utm)
        query += "FROM reservoir WHERE wss_id={0} ".format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            id = data[0]
            lon = data[1]
            lat = data[2]
            elevation = data[3]
            capacity = data[4]
            lon_utm = data[5]
            lat_utm = data[6]
            t = Tanks.Tank(id, elevation, capacity, lon, lat)
            self.tanks.append(t)

            coord = Coordinates.Coordinate(t.id, t.lon, t.lat, t.elevation, lon_utm, lat_utm)
            self.coords.add_coordinate(coord)

    def export(self, f):
        Tanks.Tank.create_header(f)
        for t in self.tanks:
            t.add(f)
        f.writelines("\n")
