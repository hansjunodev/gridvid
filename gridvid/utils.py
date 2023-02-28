import pathlib
import win32gui


"""
Need to find windows with the following attributes:

titel: [filepath]
class: SDL_app
exe:   ffplay.exe
"""


def find_windows(title) -> list[str]:
    result = []

    def callback(hwnd: str, _):
        window_text = win32gui.GetWindowText(hwnd)

        if window_text == title:
            result.append(hwnd)

    win32gui.EnumWindows(callback, None)

    return result


def get_video_files(folder: str) -> list[pathlib.Path]:
    exts = (
        "*.webm",
        "*.mkv",
        "*.flv",
        "*.avi",
        "*.mov",
        "*.qt",
        "*.wmv",
        "*.mp4",
        "*.m4p",
        "*.m4v",
        "*.mpg",
        "*.mp2",
        "*.mpeg",
        "*.mpe",
        "*.mpv",
        "*.m2v",
        "*.m4v",
        "*.3gp",
        "*.3g2",
    )

    videos = []
    for ext in exts:
        videos.extend(list(pathlib.Path(folder).glob(ext)))

    return videos
