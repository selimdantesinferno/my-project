# CapCut draft 포맷 메모 (비공식)

이 문서는 CapCut 데스크톱 프로젝트 파일 구조를 리버스 엔지니어링하며
정리하는 작업 노트입니다. **공식 문서가 아니며 버전마다 다릅니다.**

## 프로젝트 = 폴더

CapCut 데스크톱은 프로젝트를 단일 `.capcutproj` 파일이 아니라
**폴더 하나**로 저장합니다:

```
<프로젝트 이름>/
  draft_content.json     # 트랙 / 세그먼트 / 소재 (핵심)
  draft_meta_info.json   # 이름, 생성/수정 시각, 길이 등 메타
  (그 외 캐시/썸네일 파일들)
```

CapCut이 인식하려면 보통 CapCut의 Drafts 디렉터리 안에 있어야 합니다.
위치는 OS/버전마다 다릅니다(예: Windows `%LOCALAPPDATA%`, Mac `~/Movies`
하위 등) — 확인되면 여기에 적습니다.

## draft_content.json 핵심 구조

```jsonc
{
  "canvas_config": { "width": 1920, "height": 1080 },
  "fps": 30.0,
  "duration": 13000000,            // 마이크로초
  "materials": {
    "videos": [ { "id", "path", "width", "height", "duration" } ],
    "texts":  [ { "id", "content", ... } ],
    "audios": [], "canvases": [], "stickers": []
  },
  "tracks": [
    {
      "type": "video",
      "segments": [
        {
          "id",
          "material_id",                 // materials.videos[].id 참조
          "target_timerange": { "start", "duration" },  // 타임라인 위치
          "source_timerange": { "start", "duration" }    // 원본에서 자를 구간
        }
      ]
    },
    { "type": "text", "segments": [ { "material_id", "target_timerange" } ] }
  ]
}
```

### 핵심 규칙
- **시간 단위: 마이크로초** (1초 = 1,000,000).
- 세그먼트는 `material_id`로 소재 풀의 항목을 참조한다.
- `target_timerange` = 최종 타임라인에서의 위치/길이.
- `source_timerange` = 원본 소재에서 가져올 구간(컷/트림).

## 검증 체크리스트 (TODO)

- [ ] CapCut 데스크톱 버전 확인: `___`
- [ ] 빈 프로젝트 + 컷 1개 + 자막 1개 만들어 draft 폴더 확보
- [ ] 실제 `draft_content.json` 의 최상위 키 목록 기록
- [ ] video segment 필수 필드 확인 (위 근사치와 차이 보정)
- [ ] text/자막 소재의 실제 필드(폰트, 색, 위치) 기록
- [ ] 우리가 생성한 폴더가 CapCut에서 정상적으로 열리는지 확인
