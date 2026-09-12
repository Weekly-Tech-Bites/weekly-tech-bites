#!/usr/bin/env python3
"""Rebuild the README Talks table from member presentation files."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


MEMBERS = {
    "kkr010128": "김광래",
    "xoruddl": "이태경",
    "sungahbak": "박성아",
}
TALKS_DIRECTORY = "talks"

REQUIRED_FIELDS = ("round", "date", "topic", "blog")
START_MARKER = "<!-- TALKS:START -->"
END_MARKER = "<!-- TALKS:END -->"
FRONT_MATTER_PATTERN = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


class PresentationError(ValueError):
    """Raised when a presentation file has invalid metadata."""


@dataclass(frozen=True)
class Talk:
    round: int
    date: date
    member_id: str
    member_name: str
    topic: str
    blog: str
    source: Path


def parse_scalar(raw_value: str) -> str:
    value = raw_value.strip()
    if not value:
        return ""

    if value[0] in {'"', "'"}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise PresentationError(f"따옴표가 올바르지 않습니다: {value}") from exc
        if not isinstance(parsed, str):
            raise PresentationError(f"문자열 값이 필요합니다: {value}")
        return parsed.strip()

    return value


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        raise PresentationError("파일 시작 부분에 --- 로 감싼 메타데이터가 필요합니다")

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise PresentationError(f"{line_number}번째 줄이 '항목: 값' 형식이 아닙니다")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            raise PresentationError(f"'{key}' 항목이 중복되었습니다")
        metadata[key] = parse_scalar(raw_value)

    missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
    if missing:
        raise PresentationError(f"필수 항목이 없습니다: {', '.join(missing)}")

    return metadata


def parse_talk(path: Path, root: Path, member_id: str) -> Talk:
    metadata = parse_front_matter(path)

    try:
        round_number = int(metadata["round"])
    except ValueError as exc:
        raise PresentationError("round는 숫자여야 합니다") from exc
    if round_number < 1:
        raise PresentationError("round는 1 이상의 숫자여야 합니다")

    try:
        talk_date = date.fromisoformat(metadata["date"])
    except ValueError as exc:
        raise PresentationError("date는 YYYY-MM-DD 형식의 실제 날짜여야 합니다") from exc

    topic = " ".join(metadata["topic"].split())
    if not topic:
        raise PresentationError("topic은 비워둘 수 없습니다")

    blog = metadata["blog"]
    parsed_url = urlsplit(blog)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise PresentationError("blog는 http:// 또는 https://로 시작하는 전체 URL이어야 합니다")
    if any(character.isspace() for character in blog) or any(character in blog for character in "<>"):
        raise PresentationError("blog URL에 공백, '<', '>' 문자를 사용할 수 없습니다")

    return Talk(
        round=round_number,
        date=talk_date,
        member_id=member_id,
        member_name=MEMBERS[member_id],
        topic=topic,
        blog=blog,
        source=path.relative_to(root),
    )


def collect_talks(root: Path) -> list[Talk]:
    talks: list[Talk] = []
    errors: list[str] = []

    for member_id in MEMBERS:
        member_directory = root / TALKS_DIRECTORY / member_id
        if not member_directory.exists():
            continue

        for path in sorted(member_directory.rglob("*.md")):
            try:
                talks.append(parse_talk(path, root, member_id))
            except (OSError, UnicodeError, PresentationError) as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")

    duplicates: dict[tuple[int, str], list[Path]] = {}
    for talk in talks:
        duplicates.setdefault((talk.round, talk.member_id), []).append(talk.source)
    for (round_number, member_id), paths in duplicates.items():
        if len(paths) > 1:
            joined_paths = ", ".join(str(path) for path in paths)
            errors.append(f"{round_number}회차에 {member_id}의 발표가 중복되었습니다: {joined_paths}")

    if errors:
        details = "\n".join(f"- {error}" for error in errors)
        raise PresentationError(f"발표 파일을 확인해 주세요:\n{details}")

    member_order = {member_id: index for index, member_id in enumerate(MEMBERS)}
    return sorted(
        talks,
        key=lambda talk: (talk.round, talk.date, member_order[talk.member_id], talk.topic.casefold()),
    )


def escape_table_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def build_table(talks: list[Talk]) -> str:
    lines = [
        "| 회차 | 날짜 | 발표자 | 주제 | 블로그 |",
        "| --- | --- | --- | --- | --- |",
    ]

    if not talks:
        lines.append("| - | - | - | 아직 등록된 발표가 없습니다. | - |")
        return "\n".join(lines)

    for talk in talks:
        lines.append(
            "| "
            f"{talk.round} | {talk.date.isoformat()} | {escape_table_cell(talk.member_name)} | "
            f"{escape_table_cell(talk.topic)} | [글 보기](<{talk.blog}>) |"
        )

    return "\n".join(lines)


def update_readme(readme: Path, talks: list[Talk]) -> bool:
    content = readme.read_text(encoding="utf-8")
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)

    if start == -1 or end == -1 or start >= end:
        raise PresentationError("README에서 TALKS:START/TALKS:END 영역을 찾을 수 없습니다")

    generated = f"{START_MARKER}\n\n{build_table(talks)}\n\n{END_MARKER}"
    updated = content[:start] + generated + content[end + len(END_MARKER) :]
    if updated == content:
        return False

    readme.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="저장소 루트 경로",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    readme = root / "README.md"

    try:
        talks = collect_talks(root)
        changed = update_readme(readme, talks)
    except (OSError, UnicodeError, PresentationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    state = "updated" if changed else "already up to date"
    print(f"README {state}: {len(talks)} talk(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
