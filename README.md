# KIAT 뉴스레터

주소: https://chois-div.github.io/kiat-newsletter/
- 웹진: `https://chois-div.github.io/kiat-newsletter/2026-11/`
- 이메일 이미지: `https://chois-div.github.io/kiat-newsletter/email/kiat202611.jpg`
- 이메일 HTML: `https://chois-div.github.io/kiat-newsletter/email/kiat_뉴스레터_26.11.html`

`main` 브랜치에 올리면 GitHub Actions가 `python3 build.py --site`를 실행해서 1~2분 뒤 사이트에 자동으로 반영됩니다.

## 매달 할 일
1. `issues/2026-11` 폴더를 복사해서 `issues/2026-12` 같은 새 호 폴더를 만든다.
2. `content.json`에서 호수, 월, 제목, 카드 문구, 블로그 링크를 바꾼다.
3. Figma에서 이미지를 내보낸다.
   - **PC** 프레임의 히어로와 카드 이미지 → `images/hero.jpg`, `b01~b04.jpg`
   - **MO** 프레임 전체(800×1817) → `email/kiat202612.jpg`
4. GitHub에 올린다. 반영되면 이메일 HTML 주소의 소스를 발송 시스템에 붙여넣는다.
5. `python3 build.py 2026-12`로 만든 `dist/KIAT_웹진_Vol87.zip`을 KIAT에 전달한다. KIAT가 `kiat.or.kr/files/ebook/Vol87/`에 그대로 올린다 (공식 웹진 주소).

로컬에서 미리 확인하려면 `python3 build.py 2026-12`를 실행한다 (최초 1회 `pip install jinja2` 필요). `TODO`로 남은 링크나 빠진 이미지가 있으면 경고가 나온다.

## 구성
| 위치 | 내용 | 수정 빈도 |
|---|---|---|
| `issues/<YYYY-MM>/content.json` | 이번 호 글과 링크 | 매달 |
| `issues/<YYYY-MM>/images/`, `email/` | 이번 호 이미지 | 매달 |
| `site.json` | 공통 링크(홈, 지난 호, SNS), 사이트 주소 | 거의 없음 |
| `templates/` | 웹진과 이메일 HTML 틀 (이메일 이미지맵 좌표 포함) | 레이아웃이 바뀔 때만 |
| `shared/` | CSS, JS, Pretendard 글꼴, 로고, 아이콘 | 거의 없음 |

카드 색상: `b1` 남색, `b2` 주황, `b3` 연두, `b4` 청회색, `b5` 빨강
