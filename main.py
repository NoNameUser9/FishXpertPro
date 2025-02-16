import tkinter as tk
import json
from typing import List
from collections import defaultdict


class Fish(object):
    def __init__(self, Name: str = "NaN", waterTemp: int = 0, food: str = "NaN", waterType: str = "NaN", behavior: str = "NaN", aquariumSize: int = 0, pH: float = 0.0, herd: bool = False, aeration: bool = False, waterPurity: int = 0):
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


class App(tk.Frame):
    def __init__(self, master, variables: List[tk.StringVar]):
        self.variables = variables
        super().__init__(master)
        self.pack()
        self.master.title("FishXpertPro")  # tk.Tk() -> tk.fr

        # self.entrythingy = tk.Button()
        # self.entrythingy.pack()
        #
        # # Create the application variable.
        # self.contents = tk.StringVar()
        # # Set it to some value.
        # self.contents.set("this is a variable")
        # # Tell the entry widget to watch this variable.
        # self.entrythingy["textvariable"] = self.contents
        #
        # # Define a callback for when the user hits return.
        # # It prints the current value of the variable.
        # self.entrythingy.bind('<Button-1>', self.printVariables)

    def printVariables(self, event):
        # decodedDataList = [Fish(**data) for data in self.variables]
        for fish in self.variables:
            print(fish.get())


    def outputVariables(self, event, fishList: List[Fish]):
        # decodedDataList = [Fish(**data) for data in self.variables]
        dataDict: dict[str, str] = {}
        matching_fish = []

        typeList: List = list(fishList[0].__dict__.keys())

        for item, type_t in zip(self.variables, typeList):
            dataDict[type_t] = item.get()

        # print(dataDict)

        # for fish in dataList:
        #     if all(str(value) in map(str, dataList) for value in dataList if value != "Нет данных"):
        #         matching_fish.append(fish)

        # # fishList
        # if matching_fish:
        #     print("Найденные рыбы:")
        #     for fish in matching_fish:
        #         print(fish)

        for fish in fishList:
            match = True
            # print(fish.__dict__)
            for key, value in dataDict.items():
                # print(key, value)
                # print(dataDict)
                # print(getattr(fish, key, None))
                if value is not None and str(getattr(fish, key, None)) != str(value):
                    # print(f"getattr(fish, key, None): {getattr(fish, key, None)}, value: {value}")
                    match = False
                    # print("break")
                    break
            if match:
                matching_fish.append(fish.Name)
        # print("result:", matching_fish)
        label.config(text="\n".join(matching_fish))


    @staticmethod
    def makeTypeList(fishList: List[Fish]):
        typeList: List = list(fishList[0].__dict__.keys())
        # Создаём класс динамически
        ListOfTypes = type(
            "ListOfTypes",
            (object,),
            {"__dict__": defaultdict(list)}  # Делаем __dict__ объектом defaultdict
        )

        # Создаём экземпляр
        instance = ListOfTypes()

        # Инициализируем атрибуты вручную
        for key in typeList:
            setattr(instance, key, [])  # Создаём отдельные списки в __dict__

        # Заполняем экземпляр
        for fish in fishList:
            for key in typeList:
                value = getattr(fish, key)

                # print(value)

                # Приводим к bool, если исходное значение является bool
                # if isinstance(value, bool):
                value = str(value)  # Оставляем True/False
                # elif isinstance(value, int):
                #     value = int(value)  # Оставляем int
                # elif isinstance(value, str):
                #     value = str(value)  # Оставляем str

                getattr(instance, key).append(value)

        # for key in typeList:
        #     print(getattr(instance, key))

        # Убираем дубликаты
        for key in typeList:
            setattr(instance, key, list(set(getattr(instance, key))))

        return instance

    @staticmethod
    def makeButtonItemList(fishList: List[Fish], instance):
        typeList: List = list(fishList[0].__dict__.keys())
        buttonItemList: List[tk.StringVar] = []
        for typeNow in typeList:
            frame1inner = tk.Frame(master=frame1, relief=tk.RAISED, borderwidth=2)
            frame1inner.pack(fill="both", expand=True)

            options = getattr(instance, typeNow, [])
            if not options:
                options = ["Нет данных"]

            clicked = tk.StringVar()
            clicked.set(options[0])  # Устанавливаем значение по умолчанию

            label = tk.Label(master=frame1inner, text=typeNow)  # Добавляем подпись с названием атрибута
            label.pack(padx=5, pady=5, anchor="w", side="left")

            option_menu = tk.OptionMenu(frame1inner, clicked, *options)  # Создаём OptionMenu внутри frame
            buttonItemList.append(clicked)
            option_menu.pack(anchor="w", side="right")

        return buttonItemList


# TODO: Добавить поиск
def fishFinder(fishObject: object, fishList: List[Fish]):
    print("Hi. Fish is found:")
    label.config(text="Hi. Fish is found:")
    # print(fishObject[0].__dict__.keys())
    keysList = fishList[0].__dict__.keys()


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry('700x700')
    window.minsize(500, 500)

    with open('data.json', 'r') as file:
        jsonData = json.load(file)
        fishList = [Fish(**data) for data in jsonData]


    instance = App.makeTypeList(fishList)

    mainFrame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=2)
    mainFrame.pack(fill="both", expand=True, side="top")

    frame1 = tk.Frame(master=mainFrame, relief=tk.RAISED, borderwidth=2)
    frame1.pack(fill="both", expand=True, side="left")

    buttonItemList = App.makeButtonItemList(fishList, instance)

    frame2 = tk.Frame(master=mainFrame, relief=tk.RAISED, borderwidth=2)
    frame2.pack(fill="both", expand=True, side="right")

    label = tk.Label(frame2, text=" ")
    label.pack()

    app = App(window, buttonItemList)
    tk.Button(frame2, text="Click Me", command=lambda: app.outputVariables(buttonItemList, fishList)).pack(side="bottom")
    # tk.Button(frame2, text="Click Me", command=lambda: fishFinder(instance, fishList)).pack(side="bottom")
    app.mainloop()
