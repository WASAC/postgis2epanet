class WaterSupplySystems(object):
    class Wss(object):
        def __init__(self, params):
            self.wss_id = params[0]
            self.wss_name = params[1]
            self.dist_id = params[2]
            self.wss_type = params[3]
            self.status = params[4]

    def __init__(self):
        pass

    def update_elevations(self, db):
        query = "update chamber set elevation = ST_Value(e.rast, 1, chamber.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, chamber.geom);" \
                "update pumping_station set elevation = ST_Value(e.rast, 1, pumping_station.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, pumping_station.geom);" \
                "update reservoir set elevation = ST_Value(e.rast, 1, reservoir.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, reservoir.geom);" \
                "update water_connection set elevation = ST_Value(e.rast, 1, water_connection.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, water_connection.geom);" \
                "update watersource set elevation = ST_Value(e.rast, 1, watersource.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, watersource.geom);" \
                "update wtp set elevation = ST_Value(e.rast, 1, wtp.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, wtp.geom);" \
                "update valve set elevation = ST_Value(e.rast, 1, valve.geom) FROM rwanda_dem_10m e where ST_Intersects(e.rast, valve.geom);"
        db.update(query)

    def get_wss_list(self, db):
        query = "SELECT wss_id, wss_name, dist_id, wss_type, status FROM wss"
        result = db.execute(query)
        wss_list = {}
        for data in result:
            obj = WaterSupplySystems.Wss(data)
            obj.wss_name = obj.wss_name.replace(" ", "").replace("/", "").replace("\n", "")
            wss_list[str(obj.wss_id)] = obj
        return wss_list
