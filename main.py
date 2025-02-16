import tkinter as tk
import json
from typing import List
from Fish import Fish
from App import App


# # TODO: Добавить поиск
# def fishFinder(fishObject: object, fishList: List[Fish]):
#     print("Hi. Fish is found:")
#     label.config(text="Hi. Fish is found:")
#     # print(fishObject[0].__dict__.keys())
#     keysList = fishList[0].__dict__.keys()


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry('700x700')
    window.minsize(500, 500)

    window.iconbitmap('data/fish.ico')
    with open('data/data.json', 'r') as file:
        jsonData = json.load(file)
        fishList = [Fish(**data) for data in jsonData]

    instance = App.makeTypeList(fishList)

    mainFrame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=2)
    mainFrame.pack(fill="both", expand=True, side="top")

    frame1 = tk.Frame(master=mainFrame, relief=tk.RAISED, borderwidth=2)
    frame1.pack(fill="both", expand=True, side="left")

    buttonItemList = App.makeButtonItemList(fishList, instance, frame1)

    print(*[item.get() for item in buttonItemList])

    frame2 = tk.Frame(master=mainFrame, relief=tk.RAISED, borderwidth=2)
    frame2.pack(fill="both", expand=True, side="right")

    label = tk.Label(frame2, text=" ")
    label.pack()

    app = App(window)
    # app.setButtonList(buttonItemList)
    tk.Button(frame2, text="Click Me", command=lambda: app.outputVariables(buttonItemList, fishList, label)).pack(side="bottom")
    # tk.Button(frame2, text="Click Me", command=lambda: fishFinder(instance, fishList)).pack(side="bottom")
    app.mainloop()
