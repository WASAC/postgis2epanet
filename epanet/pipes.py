import json
from shapely.geometry import LineString
from epanet.layer_base import LayerBase


class Pipes(LayerBase):
    class Pipe(object):
        def __init__(self, id, node1, node2, length, diameter):
            self.id = id
            self.node1 = node1
            self.node2 = node2
            self.length = round(length, 3)
            self.diameter = diameter or 0
            self.roughness = 100
            self.minorloss = 0
            self.status = "Open"

        def set_node(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

    def __init__(self, wss_id, coords, config):
        super().__init__("pipes", wss_id, config)
        self.coords = coords
        self.pipes = []

    def get_data(self, db):
        query = self.get_sql().format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            pipe_id = data["id"]
            pipe_size = data["diameter"]
            geojson = json.loads(data["geojson"])
            coordinates = geojson['coordinates'][0]
            for i in range(0, len(coordinates) - 1):

                x1 = round(coordinates[i][0], 6)
                y1 = round(coordinates[i][1], 6)
                key1 = ",".join([str(x1), str(y1)])
                if key1 in self.coords.coordMap and self.coords.coordMap[key1]:
                    coord1 = self.coords.coordMap[key1]
                    j = i + 1
                    x2 = round(coordinates[j][0], 6)
                    y2 = round(coordinates[j][1], 6)
                    key2 = ",".join([str(x2), str(y2)])

                    if key1 != key2 and key2 in self.coords.coordMap and self.coords.coordMap[key2]:
                        coord2 = self.coords.coordMap[key2]
                        node1 = coord1.id
                        node2 = coord2.id

                        xy_list = [[coord1.lon_utm, coord1.lat_utm], [coord2.lon_utm, coord2.lat_utm]]
                        line = LineString(xy_list)

                        length = line.length
                        _id = "{0}-{1}".format(pipe_id, i)
                        pipe = Pipes.Pipe(_id, node1, node2, length, pipe_size)
                        self.pipes.append(pipe)

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