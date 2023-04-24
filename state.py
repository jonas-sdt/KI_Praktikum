class State:
    def __init__(self, position, electrode1_pos, electrode2_pos, agent_area):
        self.position = position
        self.electrode1_pos = electrode1_pos
        self.electrode2_pos = electrode2_pos
        self.agent_area = agent_area

    def is_equal(self, other):
        if not isinstance(other, State):
            return False

        print("Length of agent area: ", len(self.agent_area))
        print("Length of other agent area: ", len(other.agent_area))

        return (self.position == other.position
                and self.electrode1_pos == other.electrode1_pos
                and self.electrode2_pos == other.electrode2_pos
                and self.agent_area == other.agent_area)
