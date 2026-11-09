
class Land:
    def __init__(self):
        self.land = [
        "wall_red",
        "wall_red_edge",
        "wall_red_ll",
        "wall_red_lr",
        "wall_red_ur",
        "wall_red_ul"
        ]
        self.selection = 0
        self.brush = self.land[self.selection]
    def cycle(self):
        self.selection += 1
        self.selection %= len(self.land)
        self.brush = self.land[self.selection]