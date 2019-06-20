class Options(object):
    def __init__(self):
        self.template = "./templates/template_d-w_lps.inp"

    def export(self, f):
        with open(self.template, 'r') as tmp:
            for line in tmp:
                f.writelines(line)
        f.writelines("\n")
        f.writelines("\n")
