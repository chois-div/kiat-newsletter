#!/usr/bin/env python3
"""HRDK 웹진 생성기

사용법:
  python3 hrdk/build.py 2026-12

입력 (hrdk/2026-12/):
  issue.json        호 정보 (연·월·호수·대표색·링크)
  pages/*.html      페이지 본문 (hrdk/templates/base.html 을 상속)
  css/ fonts/ images/

출력:
  hrdk/2026-12/dist/HRDK_웹진_2026-12/   공단 서버에 그대로 올리는 폴더
  hrdk/2026-12/dist/HRDK_웹진_2026-12.zip  같은 폴더 압축본
"""
import json
import re
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent


def build(issue: str) -> int:
    src = ROOT / issue
    ctx = json.loads((src / "issue.json").read_text(encoding="utf-8"))
    name = f"HRDK_웹진_{issue}"
    dist = src / "dist"
    out = dist / name
    if dist.exists():
        shutil.rmtree(dist)
    out.mkdir(parents=True)
    for d in ("css", "fonts", "images"):
        shutil.copytree(src / d, out / d)

    env = Environment(loader=FileSystemLoader([src / "pages", ROOT / "templates"]),
                      undefined=StrictUndefined, autoescape=True)
    pages = sorted(p.name for p in (src / "pages").glob("*.html"))
    for page in pages:
        (out / page).write_text(env.get_template(page).render(ctx), encoding="utf-8")

    # 점검: 없는 페이지로 가는 링크, 없는 이미지
    problems = []
    for page in pages:
        html = (out / page).read_text(encoding="utf-8")
        for ref in set(re.findall(r'(?:href|src)="([^"#:]+)', html)):
            if not (out / ref).exists():
                problems.append(f"{page}: {ref} 없음")
        if 'href="#"' in html:
            problems.append(f"{page}: 주소가 비어 있는 링크(#) {html.count('href=\"#\"')}개")

    shutil.make_archive(str(dist / name), "zip", root_dir=dist, base_dir=name)
    print(f"[{issue}] 페이지 {len(pages)}개 → {out}")
    print(f"[{issue}] 공단 전달용 → {dist / (name + '.zip')}")
    if problems:
        print("\n⚠ 확인 필요:")
        for p in sorted(set(problems)):
            print("  -", p)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(build(sys.argv[1]))
