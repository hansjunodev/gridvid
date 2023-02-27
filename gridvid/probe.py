import json
import subprocess
from gridvid.custom_types import ProbeResult


class Probe:
    def __init__(self, file: str) -> None:
        self.file = file
        self.args = ["ffprobe", "-i", self.file, "-show_format", "-show_entries", "stream=width,height:stream_side_data=rotation", "-select_streams", "v", "-v", "quiet", "-print_format", "json=compact=1"]  # fmt: skip
        self.probe = subprocess.run(self.args, capture_output=True)
        self.dict: ProbeResult = json.loads(self.probe.stdout)

    @property
    def width(self) -> int:
        return self.dict["streams"][0]["width"]

    @property
    def height(self) -> int:
        return self.dict["streams"][0]["height"]

    @property
    def duration(self) -> float:
        return float(self.dict["format"]["duration"])

    @property
    def rotation(self) -> int:
        try:
            return self.dict["streams"][0]["side_data_list"][0]["rotation"]
        except:
            return 0

    @property
    def is_vertical(self) -> bool:
        return True if self.height > self.width or self.rotation else False

    def __repr__(self) -> str:
        return self.probe.stdout.decode()
