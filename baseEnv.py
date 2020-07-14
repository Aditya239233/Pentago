class HBDenv:

    # state must be initialised in child classes here
    def __init__(self):
        self.agents = []
        self.state = None
        raise NotImplementedError("Please initialise state here")

    # each bot's step function must be called here in child classes
    def gameStep(self):
        for agent in self.agents:
            action = agent.step(self.state)