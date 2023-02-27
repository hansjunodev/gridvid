import pathlib
import subprocess
import json
import time
import sys
from gridvid import utils
from gridvid.probe import Probe

WIDTH = 1920 // 2
HEIGHT = 1080 // 2
WIDTH_V = 1920 // 3
HEIGHT_V = 1080


class GridVid:
    file: str
    video: Probe
    players: list[subprocess.Popen]

    def __init__(self, file: str) -> None:
        self.file = file
        self.video = Probe(self.file)
        self.num_splits = 3 if self.video.is_vertical else 4
        self.players = []

    def player_dimensions(self, index: int) -> tuple:
        if self.video.is_vertical:
            w = WIDTH_V
            h = HEIGHT_V
            top = 0
            left = index * WIDTH_V
        else:
            w = WIDTH
            h = HEIGHT
            top = 0 + HEIGHT * (index // 2)
            left = WIDTH * (index % 2)

        return (top, left, w, h)

    def ffplay_args(self, index: int):
        rect = self.player_dimensions(index)
        secs_from = (index / self.num_splits) * self.video.duration
        duration = self.video.duration / self.num_splits

        return [
            "ffplay",
            "-top",
            str(rect[0]),
            "-left",
            str(rect[1]),
            "-x",
            str(rect[2]),
            "-y",
            str(rect[3]),
            "-autoexit",
            "-noborder",
            "-ss",
            str(secs_from),
            "-t",
            str(duration),
            self.file,
        ]

    def get_windows(self):
        return utils.find_windows(self.file)

    def wait_for_players(self, timeout_secs=5) -> None:
        start_time = time.time()
        while len(self.get_windows()) < self.num_splits:
            if time.time() - start_time > timeout_secs:
                raise TimeoutError(
                    f"Player windows were not found before {timeout_secs} seconds."
                )
            time.sleep(0.25)

    def play(self) -> None:
        for i in range(self.num_splits):
            self.players.append(
                subprocess.Popen(
                    self.ffplay_args(i),
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )
            )

        try:
            self.wait_for_players()
        except TimeoutError:
            self.stop()

    def stop(self) -> None:
        for player in self.players:
            player.kill()


def run():
    folder_path = pathlib.Path(input("Enter a folder path: "))
    video_files = list(folder_path.glob("*.mp4"))

    print("---")

    while True:
        print(f"Current folder: {folder_path} ({len(video_files)} videos found)")

        index = input("Choose file index: ")

        if index.isdigit():
            file = str(video_files[int(index)])
            gridvid = GridVid(file)

            print(
                f"Playing {gridvid.file} (runtime: {gridvid.video.duration / 60:.1f} mins)"
            )
            gridvid.play()

            input("Press enter to stop playback.")
            gridvid.stop()
        else:
            break

        print("---")


if __name__ == "__main__":
    run()
