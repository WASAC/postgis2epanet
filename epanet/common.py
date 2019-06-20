class Common(object):
    def __init__(self):
        pass

    def start(self, f, title):
        f.writelines("[TITLE]\n")
        f.writelines(title)
        f.writelines("\n")
        f.writelines("\n")

    def end(self, f):
        f.writelines("[END]")
        f.writelines("\n")
