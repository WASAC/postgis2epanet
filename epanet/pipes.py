import json
from shapely.geometry import LineString
import shapefile
from epanet.layer_base import LayerBase


class Pipes(LayerBase):
    class Pipe(object):
        def __init__(self, id, node1, node2, length, diameter):
            self.id = "Pipe-" + id
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

        @staticmethod
        def create_header(f):
            f.writelines("[PIPES]\n")
            f.writelines(";{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n"
                         .format("ID\t".expandtabs(20),
                                 "Node1\t".expandtabs(20),
                                 "Node2\t".expandtabs(20),
                                 "Length\t".expandtabs(12),
                                 "Diameter\t".expandtabs(12),
                                 "Roughness\t".expandtabs(12),
                                 "MinorLoss\t".expandtabs(12),
                                 "Status"
                                 ))

        def add(self, f):
            f.writelines(" {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t;\n"
                         .format("{0}\t".format(self.id).expandtabs(20),
                                 "{0}\t".format(str(self.node1)).expandtabs(20),
                                 "{0}\t".format(str(self.node2)).expandtabs(20),
                                 "{0}\t".format(str(self.length)).expandtabs(12),
                                 "{0}\t".format(str(self.diameter)).expandtabs(12),
                                 "{0}\t".format(str(self.roughness)).expandtabs(12),
                                 "{0}\t".format(str(self.minorloss)).expandtabs(12),
                                 "{0}\t".format(self.status).expandtabs(6)
                                 ))

    def __init__(self, wss_id, coords, config):
        super().__init__("pipes", wss_id, config)
        self.coords = coords
        self.pipes = []

    def get_data(self, db):
        query = " SELECT pipe_id, pipe_size, ST_AsGeoJSON(st_multi(geom)) as geojson " \
                "FROM pipeline WHERE wss_id={0} ".format(str(self.wss_id))
        result = db.execute(query)
        for data in result:
            pipe_id = data[0]
            pipe_size = data[1]
            geojson = json.loads(data[2])
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

    def export(self, f, del_pipes_id):
        Pipes.Pipe.create_header(f)
        for pipe in self.pipes:
            if not pipe.id in del_pipes_id:
                pipe.add(f)
        f.writelines("\n")

    def export_shapefile(self, f):
        if len(self.pipes) == 0:
            return
        filename = self.get_file_path(f)
        with shapefile.Writer(filename) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('node1', 'C', 254)
            _shp.field('node2', 'C', 254)
            _shp.field('length', 'N', 20, 9)
            _shp.field('diameter', 'N', 20, 9)
            _shp.field('status', 'C', 254)
            _shp.field('roughness', 'N', 20, 9)
            _shp.field('minorloss', 'N', 20, 9)
            for pipe in self.pipes:
                node1 = self.coords.get_coord_by_id(pipe.node1)
                node2 = self.coords.get_coord_by_id(pipe.node2)
                _shp.line([[[float(node1.lon), float(node1.lat)], [float(node2.lon), float(node2.lat)]]])
                _shp.record(pipe.id, pipe.node1, pipe.node2, pipe.length, pipe.diameter, pipe.status, pipe.roughness, pipe.minorloss)
            _shp.close()
        self.createProjection(filename)
