
import re, datetime
class Data:
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
        
        #Relative Humidity at 2 Meters
        self.properties["parameter"]["RH2M"] = dict(self.properties["parameter"]["RH2M"])
        #Specific Humidity at 2 Meters
        self.properties["parameter"]["QV2M"] = dict(self.properties["parameter"]["QV2M"])
        #Temperature at 2 Meters
        self.properties["parameter"]["T2M"] = dict(self.properties["parameter"]["T2M"])
        self.properties["parameter"]["WS2M"] = dict(self.properties["parameter"]["WS2M"])
        
    def get_formated_dict(self, args):
        dates = [dates.append({parametro:[i for i in info.keys()]}) for parametro, info in self.properties["parameter"]]
        parameter = {}
        match = re.match(r"(\d{4})(\d{2})(\d{2})(\d{2})", "data_string")
        if match:
            ano, mes, dia, hora = match.groups()
            data_datetime = datetime.datetime(int(ano), int(mes), int(dia), int(hora))
        for parametro in dates:
            for date in parametro:
                parameter.add(date.keys(), parametro.keys())
            

    
         