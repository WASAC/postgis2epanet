import shutil


class LayerBase(object):
    def __init__(self):
        pass

    def createProjection(self, output_dir):
        shutil.copy("./templates/wgs84_4326.prj","{0}.prj".format(output_dir))
