class DistrictCard:
    def __init__(self, value, type, name, effect):
        self.value = value 
        self.type = type
        self.name = name 
        self.effect = effect 

    def __str__(self):
        return print("value: ", self.value, \
            "type: ", self.type, \
            "name: ",self.name, \
            "effect: ", self.effect)