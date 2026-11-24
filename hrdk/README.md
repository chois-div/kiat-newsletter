# HRDK 웹진 (한국산업인력공단 HRDKorea)

- `shared/` : 공통 CSS(`css/webzine.css`), Pretendard 글꼴
- `2026-12/` : 12월호 (Vol.363, 대표색 #92D050)
  - `index.html` 메인, `images/` Figma에서 내보낸 이미지

호마다 대표색은 `index.html`의 `<style>:root { --theme: ... }</style>` 한 줄로 바꾼다.
Figma: `hrdk 사보 기획안` 파일의 `12월호 (#92D050)` 섹션 → `HRDK 웹진 11월호` 프레임(1440px)이 메인.

메인 카드는 하위 페이지(star, baeum, myway, field, people, nextpage, trend, sangsaeng, ceo, action, news, event, calendar.html)로 연결된다. 하위 페이지는 아직 없다.
