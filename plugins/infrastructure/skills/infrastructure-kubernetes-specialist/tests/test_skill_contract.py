from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized(path: Path) -> str:
    text = path.read_text(encoding="utf-8").lower().replace("`", "")
    return " ".join(text.split())


class KubernetesSpecialistContractTests(unittest.TestCase):
    def test_frontmatter_and_precise_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: infrastructure-kubernetes-specialist\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE)
        self.assertIsNotNone(description)
        value = description.group(1).lower()
        for phrase in ("kubernetes", "gitops", "do not use", "terraform"):
            self.assertIn(phrase, value)

    def test_entrypoint_is_bounded_with_preservation_rationale(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 390)
        self.assertLessEqual(len(text.split()), 1800)
        self.assertGreaterEqual(len(text.splitlines()), 285)

    def test_all_linked_references_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        links = re.findall(r"\]\((references/[^)]+\.md)\)", text)
        self.assertEqual(
            set(links),
            {
                "references/cluster-workloads-and-upgrades.md",
                "references/security-networking-and-tenancy.md",
                "references/storage-observability-gitops-and-operations.md",
            },
        )
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_long_references_have_navigation(self):
        for path in sorted((ROOT / "references").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if len(text.splitlines()) > 100:
                self.assertIn("## Contents", text, path.name)

    def test_fictional_protocol_and_metrics_are_absent(self):
        text = normalized(SKILL)
        for phrase in (
            "query context manager",
            '"clusters_managed": 8',
            '"workloads": 347',
            '"uptime": "99.97%"',
            '"resource_efficiency": "78%"',
            "reduced resource costs by 35%",
            "cluster uptime 99.95% achieved",
            "resource utilization > 70%",
        ):
            self.assertNotIn(phrase, text)

    def test_modes_credentials_and_remote_authority_are_explicit(self):
        text = normalized(SKILL)
        for phrase in (
            "establish the mode",
            "review and design are read-only",
            "never infer a production target",
            "before running renderers",
            "remove ambient credentials unconditionally",
            "live reads can expose secrets",
            "require explicit authority",
            "emergency language does not widen authority",
        ):
            self.assertIn(phrase, text)

    def test_original_capability_families_remain_reachable(self):
        package = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(ROOT.rglob("*.md"))
        ).lower().replace("`", "")
        for phrase in (
            "control plane design",
            "etcd configuration",
            "deployment strategies",
            "statefulset management",
            "job orchestration",
            "cronjob scheduling",
            "daemonset configuration",
            "init containers",
            "sidecar patterns",
            "resource quotas",
            "pod disruption budgets",
            "horizontal pod autoscaling",
            "vertical pod autoscaling",
            "cluster autoscaling",
            "node affinity",
            "pod priority",
            "cni selection",
            "ingress controllers",
            "network policies",
            "multi-cluster networking",
            "storage classes",
            "volume snapshots",
            "csi drivers",
            "pod security standards",
            "rbac configuration",
            "admission controllers",
            "opa policies",
            "distributed tracing",
            "multi-tenancy",
            "istio implementation",
            "linkerd deployment",
            "argocd setup",
            "flux configuration",
            "helm charts",
            "kustomize overlays",
            "custom resources",
            "operator development",
            "device plugins",
            "runtime classes",
            "cluster federation",
        ):
            self.assertIn(phrase, package)

    def test_all_literal_handoffs_remain(self):
        text = normalized(SKILL)
        for phrase in (
            "support devops-engineer",
            "collaborate with cloud-architect",
            "work with security-engineer",
            "guide platform-engineer",
            "help sre-engineer",
            "assist deployment-engineer",
            "partner with network-engineer",
            "coordinate with terraform-engineer",
        ):
            self.assertIn(phrase, text)

    def test_podsecuritypolicy_is_historical_only(self):
        text = normalized(SKILL) + " " + normalized(
            ROOT / "references" / "security-networking-and-tenancy.md"
        )
        for phrase in ("removed in v1.25", "historical audit", "pod security admission"):
            self.assertIn(phrase, text)

    def test_probe_and_disruption_limits_are_explicit(self):
        text = normalized(ROOT / "references" / "cluster-workloads-and-upgrades.md")
        for phrase in (
            "readiness controls",
            "liveness can restart",
            "startup protects",
            "does not prevent all disruption",
            "direct pod or controller deletion",
            "a changed deployment condition does not alone prove",
        ):
            self.assertIn(phrase, text)

    def test_security_and_tenancy_boundaries_are_explicit(self):
        text = normalized(ROOT / "references" / "security-networking-and-tenancy.md")
        for phrase in (
            "avoid wildcards",
            "short-lived credentials",
            "base64-encoded",
            "networkpolicy object has no effect",
            "namespaces scope many objects but are not a complete security boundary",
            "exceptions need an owner",
        ):
            self.assertIn(phrase, text)

    def test_storage_gitops_and_evidence_limits_are_explicit(self):
        text = normalized(
            ROOT / "references" / "storage-observability-gitops-and-operations.md"
        )
        for phrase in (
            "not automatically an application-consistent backup",
            "restore into an authorized isolated target",
            "pulled by software agents",
            "continuously observed and reconciled",
            "a repository plus push-based deployment is ordinary ci/cd",
            "never claim completion",
        ):
            self.assertIn(phrase, text)

    def test_completion_receipt_separates_evidence_states(self):
        text = normalized(SKILL)
        for phrase in (
            "a client-side dry run is not admission proof",
            "accepted configuration is not healthy runtime behavior",
            "not validated:",
            "runtime:",
            "recovery:",
            "remaining:",
        ):
            self.assertIn(phrase, text)

    def test_scenario_vectors_have_complete_individual_contracts(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 53)
        ids = []
        expectations = set()
        for block in blocks:
            fields = dict(
                re.findall(
                    r"^    (expect|prompt|evidence): (.+)$",
                    block,
                    re.MULTILINE,
                )
            )
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE)
            self.assertIsNotNone(identifier, block)
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"}, block)
            ids.append(identifier.group(1))
            expectations.add(fields["expect"])
            self.assertGreaterEqual(len(fields["prompt"].split()), 7, block)
            self.assertGreaterEqual(len(fields["evidence"].split()), 8, block)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            expectations,
            {"trigger", "no_trigger", "safe_behavior", "bounded_behavior", "workflow"},
        )


if __name__ == "__main__":
    unittest.main()
