
class Land:
    def __init__(self):
        self.land = [
        "wall",
        "wall_edge",
        "wall_ll",
        "wall_lr",
        "wall_ur",
        "wall_ul"
        ]
        self.colors = [
            "red",
            "green"
        ]
        self.selection = 0
        self.color_selection = 0
        self.color = "red"
        self.brush = self.land[self.selection]+"_"+self.color+".gif"
    def cycle_color(self):
        self.color_selection += 1
        self.color_selection %= len(self.colors)
        self.color = self.colors[self.color_selection]
        self.brush = self.land[self.selection] + "_" + self.color + ".gif"
    def cycle(self):
        self.selection += 1
        self.selection %= len(self.land)
        self.brush = self.land[self.selection]+"_"+self.color+".gif"