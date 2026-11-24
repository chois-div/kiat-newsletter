# HRDK 웹진 (한국산업인력공단 HRDKorea)

완성본은 공단 서버에 폴더째 올린다.

```
python3 hrdk/build.py 2026-12      # 최초 1회 pip install jinja2
```
→ `hrdk/2026-12/dist/HRDK_웹진_2026-12/` (서버에 올릴 폴더)와 같은 이름의 `.zip`.
빠진 이미지·페이지, 주소가 빈 링크(`#`)가 있으면 경고가 나온다.

## 구성
| 위치 | 내용 |
|---|---|
| `templates/base.html` | 상단(로고·호수·메뉴)과 하단 공통 틀 |
| `templates/cardnews.html` | 카드뉴스 페이지 틀 (상단 통이미지 + 세로 이미지) |
| `2026-12/issue.json` | 호수, 월, 대표색, 이전호·PDF·SNS 링크 |
| `2026-12/pages/` | 페이지별 본문. index(메인), star(人STAR), 카드뉴스 8개 등 |
| `2026-12/css/webzine.css` | 스타일. 1440px 시안 기준, 768px 미만은 모바일 배치 |
| `2026-12/images/` | Figma에서 내보낸 이미지 (페이지별 폴더) |

Figma: `hrdk 사보 기획안` 파일의 `12월호 (#92D050)` 섹션. 프레임 이름이 곧 페이지.
