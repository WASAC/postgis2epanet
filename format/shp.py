from abc import ABCMeta
from abc import abstractmethod
import shutil
import shapefile


class Shp(metaclass = ABCMeta):
    def __init__(self, file, array):
        self.file = file
        self.array = array

    def createProjection(self, output_dir):
        shutil.copy("./templates/wgs84_4326.prj", "{0}.prj".format(output_dir))

    @abstractmethod
    def export(self):
        pass


class ShpCoordinates(Shp):
    def __init__(self, file, array, del_coords_id):
        super().__init__(file, array)
        self.del_coords_id = del_coords_id

    def export(self):
        if len(self.array) == 0:
            return
        with shapefile.Writer(self.file) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'N', 20)
            _shp.field('pattern', 'C', 254)
            _shp.field('demand', 'N', 20, 9)
            _shp.field('demand_pto', 'N', 20, 9)
            for key in self.array:
                coord = self.array[key]
                if "Node" in coord.id:
                    if coord.id in self.del_coords_id:
                        continue
                    _shp.point(float(coord.lon), float(coord.lat))
                    _shp.record(coord.id, coord.elevation, coord.pattern, coord.demand, '')
            _shp.close()
        self.createProjection(self.file)


class ShpPipes(Shp):
    def __init__(self, file, array, coords):
        super().__init__(file, array)
        self.coords = coords

    def export(self):
        if len(self.array) == 0:
            return
        with shapefile.Writer(self.file) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('node1', 'C', 254)
            _shp.field('node2', 'C', 254)
            _shp.field('length', 'N', 20, 9)
            _shp.field('diameter', 'N', 20, 9)
            _shp.field('status', 'C', 254)
            _shp.field('roughness', 'N', 20, 9)
            _shp.field('minorloss', 'N', 20, 9)
            for data in self.array:
                node1 = self.coords.get_coord_by_id(data.node1)
                node2 = self.coords.get_coord_by_id(data.node2)
                _shp.line([[[float(node1.lon), float(node1.lat)], [float(node2.lon), float(node2.lat)]]])
                _shp.record(data.id, data.node1, data.node2, data.length, data.diameter, data.status, data.roughness,
                            data.minorloss)
            _shp.close()
        self.createProjection(self.file)


class ShpPumps(Shp):
    def __init__(self, file, array, pipes):
        super().__init__(file, array)
        self.pipes = pipes

    def export(self):
        if len(self.array) == 0:
            return
        with shapefile.Writer(self.file) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'C', 254)
            _shp.field('head', 'C', 254)
            _shp.field('flow', 'C', 254)
            _shp.field('power', 'N', 20, 9)
            _shp.field('properties', 'C', 254)
            for data in self.array:
                _shp.point(float(data.lon), float(data.lat))
                _shp.record(data.id, data.elevation, data.curve.head, data.curve.flow, None, "POWER {0}".format(str(1)))
                self.pipes.updatePipeNode(data)
            _shp.close()
        self.createProjection(self.file)


class ShpTanks(Shp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def export(self):
        if len(self.array) == 0:
            return
        with shapefile.Writer(self.file) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'N', 20)
            _shp.field('initiallev', 'N', 20)
            _shp.field('minimumlev', 'N', 20)
            _shp.field('maximumlev', 'N', 20)
            _shp.field('diameter', 'N', 20)
            _shp.field('minimumvol', 'N', 20)
            _shp.field('volumecurv', 'N', 20)
            for data in self.array:
                _shp.point(float(data.lon), float(data.lat))
                _shp.record(data.id, data.elevation, data.init_level, data.min_level, data.max_level,
                            data.diameter, data.min_vol, data.vol_curve)
            _shp.close()
        self.createProjection(self.file)


class ShpReservoirs(Shp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def export(self):
        if len(self.array) == 0:
            return
        with shapefile.Writer(self.file) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('head', 'N', 20)
            _shp.field('pattern', 'C', 254)
            for data in self.array:
                _shp.point(float(data.lon), float(data.lat))
                _shp.record(data.id, data.elevation, '')
            _shp.close()
        self.createProjection(self.file)


class ShpValves(Shp):
    def __init__(self, file, array, pipes):
        super().__init__(file, array)
        self.pipes = pipes

    def export(self):
        if len(self.array) == 0:
            return
        with shapefile.Writer(self.file) as _shp:
            _shp.autoBalance = 1
            _shp.field('dc_id', 'C', 254)
            _shp.field('elevation', 'C', 254)
            _shp.field('diameter', 'N', 20, 9)
            _shp.field('type', 'C', 254)
            _shp.field('setting', 'C', 254)
            _shp.field('minorloss', 'N', 20, 9)
            for data in self.array:
                _shp.point(float(data.lon), float(data.lat))
                _shp.record(data.id, data.elevation, data.diameter, data.valve_type, data.setting, data.minor_loss)
                self.pipes.updatePipeNode(data)
            _shp.close()
        self.createProjection(self.file)