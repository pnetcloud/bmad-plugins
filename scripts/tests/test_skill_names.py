"""Regression coverage for group-qualified identities and migration routing."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("skill_names", ROOT / "scripts/check_skill_names.py")
names = importlib.util.module_from_spec(spec)
spec.loader.exec_module(names)


class SkillNamesTests(unittest.TestCase):
    def test_all_groups_require_prefix(self):
        for group, slug, valid in (("qa", "qa-agent-browser", True),
                                   ("pnet", "pnet-skill-improver", True),
                                   ("qa", "agent-browser", False),
                                   ("pnet", "skill-improver", False)):
            with self.subTest(group=group, slug=slug), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                plugin = root / "plugins" / group
                skill = plugin / "skills" / slug
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(f"---\nname: {slug}\n---\n")
                manifest = plugin / ".claude-plugin/plugin.json"
                manifest.parent.mkdir()
                manifest.write_text(json.dumps({"skills": [f"./skills/{slug}"]}))
                with patch.object(names, "SOURCE_ROOT", root):
                    errors = names.validate()
                self.assertEqual(not errors, valid, errors)
                if not valid:
                    self.assertTrue(any("non-canonical skill name" in error for error in errors))

    def test_migration_map_resolves_unique_manifest_entries(self):
        data = json.loads((ROOT / "docs/skill-id-migrations.json").read_text())
        self.assertFalse(data["runtime_aliases"])
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        entries = [entry.removeprefix("./") for plugin in marketplace["plugins"] for entry in plugin["skills"]]
        self.assertEqual(len(entries), len(set(entries)))
        for row in data["migrations"]:
            self.assertFalse((ROOT / row["old_path"]).exists())
            target = ROOT / row["new_path"]
            self.assertEqual(target.name, row["new_id"])
            self.assertEqual(names.read_skill_name(target / "SKILL.md"), row["new_id"])
            self.assertEqual(entries.count(row["new_path"]), 1)
            manifest = json.loads((target.parents[1] / ".claude-plugin/plugin.json").read_text())
            self.assertEqual(manifest["skills"].count("./skills/" + row["new_id"]), 1)


if __name__ == "__main__":
    unittest.main()
