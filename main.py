import tkinter as tk
import json
from typing import List
from collections import defaultdict


class Fish(object):
    def __init__(self, waterTemp: int = 0, food: str = "NaN", waterType: str = "NaN", behavior: str = "NaN", aquariumSize: int = 0, pH: float = 0.0, herd: bool = False, aeration: bool = False, waterPurity: int = 0):
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
                getattr(instance, key).append(getattr(fish, key))

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
def fishFinder(fishObject: object):
    print("Hi. Fish is found:")
    label.config(text="Hi. Fish is found:")

    for key, value in fishObject.__dict__.items():
        if value:
            print(key, ":", value)
            label.config(text=label.cget("text") + "\n" + key + ":" + value)


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
    # tk.Button(frame2, text="Click Me", command=lambda: app.printVariables(buttonItemList)).pack(side="bottom")
    tk.Button(frame2, text="Click Me", command=lambda: fishFinder(instance)).pack(side="bottom")
    app.mainloop()
