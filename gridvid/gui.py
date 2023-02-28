import pathlib
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gridvid import gridvid
from gridvid import utils


class Gui:
    filename: StringVar
    video: gridvid.GridVid

    def __init__(self, root: Tk) -> None:
        root.title("gridvid")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Global Vars
        self.filename = StringVar()
        self.folder = StringVar()

        # Make Filepicker
        self.folder.set(filedialog.askdirectory(title="Select a folder"))

        # Make Tree
        self.tree = ttk.Treeview(mainframe)
        self.tree.grid(column=1, row=1, columnspan=2, sticky=(W, E))

        for file in utils.get_video_files(self.folder.get()):
            self.tree.insert("", "end", file.absolute(), text=file.name, tags=("file"))

        self.tree.tag_configure("file", background="yellow")
        self.tree.tag_bind("file", "<ButtonRelease-1>", self.tree_clicked)

        # Make Entry
        self.filename_entry = ttk.Entry(mainframe, width=50, textvariable=self.filename)
        self.filename_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E))

        # Make Buttons
        ttk.Button(mainframe, text="Play", command=self.play_video).grid(
            column=1, row=3, sticky=(W, E)
        )

        ttk.Button(mainframe, text="Stop", command=self.stop_video).grid(
            column=2, row=3, sticky=(W, E)
        )

        # Make Toolbar
        t = Toplevel(root)
        t.attributes("-topmost", True)
        t.geometry("+960+0")
        t.overrideredirect(1)
        
        ttk.Button(t, text="<", width=3, command=self.prev_video).grid(column=1, row=1)
        ttk.Button(t, text="▶", width=3, command=self.play_video).grid(column=2, row=1)
        ttk.Button(t, text="■", width=3, command=self.stop_video).grid(column=3, row=1)
        ttk.Button(t, text=">", width=3, command=self.next_video).grid(column=4, row=1)
        ttk.Button(t, text="X", width=3, command=lambda: root.destroy()).grid(column=5, row=1)

        # Add Padding
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.bind("<Return>", self.play_video)

    def tree_clicked(self, e):
        self.filename.set(self.tree.focus())
        print(self.tree.focus())

    def play_video(self, *args):
        self.video = gridvid.GridVid(self.filename.get())
        self.video.play()

    def stop_video(self, *args):
        if self.video:
            self.video.stop()

    def prev_video(self, *args):
        self.video.stop()
        self.tree.focus(self.tree.prev(self.tree.item(self.tree.focus())))

    def next_video(self, *args):
        self.video.stop()
        self.tree.focus(self.tree.next(self.tree.item(self.tree.focus())))


def run():
    root = Tk()
    Gui(root)
    root.mainloop()
