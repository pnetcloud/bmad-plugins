from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
ORIGINAL_PATHS = (
    "SKILL.md",
    "references/breakdown-examples.md",
    "references/epic-templates.md",
    "references/ticket-writing-guide.md",
)


class PackageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")

    def test_all_original_paths_are_preserved(self):
        for relative_path in ORIGINAL_PATHS:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_entrypoint_routes_every_reference_directly(self):
        for relative_path in ORIGINAL_PATHS[1:]:
            with self.subTest(relative_path=relative_path):
                self.assertIn(f"]({relative_path})", self.skill)

    def test_entrypoint_stays_within_structural_review_budget(self):
        self.assertLessEqual(len(self.skill.splitlines()), 250)
        self.assertLessEqual(len(re.findall(r"\S+", self.skill)), 2000)

    def test_modes_and_authority_gate_are_explicit(self):
        for mode in ("Draft", "Validate", "Create", "Resume", "Add to existing"):
            with self.subTest(mode=mode):
                self.assertIn(f"**{mode}**", self.skill)
        self.assertIn("obtain explicit confirmation", self.skill)
        self.assertIn("Approval covers only the displayed plan", self.skill)

    def test_draft_mode_is_read_only_and_trigger_is_narrow(self):
        draft = self.skill.split("- **Validate**", 1)[0]
        for operation in ("create", "update", "link", "transition", "delete"):
            with self.subTest(operation=operation):
                self.assertRegex(draft, rf"(?is)Do not[^.]*\b{operation}\b")
        self.assertIn("Do not use it for an isolated issue edit", self.skill)

    def test_project_contract_is_discovered_not_assumed(self):
        self.assertIn("issue types and their hierarchy levels", self.skill)
        self.assertIn("required create fields", self.skill)
        self.assertIn("An Epic or other container is optional", self.skill)
        self.assertNotIn("Epic must be created first", self.skill)

    def test_traceability_and_no_invention_contracts_exist(self):
        for phrase in (
            "Build a source ledger",
            "coverage matrix",
            "Do not invent architecture",
            "Label useful suggestions that are not source-backed as `Proposal`",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_partial_failure_and_idempotent_resume_are_covered(self):
        for phrase in (
            "run ledger",
            "do not blindly retry",
            "reconcile first",
            "failed, ambiguous, and not-attempted",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_create_approval_covers_complete_payload(self):
        preview = self.skill.split("### 5. Prove coverage", 1)[1].split(
            "### 6. Execute", 1
        )[0]
        for field in (
            "description",
            "acceptance criteria",
            "parent",
            "dependency links",
            "custom or required field name and value",
        ):
            with self.subTest(field=field):
                self.assertIn(field, preview)
        self.assertIn("exact issue-create and issue-link actions", preview)

    def test_resume_requires_unique_persisted_marker_and_fails_closed(self):
        execute = self.skill.split("### 6. Execute", 1)[1].split(
            "### 7. Complete", 1
        )[0]
        self.assertIn("unique approved run-and-item marker", execute)
        self.assertIn("cannot store and search a unique marker", execute)
        self.assertIn("automatic retry and Resume are unsafe", execute)

    def test_dependencies_are_planned_created_and_verified(self):
        self.assertIn("available issue-link types", self.skill)
        self.assertIn("create only the dependency links included", self.skill)
        self.assertIn("then re-read them", self.skill)

    def test_completion_requires_read_back_verification(self):
        self.assertIn("every reported Jira key verified by a read", self.skill)
        self.assertIn("no claim of success based only on an API request", self.skill)

    def test_original_guidance_families_remain_reachable(self):
        breakdown = (ROOT / "references/breakdown-examples.md").read_text(
            encoding="utf-8"
        )
        epics = (ROOT / "references/epic-templates.md").read_text(encoding="utf-8")
        tickets = (ROOT / "references/ticket-writing-guide.md").read_text(
            encoding="utf-8"
        )

        for family in (
            "New Feature",
            "Bug Fix",
            "Infrastructure",
            "API Development",
            "Frontend Redesign",
        ):
            with self.subTest(example_family=family):
                self.assertIn(family, breakdown)

        for family in (
            "New Feature Epic",
            "Bug Fix Epic",
            "Infrastructure/Technical Epic",
            "API Development Epic",
            "Redesign/Modernization Epic",
        ):
            with self.subTest(epic_family=family):
                self.assertIn(family, epics)

        for topic in (
            "Issue Type Selection",
            "Acceptance Criteria Best Practices",
            "Technical Notes Guidelines",
            "Descriptions by Task Type",
        ):
            with self.subTest(ticket_topic=topic):
                self.assertIn(topic, tickets)

        self.assertNotIn("Include explicit testing and documentation tasks", breakdown)
        self.assertNotIn("ensure every Epic includes", epics)
        self.assertIn("otherwise label it as a proposal", breakdown)
        self.assertIn("Keep unsupported elements", epics)


if __name__ == "__main__":
    unittest.main()
