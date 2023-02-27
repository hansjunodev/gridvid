from tkinter import *
from tkinter import ttk
from gridvid import gridvid


class Gui:
    filename: StringVar
    video: gridvid.GridVid

    def __init__(self, root: Tk) -> None:
        root.title("gridvid")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.filename = StringVar()
        filename_entry = ttk.Entry(mainframe, width=50, textvariable=self.filename)
        filename_entry.grid(column=1, row=1, columnspan=2, sticky=(W, E))

        ttk.Button(mainframe, text="Play", command=self.play_video).grid(
            column=1, row=2, sticky=(W, E)
        )

        ttk.Button(mainframe, text="Stop", command=self.stop_video).grid(
            column=2, row=2, sticky=(W, E)
        )

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        filename_entry.focus()

        root.bind("<Return>", self.play_video)

    def play_video(self, *args):
        self.video = gridvid.GridVid(self.filename.get())
        self.video.play()

    def stop_video(self, *args):
        if self.video:
            self.video.stop()


def run():
    root = Tk()
    Gui(root)
    root.mainloop()
