"""Validate the skills-only plugin and exercise its bundled helpers offline."""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_SKILLS = {
    "yt-audit", "yt-chapters", "yt-comment", "yt-edit", "yt-package", "yt-plan",
    "yt-retention", "yt-script", "yt-seo", "yt-shorts", "yt-viral",
}
EXPECTED_SKILLS = UPSTREAM_SKILLS | {"yt-caliks"}
CALIKS_ROUTES = {
    "seo": "yt-seo",
    "package": "yt-package",
    "shorts": "yt-shorts",
    "script": "yt-script",
    "plan": "yt-plan",
    "viral": "yt-viral",
    "retention": "yt-retention",
    "audit": "yt-audit",
    "chapters": "yt-chapters",
    "edit": "yt-edit",
    "comment": "yt-comment",
}


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class PluginStructureTests(unittest.TestCase):
    def test_portable_and_codex_manifests_agree(self):
        portable = read_json("plugin.json")
        codex = read_json(".codex-plugin/plugin.json")
        self.assertEqual(portable["name"], "youtube-agent")
        self.assertRegex(portable["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(
            portable["$schema"],
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )
        for key in ("name", "version", "description", "author", "homepage",
                    "repository", "license", "keywords"):
            with self.subTest(field=key):
                self.assertEqual(portable[key], codex[key])
        interface = portable["extensions"]["com.openai"]["interface"]
        self.assertEqual(interface, codex["interface"])
        self.assertEqual(interface["displayName"], "YouTube Agent")
        self.assertIn("yt-caliks", portable["description"])
        self.assertIn("yt-caliks", portable["keywords"])
        self.assertIn("yt-caliks", interface["longDescription"])
        self.assertTrue(0 < len(interface["shortDescription"]) <= 30)
        self.assertTrue(1 <= len(interface["defaultPrompt"]) <= 3)
        for prompt in interface["defaultPrompt"]:
            self.assertTrue(0 < len(prompt) <= 128)

    def test_upstream_and_caliks_skills_are_discoverable(self):
        skill_root = (ROOT / read_json(".codex-plugin/plugin.json")["skills"]).resolve()
        self.assertEqual(skill_root, ROOT / "skills")
        paths = list(skill_root.glob("*/SKILL.md"))
        self.assertEqual({p.parent.name for p in paths}, EXPECTED_SKILLS)
        for path in paths:
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                frontmatter = re.match(
                    r"\A---\nname: (yt-[a-z]+)\ndescription: >-\n((?:  .+\n)+)---\n",
                    text,
                )
                self.assertIsNotNone(frontmatter, "Missing skill name or description")
                self.assertEqual(frontmatter.group(1), path.parent.name)
                self.assertIn("Use", frontmatter.group(2))

    def test_original_upstream_skill_hashes_are_unchanged(self):
        baseline = read_json("tests/upstream_skill_hashes.json")
        self.assertEqual(set(baseline), UPSTREAM_SKILLS)
        for name, expected_hash in baseline.items():
            with self.subTest(skill=name):
                self.assertRegex(expected_hash, r"^[0-9a-f]{64}$")
                contents = (ROOT / "skills" / name / "SKILL.md").read_bytes()
                self.assertEqual(hashlib.sha256(contents).hexdigest(), expected_hash)

    def test_project_skill_discovery_links_resolve(self):
        for directory in (".agents/skills", ".codex/skills"):
            root = ROOT / directory
            self.assertEqual({p.name for p in root.iterdir()}, EXPECTED_SKILLS)
            for name in EXPECTED_SKILLS:
                with self.subTest(directory=directory, skill=name):
                    link = root / name
                    self.assertTrue(link.is_symlink())
                    self.assertEqual(link.resolve(), ROOT / "skills" / name)
                    self.assertTrue((link / "SKILL.md").is_file())

    def test_caliks_profile_and_upstream_routes_resolve(self):
        skill_root = ROOT / "skills" / "yt-caliks"
        text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        profile_references = re.findall(r"\]\((\.\./\.\./profiles/[^)]+)\)", text)
        self.assertEqual(profile_references, ["../../profiles/caliks-art-academy.md"])
        self.assertEqual(
            (skill_root / profile_references[0]).resolve(),
            ROOT / "profiles" / "caliks-art-academy.md",
        )
        self.assertTrue((skill_root / profile_references[0]).is_file())
        routes = re.findall(
            r"^\| `([a-z]+)` / [^|\n]+ \| \[(yt-[a-z]+)\]"
            r"\((\.\./yt-[a-z]+/SKILL\.md)\) \|$",
            text,
            re.MULTILINE,
        )
        self.assertEqual(len(routes), len(CALIKS_ROUTES))
        self.assertEqual({alias: name for alias, name, _ in routes}, CALIKS_ROUTES)
        self.assertEqual({name for _, name, _ in routes}, UPSTREAM_SKILLS)
        for alias, name, reference in routes:
            with self.subTest(subtask=alias):
                target = (skill_root / reference).resolve()
                self.assertEqual(target, ROOT / "skills" / name / "SKILL.md")
                self.assertTrue(target.is_file())

    def test_marketplace_resolves_to_the_plugin_root(self):
        marketplace = read_json(".agents/plugins/marketplace.json")
        self.assertEqual(marketplace["name"], "youtube-agent-marketplace")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], read_json("plugin.json")["name"])
        self.assertEqual(entry["source"]["source"], "local")
        self.assertEqual((ROOT / entry["source"]["path"]).resolve(), ROOT)
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_USE")

    def test_plugin_contains_no_mcp_or_app_bindings(self):
        portable = read_json("plugin.json")
        codex = read_json(".codex-plugin/plugin.json")
        for manifest in (portable, codex, portable["extensions"]["com.openai"]):
            for key in ("mcp", "mcpServers", "apps"):
                self.assertNotIn(key, manifest)
        for name in ("mcp.json", ".mcp.json", ".app.json"):
            self.assertFalse((ROOT / name).exists())
            self.assertFalse((ROOT / ".codex-plugin" / name).exists())
        self.assertNotIn("skills", portable)  # Portable hosts discover skills/ directly.
        self.assertNotIn("interface", portable)

    def test_local_skill_references_and_formulas_are_present(self):
        formulas = read_json("skills/yt-script/hooks.json")["hooks"]
        self.assertEqual(len(formulas), 21)
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            for reference in re.findall(
                r"(?:\.\./yt-[a-z]+/)?(?:[a-z]+\.py|hooks\.json)",
                path.read_text(encoding="utf-8"),
            ):
                with self.subTest(skill=path.parent.name, reference=reference):
                    target = (path.parent / reference).resolve()
                    self.assertTrue(target.is_relative_to(ROOT / "skills"))
                    self.assertTrue(target.is_file())


