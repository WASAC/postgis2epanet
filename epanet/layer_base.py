import shutil


class LayerBase(object):
    def __init__(self, layer, wss_id, config):
        self.layer = layer
        self.wss_id = wss_id
        self.epsg = config["epsg"]
        self.epsg_utm = config["epsg_utm"]
        self.config = config

    def get_sql(self):
        sql = ""
        if self.config[self.layer]:
            sql = "".join(self.config[self.layer]["sql"])
            sql = sql.replace("%epsg%", str(self.epsg)).replace("%epsg_utm%", str(self.epsg_utm))
        return sql

    def get_file_path(self, f):
        return "{0}/{1}".format(f.name.replace(".inp", ""), self.layer)