import tkinter as tk
    
class Gui:
    @staticmethod
    def prompt_name():
        root = tk.Tk()

        _name_ = tk.StringVar()

        canvas = tk.Canvas(root, width=400, height=300, relief="raised")
        canvas.pack()

        label1 = tk.Label(root, text="Car-BioID")
        label1.config(font=("roboto", 14))
        canvas.create_window(200, 25, window=label1)

        label2 = tk.Label(root, text="What is your name?")
        label2.config(font=("roboto", 10))
        canvas.create_window(200, 100, window=label2)

        entry = tk.Entry(root, justify="center", textvariable=_name_)
        entry.pack()
        canvas.create_window(200, 140, window=entry)

        button = tk.Button(
            text="Enter",
            command=root.destroy,
            bg="brown",
            fg="white",
            font=("roboto", 9, "bold")
        )
        canvas.create_window(200, 180, window=button)

        root.mainloop()
        return _name_.get()