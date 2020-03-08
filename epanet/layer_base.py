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

    def createProjection(self, output_dir):
        shutil.copy("./templates/wgs84_4326.prj","{0}.prj".format(output_dir))

    def get_file_path(self, f):
        return "{0}/{1}".format(f.name.replace(".inp", ""), self.layer)

    def updatePipeNode(self, obj):
        '''
        To update pipe node which intersects valve or pump node.
        :param obj: valve object or pump object shall be here
        :return:
        '''
        target_key = ",".join([str(obj.lon), str(obj.lat)])
        if target_key in self.coords.coordMap and self.coords.coordMap[target_key]:
            coord = self.coords.coordMap[target_key]
            nodeid = coord.id
            for pipe in self.pipes:
                if nodeid == pipe.node1:
                    pipe.set_node(obj.id, pipe.node2)
                    coord.id = obj.id
                elif nodeid == pipe.node2:
                    pipe.set_node(pipe.node1, obj.id)
                    coord.id = obj.id