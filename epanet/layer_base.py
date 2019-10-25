import shutil


class LayerBase(object):
    def __init__(self, layer, wss_id):
        self.layer = layer
        self.wss_id = wss_id
        self.epsg = 4326
        self.epsg_utm = 32736

    def createProjection(self, output_dir):
        shutil.copy("./templates/wgs84_4326.prj","{0}.prj".format(output_dir))

    def get_file_path(self, f):
        return "{0}/{1}".format(f.name.replace(".inp", ""), self.layer)