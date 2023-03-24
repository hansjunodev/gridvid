import os.path
import pickle
import keyboard

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
        ttk.Button(mainframe, text="Open Folder", command=self.open_folder_picker).grid(
            column=1, row=0, columnspan=2, sticky=(W, E)
        )

        # Make Tree
        self.tree = ttk.Treeview(mainframe, height=30)
        self.tree.grid(column=1, row=1, columnspan=2, sticky=(W, E))

        self.tree.tag_configure("folder", background="yellow")
        # self.tree.tag_configure("file", background="yellow")
        self.tree.tag_bind("file", "<ButtonRelease-1>", self.handle_tree_click)
        self.tree.tag_bind("file", "<Double-1>", self.handle_file_double_click)
        self.tree.tag_bind("folder", "<Double-1>", self.handle_folder_double_click)

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

        keyboard.add_hotkey("a", self.play_prev_video)
        keyboard.add_hotkey("left", self.play_prev_video)

        keyboard.add_hotkey("w", self.select_prev_item)
        keyboard.add_hotkey("up", self.select_prev_item)

        keyboard.add_hotkey("s", self.select_next_item)
        keyboard.add_hotkey("down", self.select_next_item)

        keyboard.add_hotkey("d", self.play_next_video)
        keyboard.add_hotkey("right", self.play_next_video)

        # TODO: Move selection to next video, not next item. i.e. skip folders
        keyboard.add_hotkey("space", self.start_playback)
        keyboard.add_hotkey("esc", self.stop_playback)

        root.protocol("WM_DELETE_WINDOW", self.handle_close)

        # Load Saved State
        self.load_state()

    def __initialize_toolbar(self):
        t = Toplevel(self.root)
        t.attributes("-topmost", True)
        t.geometry("+960+0")
        t.overrideredirect(1)

        ttk.Button(t, text="<", width=3, command=self.play_prev_video).grid(
            column=1, row=1
        )
        ttk.Button(t, text=">", width=3, command=self.play_next_video).grid(
            column=2, row=1
        )
        ttk.Button(t, text="X", width=3, command=self.stop_playback).grid(
            column=3, row=1
        )

    def open_folder_picker(self):
        self.folder.set(filedialog.askdirectory(title="Choose a folder"))
        self.clear_tree()
        self.populate_tree()

        # TODO: get list of folders as well <- double click to open folder and populate fields
        # TODO: option to list all videos of depth < 3
        # TODO: double click video file to play
        # TODO: toolbar <- X closes video, not the program
        # TODO: show video duration in toolbar

    def handle_tree_click(self, *args):
        self.filename.set(self.tree.focus())

    def handle_file_double_click(self, *args):
        self.filename.set(self.tree.focus())
        self.start_playback()

    def handle_folder_double_click(self, *args):
        self.load_folder(self.tree.focus())

    def load_folder(self, path: str):
        self.folder.set(path)
        self.clear_tree()
        self.populate_tree()

    def populate_tree(self):
        if not self.folder.get():
            return

        # Parent directory
        # TODO: What if there is no parent folder? don't add this item
        parent_folder = utils.get_parent_folder(self.folder.get())
        self.tree.insert(
            "", "end", parent_folder.absolute(), text="⇧ ..", tags=("folder")
        )

        # Subdirectories
        for folder in utils.get_subdirectories(self.folder.get()):
            self.tree.insert(
                "", "end", folder.absolute(), text=folder.name + "/", tags=("folder")
            )

        # Video files
        for file in utils.get_video_files(self.folder.get()):
            self.tree.insert("", "end", file.absolute(), text=file.name, tags=("file"))

        # Select the first item
        children = self.tree.get_children()
        if children:
            self.tree.focus(children[0])
            self.tree.selection_set(children[0])

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def start_playback(self, *args):
        self.stop_playback()
        if os.path.isfile(self.filename.get()):
            self.video = gridvid.GridVid(self.filename.get())
            self.video.play()

    def stop_playback(self, *args):
        if self.video is not None:
            self.video.stop()

    def select_prev_item(self, *args):
        prev_item = self.tree.prev(self.tree.focus())

        if prev_item:
            self.tree.focus(prev_item)
            self.tree.selection_set(prev_item)
            self.tree.see(prev_item)
            self.filename.set(self.tree.focus())

    def select_next_item(self, *args):
        next_item = self.tree.next(self.tree.focus())

        if next_item:
            self.tree.focus(next_item)
            self.tree.selection_set(next_item)
            self.tree.see(next_item)
            self.filename.set(self.tree.focus())

    def play_prev_video(self, *args):
        self.select_prev_item()
        self.start_playback()

    def play_next_video(self, *args):
        self.select_next_item()
        self.start_playback()

    def close(self, *args):
        self.stop_playback()
        self.root.destroy()

    def handle_close(self):
        self.save_state()
        self.stop_playback()
        self.root.destroy()

    def save_state(self):
        with open("ultra-video.settings", "wb+") as file:
            state = {"last_opened_directory": self.folder.get()}
            pickle.dump(state, file)

    def load_state(self):
        try:
            with open("ultra-video.settings", "rb") as file:
                state = pickle.load(file)
        except:
            state = self.initial_state()

        self.folder.set(state["last_opened_directory"])
        self.populate_tree()

    def initial_state(self) -> dict:
        state = {"last_opened_directory": "C:/"}
        return state


def run():
    root = Tk()
    Gui(root)
    root.mainloop()
