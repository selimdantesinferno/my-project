"""ffprobe로 영상 메타데이터(해상도/fps/길이)를 읽는다."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .models import seconds_to_us


def probe(path: Path) -> dict:
    """ffprobe로 width/height/fps/duration_us 를 추출한다.

    ffmpeg(ffprobe)가 PATH에 있어야 한다.
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate:format=duration",
        "-of",
        "json",
        str(path),
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    stream = data["streams"][0]
    num, den = stream["r_frame_rate"].split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    duration_s = float(data["format"]["duration"])
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "fps": round(fps, 3),
        "duration_us": seconds_to_us(duration_s),
    }
