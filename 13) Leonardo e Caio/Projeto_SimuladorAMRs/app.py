import tkinter as tk
from interface import Interface

if __name__ == "__main__":
    print(">>> Interface grafica <<<")

    root = tk.Tk()
    
    appInterface = Interface(root)

    root.mainloop()

