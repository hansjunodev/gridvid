import typing


class SideData(typing.TypedDict, total=False):
    rotation: int


class ProbeStreamData(typing.TypedDict, total=False):
    width: int
    height: int
    side_data_list: list[SideData]


class ProbeFormatData(typing.TypedDict, total=False):
    duration: float


class ProbeResult(typing.TypedDict, total=False):
    format: ProbeFormatData
    streams: list[ProbeStreamData]


if __name__ == "__main__":
    pass
