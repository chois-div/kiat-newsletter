#!/usr/bin/env python3
"""KIAT 뉴스레터 생성기

사용법:
  python3 build.py 2026-11     한 호만 생성 → issues/2026-11/dist/
  python3 build.py --site      모든 호를 생성해서 _site/ 에 사이트 전체를 조립
                               (GitHub Actions 가 push 때마다 실행)

한 호 폴더 구성 (issues/2026-11/):
  content.json                 이번 호 글·링크
  images/                      hero.jpg, b01~b04.jpg  (Figma PC 프레임에서 내보내기)
  email/kiat202611.jpg         이메일 통이미지 800x1817 (Figma MO 프레임에서 내보내기)

사이트 구조 (_site/):
  index.html                   전체 호 목록 (지난 호 보기)
  2026-11/                     웹진
  email/kiat202611.jpg         이메일 이미지 (메일 본문이 이 주소를 불러옴)
  email/kiat_뉴스레터_26.11.html  이메일 HTML (발송 시스템에 붙여넣기용)
"""
import html
import json
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent
ISSUES = ROOT / "issues"


def build_issue(issue: str) -> tuple[dict, list[str]]:
    issue_dir = ISSUES / issue
    content = json.loads((issue_dir / "content.json").read_text(encoding="utf-8"))
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))

    y, m = content["year"], content["month"]
    official = site.get("official_web_pattern", "").format(vol=content["vol"]) or (
        f"{site['web_base']}{issue}/" if site["web_base"] else "")
    email_img = f"kiat{y}{m:02d}.jpg"
    ctx = {
        **content,
        "month2": f"{m:02d}",
        "links": site["links"],
        "web_url": official,
        "og_image": f"{official}images/{content['hero']['image']}" if official else "",
        "email": {"image_url": f"{site['email_image_base']}{email_img}", "image_file": email_img},
    }

    # 점검: TODO 링크, 빠진 이미지
    problems = []
    if "TODO" in ctx["hero"]["link"]:
        problems.append("히어로 링크가 TODO")
    for c in ctx["cards"]:
        if "TODO" in c["link"]:
            problems.append(f"'{c['label']}' 카드 링크가 TODO")
    for img in [ctx["hero"]["image"]] + [c["image"] for c in ctx["cards"]]:
        if not (issue_dir / "images" / img).exists():
            problems.append(f"이미지 없음: images/{img}")
    if not (issue_dir / "email" / email_img).exists():
        problems.append(f"이메일 이미지 없음: email/{email_img} (Figma MO 프레임 내보내기)")

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), undefined=StrictUndefined, autoescape=True)

    dist = issue_dir / "dist"
    web = dist / "web"
    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(ROOT / "shared", web)          # css, js, 폰트, 공통 아이콘·로고
    for f in (issue_dir / "images").iterdir():     # 이번 호 이미지
        shutil.copy2(f, web / "images" / f.name)
    (web / "index.html").write_text(env.get_template("web.html").render(ctx), encoding="utf-8")

    email_name = f"kiat_뉴스레터_{str(y)[2:]}.{m:02d}.html"
    (dist / email_name).write_text(env.get_template("email.html").render(ctx), encoding="utf-8")

    # KIAT 전달용: VolNN/ 폴더째 압축 (kiat.or.kr/files/ebook/VolNN/ 에 그대로 업로드)
    vol_dir = f"Vol{content['vol']}"
    tmp = dist / "_pack"
    shutil.copytree(web, tmp / vol_dir)
    shutil.make_archive(str(dist / f"KIAT_웹진_{vol_dir}"), "zip", root_dir=tmp, base_dir=vol_dir)
    shutil.rmtree(tmp)

    print(f"[{issue}] 웹진: {web / 'index.html'}")
    print(f"[{issue}] 이메일: {dist / email_name}")
    print(f"[{issue}] 이메일 이미지 주소: {ctx['email']['image_url']}")
    print(f"[{issue}] KIAT 전달용: {dist / f'KIAT_웹진_{vol_dir}.zip'}  →  {official}")
    ctx["_email_name"] = email_name
    return ctx, problems


def report(issue: str, problems: list[str]) -> None:
    if problems:
        print(f"\n⚠ [{issue}] 확인 필요:")
        for p in problems:
            print("  -", p)


def build_site() -> int:
    out = ROOT / "_site"
    if out.exists():
        shutil.rmtree(out)
    (out / "email").mkdir(parents=True)

    rows = []
    issue_dirs = sorted((d for d in ISSUES.iterdir() if (d / "content.json").exists()), reverse=True)
    latest = issue_dirs[0].name
    for issue_dir in issue_dirs:
        issue = issue_dir.name
        ctx, problems = build_issue(issue)
        report(issue, problems)
        shutil.copytree(issue_dir / "dist" / "web", out / issue)
        shutil.copy2(issue_dir / "dist" / ctx["_email_name"], out / "email" / ctx["_email_name"])
        email_img = issue_dir / "email" / ctx["email"]["image_file"]
        if email_img.exists():
            shutil.copy2(email_img, out / "email" / email_img.name)
        rows.append(
            f'<li><a href="./{issue}/"><b>{ctx["year"]}. {ctx["month2"]}. VOL {ctx["vol"]}</b>'
            f' {html.escape(ctx["hero"]["title"])}</a></li>'
        )

    (out / "index.html").write_text(
        "<!doctype html><html lang=\"ko\"><head><meta charset=\"UTF-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
        f"<title>KIAT 뉴스레터</title><link rel=\"stylesheet\" href=\"./{latest}/css/init.css\">"
        "<style>body{max-width:720px;margin:0 auto;padding:60px 20px}h1{font-size:32px;font-weight:800;"
        "color:#06377b;margin-bottom:30px}li{border-bottom:1px solid #ddd}li a{display:block;padding:18px 0;"
        "font-size:18px}li b{color:#06377b;font-weight:700;margin-right:12px}</style></head><body>"
        "<h1>KIAT NEWS LETTER</h1><ul>" + "".join(rows) + "</ul></body></html>",
        encoding="utf-8",
    )
    (out / ".nojekyll").write_text("")
    print(f"\n사이트 조립 완료: {out}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "--site":
        sys.exit(build_site())
    _, probs = build_issue(sys.argv[1])
    report(sys.argv[1], probs)
    sys.exit(1 if probs else 0)
