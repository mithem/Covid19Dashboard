import tkinter as tk
from DataManager import DataManager

class UI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.manager = DataManager()
        self.pack()
        self.create_ui()
    
    def create_ui(self):
        self.country_list = tk.Listbox(self)
        self.country_list.pack(side=tk.LEFT)
        tk.Button(self, text="Refresh", command=self.refresh).pack(side=tk.LEFT)
    
    def refresh(self):
        self.manager.load_from_api()
        for measurement in self.manager.latest_measurements:
            self.country_list.insert(round(measurement.date.timestamp()), str(measurement))


if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("700x600")
    root.resizable(700, 600)
    root.title("Covid19 Dashboard")
    gui = UI(root)
    gui.mainloop()