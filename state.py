
# For now the class still uses the old attributes. Change later, when the new attributes (nxn array) are implemented.
class State:
    def __init__(self, position, electrode1_pos, electrode2_pos, agent_area):
        self.position = position
        self.electrode1_pos = electrode1_pos
        self.electrode2_pos = electrode2_pos
        self.agent_area = agent_area

    def __hash__(self):
        return hash((self.position, self.electrode1_pos, self.electrode2_pos, tuple(map(tuple, self.agent_area))))

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.position, self.electrode1_pos, self.electrode2_pos, tuple(map(tuple, self.agent_area))) == (other.position, other.electrode1_pos, other.electrode2_pos, tuple(map(tuple, other.agent_area)))
