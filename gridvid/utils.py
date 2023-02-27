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
