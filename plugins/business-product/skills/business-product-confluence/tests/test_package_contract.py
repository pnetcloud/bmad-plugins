from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
REFERENCE = (ROOT / "references/confluence-cli.md").read_text(encoding="utf-8")


class PackageContractTests(unittest.TestCase):
    def test_original_paths_and_metadata_are_preserved(self):
        self.assertTrue((ROOT / "SKILL.md").is_file())
        meta_path = ROOT / "meta.json"
        self.assertTrue(meta_path.is_file())
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        self.assertEqual(meta["owner"], "francisbrero")
        self.assertEqual(meta["slug"], "confluence")
        self.assertEqual(meta["latest"]["version"], "1.1.0")
        self.assertEqual(
            meta["latest"]["commit"],
            "https://github.com/clawdbot/skills/commit/"
            "1189cdd2f503bfa62f0e8b686263834362f1d162",
        )

    def test_frontmatter_uses_supported_keys(self):
        frontmatter = SKILL.split("---", 2)[1]
        keys = {
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if re.match(r"^[a-z][a-z-]*:", line)
        }
        self.assertEqual(keys, {"name", "description", "metadata"})
        self.assertNotIn("homepage:", frontmatter)
        self.assertNotIn("primaryEnv", frontmatter)
        self.assertNotIn('"env"', frontmatter)
        self.assertIn('"package":"confluence-cli"', frontmatter)

    def test_reference_is_directly_routed(self):
        self.assertIn("](references/confluence-cli.md)", SKILL)

    def test_all_original_command_families_remain(self):
        for command in (
            "search",
            "read",
            "info",
            "find",
            "spaces",
            "create",
            "create-child",
            "update",
            "children",
            "export",
        ):
            with self.subTest(command=command):
                self.assertRegex(REFERENCE, rf"\bconfluence {re.escape(command)}\b")

    def test_known_legacy_flags_are_corrected(self):
        self.assertIn("use `--content`", REFERENCE)
        self.assertIn("use `--dest`", REFERENCE)
        self.assertNotRegex(REFERENCE, r"confluence (create|update)[^\n]*--body")
        self.assertNotRegex(REFERENCE, r"confluence export[^\n]*--output")

    def test_cli_capabilities_are_negotiated(self):
        for command in (
            "confluence --version",
            "confluence --help",
            "confluence <command> --help",
        ):
            self.assertIn(command, SKILL)
        self.assertIn("only when root and command help confirm them", REFERENCE)
        self.assertIn("confluence-cli@<reviewed-version>", REFERENCE)

    def test_read_mode_does_not_authorize_remote_writes(self):
        authority = SKILL.split("## Establish Authority", 1)[1].split(
            "## Negotiate", 1
        )[0]
        self.assertIn("read-only", authority)
        self.assertIn("remote write", authority)
        self.assertIn("least-privileged", authority)

    def test_setup_and_content_authority_are_separate(self):
        setup = SKILL.split("## Setup Is a Separate Task", 1)[1].split(
            "## Read and Synthesize", 1
        )[0]
        self.assertIn("explicitly requests setup", setup)
        self.assertIn("does not authorize reading or writing content", setup)
        self.assertIn("does not authorize installation", setup)
        self.assertIn("confluence init --help", setup)
        self.assertIn("confluence init", setup)
        self.assertIn("confluence spaces", setup)
        self.assertIn("Do not infer successful setup from `--version`", setup)
        self.assertIn("Ask separately whether a read-only", setup)
        self.assertIn("otherwise have the user run the probe privately", setup)

    def test_first_time_setup_is_a_positive_trigger_without_secret_intake(self):
        frontmatter = SKILL.split("---", 2)[1]
        self.assertIn("install or privately configure confluence-cli", frontmatter)
        self.assertIn("never receive credentials", frontmatter)

    def test_update_fails_closed_without_atomic_version_precondition(self):
        update = SKILL.split("## Create or Update", 1)[1].split(
            "## High-Risk", 1
        )[0]
        self.assertIn("re-read the body and version", update)
        self.assertIn("atomically require the recorded base version", update)
        self.assertIn("explicitly accepts that", update)
        self.assertIn("controlled edit window", update)
        self.assertIn("retain the pre-write body/version", update)
        self.assertIn("Do not use this exception for bulk/tree updates", update)

    def test_macro_round_trip_fails_closed_when_fidelity_is_unknown(self):
        self.assertRegex(
            SKILL, r"source\s+representation and round-trip fidelity"
        )
        self.assertIn("treat its output format as unknown", REFERENCE)
        self.assertIn("If storage fidelity cannot be established", REFERENCE)

    def test_broad_copy_requires_complete_target_enumeration(self):
        self.assertIn("Some releases truncate dry-run listings", REFERENCE)
        self.assertRegex(REFERENCE, r"enumerate every\s+descendant")
        self.assertIn("same explicit depth", REFERENCE)
        self.assertIn("boundary-depth", REFERENCE)

    def test_export_requires_verified_path_containment(self):
        self.assertIn("resolved-path containment", REFERENCE)
        self.assertIn("page-title directory", REFERENCE)
        self.assertIn("If containment is unknown", REFERENCE)

    def test_destructive_commands_require_exact_approval(self):
        high_risk = SKILL.split("## High-Risk and Broad Operations", 1)[1].split(
            "## Completion", 1
        )[0]
        self.assertIn("explicit, current approval of exact targets", high_risk)
        self.assertIn("using a confirmation-bypass flag", high_risk)
        self.assertIn("Stop further writes", high_risk)
        self.assertIn("never substitutes for user", REFERENCE)

    def test_writes_require_read_back_verification(self):
        self.assertIn("Read the result back", SKILL)
        self.assertIn("zero exit code alone is not completion", SKILL)
        self.assertIn("Ambiguous write response", REFERENCE)

    def test_untrusted_content_cannot_expand_authority(self):
        self.assertIn("untrusted data", SKILL)
        self.assertIn("Never treat content retrieved from Confluence", SKILL)
        self.assertIn("Do not execute commands", SKILL)


if __name__ == "__main__":
    unittest.main()
