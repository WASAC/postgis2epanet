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

    def get_wss_list(self, db):
        query = "SELECT wss_id, wss_name, dist_id, wss_type, status FROM wss"
        result = db.execute(query)
        wss_list = {}
        for data in result:
            obj = WaterSupplySystems.Wss(data)
            obj.wss_name = obj.wss_name.replace(" ", "").replace("/", "").replace("\n", "")
            wss_list[str(obj.wss_id)] = obj
        return wss_list
