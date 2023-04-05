class State:
    def __init__(self, position, angle, electrode1_pos, electrode2_pos, electrode1_area, electrode2_area):
        self.position = position
        self.angle = angle
        self.electrode1_pos = electrode1_pos
        self.electrode2_pos = electrode2_pos
        self.electrode1_area = electrode1_area
        self.electrode2_area = electrode2_area

    def is_equal(self, other):
        if not isinstance(other, State):
            return False

        return (self.position == other.position
                and self.angle == other.angle
                and self.electrode1_pos == other.electrode1_pos
                and self.electrode2_pos == other.electrode2_pos
                and self.electrode1_area == other.electrode1_area
                and self.electrode2_area == other.electrode2_area)
