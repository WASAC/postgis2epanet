from epanet.coordinates import Coordinates


class Tanks(object):
    class Tank(object):
        def __init__(self, id, elevation, capacity, lon, lat):
            self.id = "Tank-" + str(id)
            self.elevation = elevation or 0
            self.capacity = capacity or 0
            self.lon = round(lon, 6)
            self.lat = round(lat, 6)

        @staticmethod
        def create_header(f):
            f.writelines("[TANKS]\n")
            f.writelines(";{0}{1}{2}{3}{4}\n"
                         .format("ID\t".expandtabs(20),
                                 "Elevation\t".expandtabs(10),
                                 "InitLevel\t".expandtabs(10),
                                 "MinLevel\t".expandtabs(10),
                                 "MaxLevel\t".expandtabs(10)
                                 ))

        def add(self, f):
            f.writelines("{0}{1}{2}{3}{4}\n"
                         .format("{0}\t".format(self.id).expandtabs(20),
                                 "{0}\t".format(str(self.elevation)).expandtabs(10),
                                 "{0}\t".format(str(self.capacity * 0.5)).expandtabs(10),
                                 "{0}\t".format(str(self.capacity * 0.1)).expandtabs(10),
                                 "{0}\t".format(str(self.capacity)).expandtabs(10)
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
