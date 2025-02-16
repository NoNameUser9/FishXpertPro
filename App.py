from collections import defaultdict
from typing import List
import tkinter as tk
import Fish


class App(tk.Frame):
    def __init__(self, master):
        # self.variables = variables
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

    def setButtonList(self, variables: List[tk.StringVar]):
        self.variables = variables

    def printVariables(self, variables):
        for fish in variables:
            print(fish.get())

    def outputVariables(self, variables, fishList: List[Fish], label: tk.Label):
        dataDict: dict[str, str] = {}
        matching_fish = []

        typeList: List = list(fishList[0].__dict__.keys())

        for item, type_t in zip(variables[0:], typeList[1:]):
            dataDict[type_t] = item.get()

        for fish in fishList:
            match = True
            for key, value in dataDict.items():
                if value is not None and str(getattr(fish, key, None)) != str(value):
                    match = False
                    break
            if match:
                matching_fish.append(fish.Name)

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
                getattr(instance, key).append(value)

        # Убираем дубликаты
        for key in typeList:
            setattr(instance, key, list(dict.fromkeys(getattr(instance, key))))

        return instance

    @staticmethod
    def makeButtonItemList(fishList: List[Fish], instance, buttonListFrame: tk.Frame):
        typeList: List = list(fishList[0].__dict__.keys())
        buttonItemList: List[tk.StringVar] = []
        for typeNow in typeList:
            if typeNow == "Name":
                continue

            frame1inner = tk.Frame(master=buttonListFrame, relief=tk.RAISED, borderwidth=2)
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
