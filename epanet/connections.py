class Connections(object):
    class Connection(object):
        def __init__(self, id, type, lon, lat, no_user, demands):
            self.id = id
            self.type = type
            self.lon = round(lon, 6)
            self.lat = round(lat, 6)
            self.no_user = no_user
            self.demands = round(demands, 9)

    def __init__(self, wss_id):
        self.wss_id = wss_id
        self.connections = []

    def get_data(self, db):
        query = " select connection_id, connection_type, st_x(geom) as lon, st_y(geom) as lat, " \
                "no_user, COALESCE(cast(no_user as float)*40/86400,0.0) as demands " \
                "from water_connection WHERE wss_id={0} ".format(str(self.wss_id))

        result = db.execute(query)
        for data in result:
            id = data[0]
            conn_type = data[1]
            lon = data[2]
            lat = data[3]
            no_user = data[4]
            demands = data[5]
            c = Connections.Connection(id, conn_type, lon, lat, no_user, demands)
            self.connections.append(c)
