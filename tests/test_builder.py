from capcut_autoedit.capcut.builder import build_draft_content
from capcut_autoedit.models import Cut, EditPlan, Subtitle, seconds_to_us


def _plan() -> EditPlan:
    return EditPlan(
        source_path="/tmp/in.mp4",
        width=1920,
        height=1080,
        fps=30.0,
        duration_us=seconds_to_us(60),
        cuts=[
            Cut(seconds_to_us(0), seconds_to_us(5)),
            Cut(seconds_to_us(20), seconds_to_us(28)),
        ],
        subtitles=[Subtitle(seconds_to_us(0), seconds_to_us(3), "안녕하세요")],
    )


def test_cuts_are_concatenated_on_timeline():
    draft = build_draft_content(_plan())
    segs = draft["tracks"][0]["segments"]

    assert len(segs) == 2
    # 첫 컷: 타임라인 0부터 5초, 원본 0~5초
    assert segs[0]["target_timerange"] == {"start": 0, "duration": seconds_to_us(5)}
    assert segs[0]["source_timerange"] == {"start": 0, "duration": seconds_to_us(5)}
    # 둘째 컷: 타임라인은 첫 컷 끝(5초)에 이어붙고, 원본은 20초부터
    assert segs[1]["target_timerange"]["start"] == seconds_to_us(5)
    assert segs[1]["source_timerange"]["start"] == seconds_to_us(20)


def test_total_duration_is_sum_of_cuts():
    draft = build_draft_content(_plan())
    assert draft["duration"] == seconds_to_us(13)  # 5 + 8


def test_subtitle_becomes_text_material_and_segment():
    draft = build_draft_content(_plan())
    texts = draft["materials"]["texts"]
    text_segs = draft["tracks"][1]["segments"]

    assert len(texts) == 1
    assert texts[0]["content"] == "안녕하세요"
    assert text_segs[0]["material_id"] == texts[0]["id"]


def test_segment_references_existing_material():
    draft = build_draft_content(_plan())
    video_mat_ids = {m["id"] for m in draft["materials"]["videos"]}
    for seg in draft["tracks"][0]["segments"]:
        assert seg["material_id"] in video_mat_ids


def test_zero_length_cut_rejected():
    import pytest

    with pytest.raises(ValueError):
        Cut(100, 100)
