

class Feature:
    def __init__(self, data):
        self.type = data["type"]
        self.geometry = data["geometry"]
        self.properties = data["properties"]
        self.header = data["header"]
        self.messages = data["messages"]
        self.parameters = data["parameters"]
        self.times = data["times"]

        # Convert Parameters to Dictionary
        self.properties["parameter"]["PRECTOTCORR"] = dict(self.properties["parameter"]["PRECTOTCORR"])
