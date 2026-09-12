#!/usr/bin/env python3
"""Create a presentation file from GitHub Actions form inputs."""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from update_readme import MEMBERS, TALKS_DIRECTORY, PresentationError, collect_talks


def require_single_line(name: str, value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise PresentationError(f"{name}을(를) 입력해 주세요")
    if "\n" in normalized or "\r" in normalized:
        raise PresentationError(f"{name}은(는) 한 줄로 입력해 주세요")
    return normalized


def make_filename(topic: str) -> str:
    normalized = unicodedata.normalize("NFKC", topic)
    slug = re.sub(r"[^\w-]+", "-", normalized, flags=re.UNICODE).strip("-_")
    if not slug:
        slug = "talk"
    return f"{slug[:80]}.md"


def create_talk(
    root: Path,
    *,
    member_id: str,
    round_value: str,
    date_value: str,
    topic_value: str,
    blog_value: str,
) -> Path:
    if member_id not in MEMBERS:
        raise PresentationError(f"등록된 참여자가 아닙니다: {member_id}")

    try:
        round_number = int(round_value)
    except ValueError as exc:
        raise PresentationError("회차는 숫자여야 합니다") from exc
    if round_number < 1:
        raise PresentationError("회차는 1 이상의 숫자여야 합니다")

    try:
        talk_date = date.fromisoformat(date_value)
    except ValueError as exc:
        raise PresentationError("날짜는 YYYY-MM-DD 형식의 실제 날짜여야 합니다") from exc

    topic = require_single_line("발표 주제", topic_value)
    blog = require_single_line("블로그 URL", blog_value)
    parsed_url = urlsplit(blog)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise PresentationError("블로그 URL은 http:// 또는 https://로 시작해야 합니다")
    if any(character.isspace() for character in blog) or any(character in blog for character in "<>"):
        raise PresentationError("블로그 URL에 공백, '<', '>' 문자를 사용할 수 없습니다")

    for talk in collect_talks(root):
        if talk.member_id == member_id and talk.round == round_number:
            raise PresentationError(
                f"{member_id}의 {round_number}회차 발표가 이미 존재합니다: {talk.source}"
            )

    member_directory = root / TALKS_DIRECTORY / member_id
    destination = member_directory / make_filename(topic)
    if destination.exists():
        raise PresentationError(f"같은 이름의 발표 파일이 이미 존재합니다: {destination.relative_to(root)}")

    member_directory.mkdir(parents=True, exist_ok=True)
    content = (
        "---\n"
        f"round: {round_number}\n"
        f"date: {json.dumps(talk_date.isoformat(), ensure_ascii=False)}\n"
        f"topic: {json.dumps(topic, ensure_ascii=False)}\n"
        f"blog: {json.dumps(blog, ensure_ascii=False)}\n"
        "---\n"
    )
    destination.write_text(content, encoding="utf-8")
    return destination


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    try:
        destination = create_talk(
            root,
            member_id=os.environ.get("TALK_MEMBER", ""),
            round_value=os.environ.get("TALK_ROUND", ""),
            date_value=os.environ.get("TALK_DATE", ""),
            topic_value=os.environ.get("TALK_TOPIC", ""),
            blog_value=os.environ.get("TALK_BLOG", ""),
        )
    except (OSError, UnicodeError, PresentationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Created {destination.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
