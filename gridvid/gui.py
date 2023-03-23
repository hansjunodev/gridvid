from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gridvid import gridvid
from gridvid import utils


class Gui:
    folder: StringVar
    filename: StringVar
    video: gridvid.GridVid

    def __init__(self, root: Tk) -> None:
        self.root = root
        root.title("gridvid")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Global Vars
        self.folder = StringVar()
        self.filename = StringVar()
        self.video = None

        # Make Open Folder Button
        ttk.Button(mainframe, text="Open Folder", command=self.open_folder).grid(
            column=1, row=0, columnspan=2, sticky=(W, E)
        )

        # Make Tree
        self.tree = ttk.Treeview(mainframe)
        self.tree.grid(column=1, row=1, columnspan=2, sticky=(W, E))

        # self.tree.tag_configure("file", background="yellow")
        self.tree.tag_bind("file", "<ButtonRelease-1>", self.tree_clicked)

        # Make Entry
        self.filename_entry = ttk.Entry(mainframe, width=50, textvariable=self.filename)
        self.filename_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E))

        # Make Buttons
        ttk.Button(mainframe, text="Play", command=self.start_playback).grid(
            column=1, row=3, sticky=(W, E)
        )

        ttk.Button(mainframe, text="Stop", command=self.stop_playback).grid(
            column=2, row=3, sticky=(W, E)
        )

        # Make Toolbar
        self.__initialize_toolbar()

        # Add Padding
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.bind("<Return>", self.start_playback)

    def __initialize_tree(self):
        pass

    def __initialize_toolbar(self):
        t = Toplevel(self.root)
        t.attributes("-topmost", True)
        t.geometry("+960+0")
        t.overrideredirect(1)

        ttk.Button(t, text="<", width=3, command=self.play_prev_video).grid(
            column=1, row=1
        )
        ttk.Button(t, text="▶", width=3, command=self.start_playback).grid(
            column=2, row=1
        )
        ttk.Button(t, text="■", width=3, command=self.stop_playback).grid(
            column=3, row=1
        )
        ttk.Button(t, text=">", width=3, command=self.play_next_video).grid(
            column=4, row=1
        )
        ttk.Button(t, text="X", width=3, command=self.close).grid(column=5, row=1)

    def open_folder(self):
        self.folder.set(filedialog.askdirectory(title="Select a folder"))

        self.tree.delete(*self.tree.get_children())

        for file in utils.get_video_files(self.folder.get()):
            self.tree.insert("", "end", file.absolute(), text=file.name, tags=("file"))

    def tree_clicked(self, *args):
        self.filename.set(self.tree.focus())

    def start_playback(self, *args):
        self.stop_playback()
        self.video = gridvid.GridVid(self.filename.get())
        self.video.play()

    def stop_playback(self, *args):
        if self.video is not None:
            self.video.stop()

    def play_prev_video(self, *args):
        prev_item = self.tree.prev(self.tree.focus())
        self.tree.focus(prev_item)
        self.tree.selection_set(prev_item)
        self.filename.set(self.tree.focus())
        self.start_playback()

    def play_next_video(self, *args):
        next_item = self.tree.next(self.tree.focus())
        self.tree.focus(next_item)
        self.tree.selection_set(next_item)
        self.filename.set(self.tree.focus())
        self.start_playback()

    def close(self, *args):
        self.stop_playback()
        self.root.destroy()


def run():
    root = Tk()
    Gui(root)
    root.mainloop()
