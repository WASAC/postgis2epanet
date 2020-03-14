from abc import ABCMeta
from abc import abstractmethod


class Inp(metaclass = ABCMeta):
    def __init__(self, file, array):
        self.file = file
        self.array = array

    @abstractmethod
    def create_header(self):
        pass

    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def export(self):
        pass


class InpJunctions(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[JUNCTIONS]\n")
        self.file.writelines(";{0}\t{1}\t{2}\t{3}\n"
             .format("ID\t".expandtabs(20),
                     "Elev\t".expandtabs(12),
                     "Demand\t".expandtabs(12),
                     "Pattern\t".expandtabs(16)))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t{3}\t;\n"
                     .format("{0}\t".format(data.id).expandtabs(20),
                             "{0}\t".format(data.elevation).expandtabs(12),
                             "{0}\t".format(data.demand).expandtabs(12),
                             "{0}\t".format(data.pattern).expandtabs(16)))

    def export(self):
        self.create_header()
        for key in self.array:
            data = self.array[key]
            if "Node" in data.id:
                self.add(data)
        self.file.writelines("\n")


class InpCoordinates(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[COORDINATES]\n")
        self.file.writelines(";{0}\t{1}\t{2}\n"
             .format("Node\t".expandtabs(20),
                     "X-Coord\t".expandtabs(16),
                     "Y-Coord\t".expandtabs(16)))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\n"
             .format("{0}\t".format(data.id).expandtabs(20),
                     "{0}\t".format(data.lon).expandtabs(16),
                     "{0}\t".format(data.lat).expandtabs(16)))

    def export(self):
        self.create_header()
        for key in self.array:
            data = self.array[key]
            self.add(data)
        self.file.writelines("\n")


class InpPipes(Inp):
    def __init__(self, file, array, del_pipes_id):
        super().__init__(file, array)
        self.del_pipes_id = del_pipes_id

    def create_header(self):
        self.file.writelines("[PIPES]\n")
        self.file.writelines(";{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n"
                     .format("ID\t".expandtabs(20),
                             "Node1\t".expandtabs(20),
                             "Node2\t".expandtabs(20),
                             "Length\t".expandtabs(12),
                             "Diameter\t".expandtabs(12),
                             "Roughness\t".expandtabs(12),
                             "MinorLoss\t".expandtabs(12),
                             "Status"
                             ))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t;\n"
            .format("{0}\t".format(data.id).expandtabs(20),
                    "{0}\t".format(str(data.node1)).expandtabs(20),
                    "{0}\t".format(str(data.node2)).expandtabs(20),
                    "{0}\t".format(str(data.length)).expandtabs(12),
                    "{0}\t".format(str(data.diameter)).expandtabs(12),
                    "{0}\t".format(str(data.roughness)).expandtabs(12),
                    "{0}\t".format(str(data.minorloss)).expandtabs(12),
                    "{0}\t".format(data.status).expandtabs(6)
                    ))

    def export(self):
        self.create_header()
        for data in self.array:
            if self.del_pipes_id and (data.id in self.del_pipes_id):
                continue
            self.add(data)
        self.file.writelines("\n")


class InpPumps(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[PUMPS]\n")
        self.file.writelines(";{0}\t{1}\t{2}\t{3}\n"
             .format("ID\t".expandtabs(20),
                     "Node1\t".expandtabs(20),
                     "Node2\t".expandtabs(20),
                     "Parameters\t".expandtabs(12)
                     ))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t{3}\t;\n"
             .format("{0}\t".format(data.id).expandtabs(20),
                     "{0}\t".format(str(data.node1)).expandtabs(20),
                     "{0}\t".format(str(data.node2)).expandtabs(20),
                     "{0}\t".format(str(data.parameter)).expandtabs(12)
                     ))

    def export(self):
        self.create_header()
        for data in self.array:
            self.add(data)
        self.file.writelines("\n")


class InpCurve(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[CURVES]\n")
        self.file.writelines(";{0}\t{1}\t{2}\n"
             .format("ID\t".expandtabs(16),
                     "X-Value\t".expandtabs(12),
                     "Y-Value\t".expandtabs(12)
                     ))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t;\n"
             .format("{0}\t".format(data.id).expandtabs(16),
                     "{0}\t".format(str(data.flow)).expandtabs(12),
                     "{0}\t".format(str(data.head)).expandtabs(12)
                     ))

    def export(self):
        self.create_header()
        for data in self.array:
            self.add(data.curve)
        self.file.writelines("\n")


