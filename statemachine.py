import json

class FSM:
    def __init__(self, definition: str):
        with open(definition, "r") as f:
            self.trans = json.load(f)
        self.curr = list(self.trans.keys())[0]
        print(f"Starting state {self.curr}")

    def next(self, inp: str):
        self.curr = self.trans[self.curr][inp]
        return self.curr



