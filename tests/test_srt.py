from capcut_autoedit.export.srt import to_srt
from capcut_autoedit.models import Subtitle, seconds_to_us


def test_empty_subtitles_returns_empty_string():
    assert to_srt([]) == ""


def test_basic_block_format():
    subs = [Subtitle(seconds_to_us(0), seconds_to_us(2.5), "안녕")]
    out = to_srt(subs)
    assert out.startswith("1\n00:00:00,000 --> 00:00:02,500\n안녕\n")


def test_multiple_blocks_are_separated_by_blank_line():
    subs = [
        Subtitle(seconds_to_us(0), seconds_to_us(1), "A"),
        Subtitle(seconds_to_us(1), seconds_to_us(2), "B"),
    ]
    out = to_srt(subs)
    # 각 블록은 빈 줄로 구분
    assert "안녕" not in out
    assert "\n\n2\n" in out


def test_timestamp_hours_minutes_milliseconds():
    # 1h 2m 3.456s
    us = seconds_to_us(3600 + 2 * 60 + 3.456)
    subs = [Subtitle(0, us, "x")]
    out = to_srt(subs)
    assert "00:00:00,000 --> 01:02:03,456" in out
