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

    def export_tags(self, f):
        tmp = "./templates/tags_template.inp"
        with open(tmp, 'r') as tmp:
            for line in tmp:
                f.writelines(line)
        f.writelines("\n")

    def export_options(self, f):
        tmp = "./templates/options_template.inp"
        with open(tmp, 'r') as tmp:
            for line in tmp:
                f.writelines(line)
        f.writelines("\n")
        f.writelines("\n")