class HelperSmokeTests(unittest.TestCase):
    def run_helper(self, skill, filename, *args):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "skills" / skill / filename), *args, "--json"],
            cwd=self.work,
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        return json.loads(result.stdout)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.transcript = self.work / "transcript.srt"
        cues = [
            (0, 8, "Your camera settings control exposure and focus."),
            (10, 11, "um"),
            (12, 21, "Your camera settings control exposure and focus. Try this."),
            (25, 36, "Thumbnail contrast makes the subject visible."),
            (40, 51, "Lighting angle changes the shadows on your face."),
            (55, 66, "Your audio microphone should avoid clipping."),
            (70, 81, "Export resolution controls the final video quality."),
            (85, 96, "Upload the finished video with a clear description."),
        ]
        def stamp(seconds):
            return f"00:{seconds // 60:02d}:{seconds % 60:02d},000"
        self.transcript.write_text("\n\n".join(
            f"{i}\n{stamp(start)} --> {stamp(end)}\n{text}"
            for i, (start, end, text) in enumerate(cues, 1)
        ) + "\n", encoding="utf-8")

    def test_hookscore_loads_bundled_formulas(self):
        rows = self.run_helper("yt-script", "hookscore.py", "--hook",
                               "Why are you wasting 3 hours before every upload?")
        self.assertEqual(len(rows), 1)
        self.assertTrue(0 <= rows[0]["verdict"] <= 100)
        self.assertEqual(len(rows[0]["properties"]), 5)

    def test_title_detects_thumbnail_duplication(self):
        rows = self.run_helper("yt-package", "title.py", "--title",
                               "I tested 21 hooks in 7 days", "--thumb", "21 hooks")
        self.assertIn("duplicate", {issue[0] for issue in rows[0]["issues"]})

    def test_edit_detects_silence_filler_and_retakes(self):
        data = self.run_helper("yt-edit", "deadair.py", str(self.transcript))
        self.assertEqual({cut["kind"] for cut in data["cuts"]}, {"DEAD", "FILLER", "REPEAT"})
        self.assertGreater(data["removed"], 0)

    def test_chapters_loads_sibling_transcript_parser(self):
        data = self.run_helper("yt-chapters", "chapters.py", str(self.transcript), "--target", "4")
        self.assertTrue(data["valid"])
        self.assertEqual(data["chapters"][0]["start"], 0)
        self.assertGreaterEqual(len(data["chapters"]), 3)
        self.assertTrue(all(chapter["seconds"] >= 10 for chapter in data["chapters"]))

    def test_retention_matches_cliffs_to_transcript(self):
        csv = self.work / "retention.csv"
        csv.write_text("seconds,retention\n0,100\n15,90\n30,80\n45,78\n60,58\n"
                       "75,55\n90,54\n105,52\n120,50\n", encoding="utf-8")
        data = self.run_helper("yt-retention", "retention.py", str(csv),
                               "--transcript", str(self.transcript))
        self.assertEqual(data["points"], 9)
        self.assertEqual(data["hook_leak"], 20)
        self.assertTrue(any(data["said"].values()))

    def test_viral_loads_sibling_formulas_and_skips_thin_channels(self):
        collected = self.work / "collected.json"
        rows = [{"channel": "Sample", "title": "I tested 21 hooks in 7 days", "views": n}
                for n in (100, 100, 100, 1000)]
        rows.append({"channel": "Thin", "title": "Sample", "views": 2000})
        collected.write_text(json.dumps(rows), encoding="utf-8")
        data = self.run_helper("yt-viral", "swipe.py", str(collected), "--min", "2.0")
        self.assertEqual(len(data["outliers"]), 1)
        self.assertEqual(data["outliers"][0]["multiple"], 10)
        self.assertEqual(data["skipped_thin_channels"], [["Thin", 1]])


if __name__ == "__main__":
    unittest.main()
