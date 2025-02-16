class Fish(object):
    def __init__(self, Name: str = "NaN", waterTemp: int = 0, food: str = "NaN", waterType: str = "NaN",
                 behavior: str = "NaN", aquariumSize: int = 0, pH: float = 0.0, herd: bool = False,
                 aeration: bool = False, waterPurity: int = 0):
        self.Name = Name
        self.waterTemp = waterTemp
        self.food = food
        self.waterType = waterType
        self.behavior = behavior
        self.aquariumSize = aquariumSize
        self.pH = pH
        self.herd = herd
        self.aeration = aeration
        self.waterPurity = waterPurity