class WaterSupplySystems(object):
    class Wss(object):
        def __init__(self, params):
            self.wss_id = params["wss_id"]
            self.wss_name = params["wss_name"]
            self.dist_id = params["dist_id"]
            self.wss_type = params["wss_type"]
            self.status = params["status"]

    def __init__(self, config):
        self.config = config

    def get_wss_list(self, db):
        query = "".join(self.config["prepare"]["wss"])
        result = db.execute(query)
        wss_list = {}
        for data in result:
            obj = WaterSupplySystems.Wss(data)
            obj.wss_name = obj.wss_name.replace(" ", "").replace("/", "").replace("\n", "")
            wss_list[str(obj.wss_id)] = obj
        return wss_list
