
import re, datetime
class Data:
    def __init__(self, data):
        self.type = data["type"]
        self.geometry = data["geometry"]
        self.properties = data["properties"]
        self.header = data["header"]
        self.messages = data["messages"]
        self.parameters = Parameter()
        #self.parameters.JSON = data["parameters"]
        self.times = data["times"]

        # Convert Parameters to Dictionary
        if "PRECTOTCORR" in self.properties["parameter"]:
            self.parameters.PRECTOTCORR = dict(self.properties["parameter"]["PRECTOTCORR"])
            # for i in self.parameters.PRECTOTCORR.keys():
            #     self.parameters.JSON
        #Relative Humidity at 2 Meters
        if "RH2M" in self.properties["parameter"]:
            self.parameters.RH2M = dict(self.properties["parameter"]["RH2M"])
        #Specific Humidity at 2 Meters
        if "QV2M" in self.properties["parameter"]:
            self.parameters.QV2M = dict(self.properties["parameter"]["QV2M"])
        #Temperature at 2 Meters
        if "T2M" in self.properties["parameter"]:
            self.parameters.T2M = dict(self.properties["parameter"]["T2M"])
        if "WS2M" in self.properties["parameter"]:
            self.parameters.WS2M = dict(self.properties["parameter"]["WS2M"])
        
    def get_formated_dict(self) -> list:
        data = dict(vars(self.parameters))
        dictionary = []
        for parameter in data.keys(): 
            chaves = list(data.keys())
            if parameter in data:
                for date in data[parameter].keys():
                    if parameter == chaves[0]:
                        dictionary.append({"date":date, parameter:data[parameter][date]})
                    else:
                        data_list = list(data[parameter].keys())
                        index = data_list.index(date)
                        dictionary[index][parameter] = data[parameter][date]
                    
        return dictionary
        
            
class Parameter():
    def __init__(self, PRECTOTCORR=None ,RH2M=None ,QV2M=None ,T2M=None ,WS2M=None):
        self.PRECTOTCORR = PRECTOTCORR
        self.RH2M = RH2M
        self.QV2M = QV2M
        self.T2M = T2M
        self.WS2M = WS2M
        # self.POSITION = []
    
         