class InpReservoirs(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[RESERVOIRS]\n")
        self.file.writelines(";{0}\t{1}\t{2}\n"
             .format("ID\t".expandtabs(20),
                     "Head\t".expandtabs(12),
                     "Pattern\t".expandtabs(16)
                     ))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t;\n"
             .format("{0}\t".format(data.id).expandtabs(20),
                     "{0}\t".format(str(data.elevation)).expandtabs(12),
                     "{0}\t".format(str(data.pattern)).expandtabs(16)
                     ))

    def export(self):
        self.create_header()
        for data in self.array:
            self.add(data)
        self.file.writelines("\n")


class InpTanks(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[TANKS]\n")
        self.file.writelines(";{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n"
             .format("ID\t".expandtabs(20),
                     "Elevation\t".expandtabs(12),
                     "InitLevel\t".expandtabs(12),
                     "MinLevel\t".expandtabs(12),
                     "MaxLevel\t".expandtabs(12),
                     "Diameter\t".expandtabs(12),
                     "MinVol\t".expandtabs(12),
                     "VolCurve"
                     ))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t;\n"
             .format("{0}\t".format(data.id).expandtabs(20),
                     "{0}\t".format(str(data.elevation)).expandtabs(12),
                     "{0}\t".format(str(data.init_level)).expandtabs(12),
                     "{0}\t".format(str(data.min_level)).expandtabs(12),
                     "{0}\t".format(str(data.max_level)).expandtabs(12),
                     "{0}\t".format(str(data.diameter)).expandtabs(12),
                     "{0}\t".format(str(data.min_vol)).expandtabs(12),
                     "{0}\t".format(str(data.vol_curve)).expandtabs(16)
                     ))

    def export(self):
        self.create_header()
        for data in self.array:
            self.add(data)
        self.file.writelines("\n")


class InpValves(Inp):
    def __init__(self, file, array):
        super().__init__(file, array)

    def create_header(self):
        self.file.writelines("[VALVES]\n")
        self.file.writelines(";{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n"
             .format("ID\t".expandtabs(20),
                     "Node1\t".expandtabs(16),
                     "Node2\t".expandtabs(16),
                     "Diameter\t".expandtabs(12),
                     "Type\t".expandtabs(12),
                     "Setting\t".expandtabs(12),
                     "MinorLoss\t".expandtabs(12),
                     ))

    def add(self, data):
        self.file.writelines(" {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t;\n"
             .format("{0}\t".format(data.id).expandtabs(20),
                     "{0}\t".format(str(data.node1)).expandtabs(20),
                     "{0}\t".format(str(data.node2)).expandtabs(20),
                     "{0}\t".format(str(data.diameter)).expandtabs(12),
                     "{0}\t".format(str(data.valve_type)).expandtabs(12),
                     "{0}\t".format(str(data.setting)).expandtabs(12),
                     "{0}\t".format(str(data.minor_loss)).expandtabs(12)
                     ))

    def export(self):
        self.create_header()
        for data in self.array:
            self.add(data)
        self.file.writelines("\n")


class InpTitle(object):
    def __init__(self, file, title):
        self.file = file
        self.title = title

    def export(self):
        self.file.writelines("[TITLE]\n")
        self.file.writelines(self.title)
        self.file.writelines("\n")
        self.file.writelines("\n")


class InpEnd(object):
    def __init__(self, file):
        self.file = file

    def export(self):
        self.file.writelines("[END]")
        self.file.writelines("\n")


class InpTags(object):
    def __init__(self, file):
        self.file = file

    def export(self):
        tmp = "./templates/tags_template.inp"
        with open(tmp, 'r') as tmp:
            for line in tmp:
                self.file.writelines(line)
        self.file.writelines("\n")


class InpOptions(object):
    def __init__(self, file):
        self.file = file

    def export(self):
        tmp = "./templates/options_template.inp"
        with open(tmp, 'r') as tmp:
            for line in tmp:
                self.file.writelines(line)
        self.file.writelines("\n")