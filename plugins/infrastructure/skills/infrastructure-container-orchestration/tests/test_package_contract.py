from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
COMPOSE = SKILL_DIR / "assets/docker-compose.template.yml"
DOCKERFILE = SKILL_DIR / "assets/Dockerfile.template"


class PackageContractTests(unittest.TestCase):
    def test_every_original_resource_is_retained(self) -> None:
        expected = {
            "SKILL.md",
            "assets/Dockerfile.template",
            "assets/docker-compose.template.yml",
            "references/dockerfile-patterns.md",
            "references/helm-patterns.md",
            "references/k8s-manifests.md",
            "scripts/build-push.sh",
            "skill-report.json",
        }
        for relative in expected:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_DIR / relative).is_file())

    def test_compose_preserves_services_without_secret_defaults(self) -> None:
        text = COMPOSE.read_text(encoding="utf-8")
        self.assertNotIn("\nversion:", text)
        self.assertNotIn("container_name:", text)
        self.assertNotIn("PASSWORD:-", text)
        self.assertNotIn("postgres://", text)
        for service in ("app:", "db:", "redis:"):
            self.assertIn(service, text)
        self.assertIn("database_password:", text)
        self.assertIn("POSTGRES_PASSWORD_FILE:", text)
        self.assertNotRegex(text, r'(?m)^  (db|redis):.*\n(?:.*\n)*?    ports:')

    def test_dockerfile_retains_runtime_security_contract(self) -> None:
        text = DOCKERFILE.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("\nFROM "), 2)
        self.assertIn(" AS builder", text)
        self.assertIn(" AS runtime", text)
        self.assertIn("\nUSER 10001:10001\n", text)
        self.assertIn("\nHEALTHCHECK ", text)
        self.assertIn("COPY --from=builder", text)
        self.assertNotIn(":latest", text)
        self.assertNotRegex(text, r"(?m)^(ARG|ENV) .*?(TOKEN|PASSWORD|SECRET|KEY)")

    @unittest.skipUnless(shutil.which("docker"), "docker CLI is not installed")
    def test_compose_renders_without_interpolation(self) -> None:
        result = subprocess.run(
            [
                "docker",
                "compose",
                "--file",
                str(COMPOSE),
                "config",
                "--no-interpolate",
                "--quiet",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if "is not a docker command" in result.stderr:
            self.skipTest("Docker Compose plugin is not installed")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_references_retain_all_documented_families(self) -> None:
        dockerfile = (SKILL_DIR / "references/dockerfile-patterns.md").read_text(
            encoding="utf-8"
        )
        kubernetes = (SKILL_DIR / "references/k8s-manifests.md").read_text(
            encoding="utf-8"
        )
        helm = (SKILL_DIR / "references/helm-patterns.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## Multi-Stage Builds",
            "## Layer Optimization",
            "## Security Best Practices",
            "## Health Checks",
            "## Build Arguments",
            "## Caching Strategies",
            "## Labels and Metadata",
            "## .dockerignore",
            "## Debug Container",
        ):
            self.assertIn(heading, dockerfile)
        for heading in (
            "### Namespace",
            "### ConfigMap",
            "### Secret",
            "### Deployment",
            "### Service",
            "### Ingress",
            "### HorizontalPodAutoscaler",
            "### PodDisruptionBudget",
            "### ServiceAccount and RBAC",
            "### NetworkPolicy",
            "### CronJob",
            "## kubectl Quick Reference",
        ):
            self.assertIn(heading, kubernetes)
        for heading in (
            "## Chart Structure",
            "## Chart.yaml",
            "## values.yaml",
            "## values.schema.json",
            "## Helper Template (_helpers.tpl)",
            "## ServiceAccount Template",
            "## Deployment Template",
            "## Helm Commands",
            "## Environment-Specific Values",
        ):
            self.assertIn(heading, helm)

    def test_cross_resource_examples_form_actionable_safe_paths(self) -> None:
        dockerfile = (SKILL_DIR / "references/dockerfile-patterns.md").read_text(
            encoding="utf-8"
        )
        kubernetes = (SKILL_DIR / "references/k8s-manifests.md").read_text(
            encoding="utf-8"
        )
        helm = (SKILL_DIR / "references/helm-patterns.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("secretKey: DATABASE_URL", kubernetes)
        self.assertIn("key: DATABASE_URL", kubernetes)
        self.assertIn("name: app-secrets-manual-example", kubernetes)
        self.assertIn("serviceAccountToken:", kubernetes)
        for command in (
            " get pods",
            " logs <pod>",
            " exec -it <pod> -- sh",
            " apply --server-side -f manifest.yaml",
            " rollout restart deployment/app",
            " describe pod <pod>",
            " port-forward --address localhost service/app 8080:80",
        ):
            self.assertIn(command, kubernetes)

        self.assertIn("serviceaccount.yaml", helm)
        self.assertIn("kind: ServiceAccount", helm)
        rendered_commands = helm.replace("\\\n", " ")
        for command in (
            'helm install "$release_name"',
            'helm upgrade "$release_name"',
            'helm rollback "$release_name"',
            'helm uninstall "$release_name"',
        ):
            start = rendered_commands.index(command)
            block = rendered_commands[start : start + 260]
            self.assertIn('--kube-context "$context_name"', block)
            self.assertIn('--namespace "$namespace_name"', block)
        self.assertIn(
            'helm rollback "$release_name" "$rollback_revision"',
            rendered_commands,
        )

        self.assertIn('--listen", "0.0.0.0:5678"', dockerfile)
        self.assertIn(
            "--publish 127.0.0.1:5678:5678 example-app:debug-review",
            dockerfile,
        )

    def test_historical_report_is_valid_and_explicitly_non_authoritative(self) -> None:
        report = json.loads(
            (SKILL_DIR / "skill-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual("historical-upstream-snapshot", report["meta"]["scope"])
        self.assertIn("not current operational guidance", report["meta"]["review_notice"])


if __name__ == "__main__":
    unittest.main()
