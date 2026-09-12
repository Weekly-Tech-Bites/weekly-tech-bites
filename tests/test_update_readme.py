from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import update_readme  # noqa: E402
import create_talk  # noqa: E402


class UpdateReadmeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.readme = self.root / "README.md"
        self.readme.write_text(
            "# Test\n\n"
            f"{update_readme.START_MARKER}\n\n"
            "old table\n\n"
            f"{update_readme.END_MARKER}\n",
            encoding="utf-8",
        )
        self.member_directory = self.root / "talks" / "kkr010128"
        self.member_directory.mkdir(parents=True)
        self.presentation = self.member_directory / "talk.md"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_presentation(self, *, topic: str, blog: str) -> None:
        self.presentation.write_text(
            "---\n"
            "round: 1\n"
            'date: "2026-09-18"\n'
            f'topic: "{topic}"\n'
            f'blog: "{blog}"\n'
            "---\n",
            encoding="utf-8",
        )

    def regenerate(self) -> str:
        talks = update_readme.collect_talks(self.root)
        update_readme.update_readme(self.readme, talks)
        return self.readme.read_text(encoding="utf-8")

    def test_add_update_and_delete_are_reflected(self) -> None:
        self.write_presentation(topic="기존 제목", blog="https://example.com/old")
        content = self.regenerate()
        self.assertIn("기존 제목", content)
        self.assertIn("https://example.com/old", content)

        self.write_presentation(topic="수정된 제목", blog="https://example.com/new")
        content = self.regenerate()
        self.assertNotIn("기존 제목", content)
        self.assertNotIn("https://example.com/old", content)
        self.assertIn("수정된 제목", content)
        self.assertIn("https://example.com/new", content)

        self.presentation.unlink()
        content = self.regenerate()
        self.assertNotIn("수정된 제목", content)
        self.assertIn("아직 등록된 발표가 없습니다.", content)

    def test_invalid_date_is_rejected(self) -> None:
        self.presentation.write_text(
            "---\n"
            "round: 1\n"
            'date: "2026-02-30"\n'
            'topic: "잘못된 날짜"\n'
            'blog: "https://example.com"\n'
            "---\n",
            encoding="utf-8",
        )

        with self.assertRaises(update_readme.PresentationError):
            update_readme.collect_talks(self.root)

    def test_root_level_member_directory_is_ignored(self) -> None:
        root_level_directory = self.root / "xoruddl"
        root_level_directory.mkdir()
        (root_level_directory / "old-layout.md").write_text(
            "---\n"
            "round: 1\n"
            'date: "2026-09-18"\n'
            'topic: "이전 구조"\n'
            'blog: "https://example.com/old-layout"\n'
            "---\n",
            encoding="utf-8",
        )

        self.assertEqual(update_readme.collect_talks(self.root), [])


class CreateTalkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def create(self, **overrides: str) -> Path:
        values = {
            "member_id": "kkr010128",
            "round_value": "3",
            "date_value": "2026-09-12",
            "topic_value": "Spring 트랜잭션 동작 원리",
            "blog_value": "https://example.com/spring-transaction",
        }
        values.update(overrides)
        return create_talk.create_talk(self.root, **values)

    def test_form_inputs_create_valid_talk_file(self) -> None:
        destination = self.create()

        self.assertEqual(destination.parent.name, "kkr010128")
        self.assertEqual(destination.parent.parent.name, "talks")
        self.assertEqual(destination.name, "Spring-트랜잭션-동작-원리.md")
        talk = update_readme.parse_talk(destination, self.root, "kkr010128")
        self.assertEqual(talk.round, 3)
        self.assertEqual(talk.topic, "Spring 트랜잭션 동작 원리")
        self.assertEqual(talk.blog, "https://example.com/spring-transaction")

    def test_unregistered_member_is_rejected(self) -> None:
        with self.assertRaises(update_readme.PresentationError):
            self.create(member_id="outsider")

    def test_duplicate_round_is_rejected(self) -> None:
        self.create()

        with self.assertRaises(update_readme.PresentationError):
            self.create(topic_value="다른 주제")


if __name__ == "__main__":
    unittest.main()
