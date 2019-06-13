class Options(object):
    class Option(object):
        def __init__(self, key, val):
            self.key = key
            self.val = val

        @staticmethod
        def create_header(f):
            f.writelines("[OPTIONS]\n")

        def add(self, f):
            f.writelines("{0}{1}\n"
                         .format("{0}\t".format(self.key).expandtabs(20),
                                 "{0}\t".format(str(self.val)).expandtabs(15)
                                 ))

    def __init__(self):
        self.options = [
            Options.Option("Units", "LPS"),
            Options.Option("Headloss", "H-W"),
            Options.Option("Specific Gravity", "1"),
            Options.Option("Viscosity", "1"),
            Options.Option("Trials", "40"),
            Options.Option("Accuracy", "0.001"),
            Options.Option("CHECKFREQ", "2"),
            Options.Option("MAXCHECK", "10"),
            Options.Option("DAMPLIMIT", "0"),
            Options.Option("Unbalanced", "Continue 10"),
            Options.Option("Pattern", "0"),
            Options.Option("Demand Multiplier", "1.0"),
            Options.Option("Emitter Exponent", "0.5"),
            Options.Option("Quality", "None mg/L"),
            Options.Option("Diffusivity", "1"),
            Options.Option("Tolerance", "0.01")
        ]

    def export(self, f):
        Options.Option.create_header(f)
        for o in self.options:
            o.add(f)
        f.writelines("\n")
