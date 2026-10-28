from __future__ import annotations

import hashlib
import importlib.util
import json
import struct
import sys
import zlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "scan_skill.py"
SPEC = importlib.util.spec_from_file_location("scan_skill", SCRIPT)
assert SPEC and SPEC.loader
scan_skill = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scan_skill
SPEC.loader.exec_module(scan_skill)


def write_skill(root: Path, name: str = "demo-skill", body: str = "# Demo\n") -> Path:
    skill = root / name
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        "description: Improve a demo. Use when testing the scanner.\n"
        "---\n\n"
        f"{body}",
        encoding="utf-8",
    )
    return skill


def write_public_policy(
    root: Path,
    *,
    forbidden_literals: list[str] | None = None,
    forbidden_regexes: list[str] | None = None,
    allowed_environment_variables: list[str] | None = None,
) -> tuple[Path, scan_skill.PublicPolicy]:
    path = root / "public-policy.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "forbidden_literals": forbidden_literals or ["Private Product"],
                "forbidden_regexes": forbidden_regexes or [],
                "forbidden_domains": ["private.example"],
                "allowed_environment_variables": (
                    allowed_environment_variables or ["PATH"]
                ),
                "allowed_email_domains": ["example.com"],
            }
        ),
        encoding="utf-8",
    )
    findings: list[scan_skill.Finding] = []
    policy = scan_skill.load_public_policy(path, findings)
    if findings or policy is None:
        raise AssertionError(findings)
    return path, policy


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload)))


def make_png(*, width: int = 1, height: int = 1, raw: bytes = b"\0\xff\0\0",
             compressed: bytes | None = None, extra: bytes = b"") -> bytes:
    return (b"\x89PNG\r\n\x1a\n"
            + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + extra
            + png_chunk(b"IDAT", zlib.compress(raw) if compressed is None else compressed)
            + png_chunk(b"IEND", b""))


def asset_descriptor(data: bytes, **overrides) -> dict:
    return {"skill": "demo-skill", "path": "assets/icon.png",
            "sha256": hashlib.sha256(data).hexdigest(), "size": len(data),
            "format": "png", **overrides}


def asset_policy(root: Path, entries) -> tuple[scan_skill.PublicPolicy | None, list]:
    path, _ = write_public_policy(root)
    data = json.loads(path.read_text())
    data["reviewed_assets"] = entries
    path.write_text(json.dumps(data), encoding="utf-8")
    findings = []
    return scan_skill.load_public_policy(path, findings), findings


class ScanSkillTests(unittest.TestCase):
    def test_valid_skill_has_no_blocking_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory))
            findings = scan_skill.scan_skill(skill)
            self.assertFalse([item for item in findings if item.severity == "blocking"])

    def test_frontmatter_name_must_match_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory))
            content = (skill / "SKILL.md").read_text(encoding="utf-8")
            (skill / "SKILL.md").write_text(
                content.replace("name: demo-skill", "name: another-skill"),
                encoding="utf-8",
            )
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("name-directory-mismatch", codes)

    def test_missing_reference_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body="# Demo\nRead [missing](references/missing.md).\n",
            )
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("reference-missing", codes)

    def test_hidden_unicode_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory), body="# Demo\nsafe\u202etext\n")
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("hidden-unicode", codes)

    def test_symlink_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = write_skill(root)
            outside = root / "outside.txt"
            outside.write_text("data", encoding="utf-8")
            (skill / "linked.txt").symlink_to(outside)
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("symlink", codes)

    def test_dangerous_command_is_warning_not_automatic_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body=(
                    "# Demo\n"
                    "Run `rm -fr output` or `rm --force --recursive cache`.\n"
                ),
            )
            findings = scan_skill.scan_skill(skill)
            destructive = [item for item in findings if item.code == "destructive-command"]
            self.assertTrue(destructive)
            self.assertTrue(all(item.severity == "warning" for item in destructive))

    def test_multiline_pipe_to_shell_is_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body="# Demo\n```sh\ncurl https://example.test/install \\\n  | bash\n```\n",
            )
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("pipe-to-shell", codes)

    def test_binary_or_oversized_file_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory))
            (skill / "payload.bin").write_bytes(b"\0payload")
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("opaque-or-oversized-file", codes)

            (skill / "payload.bin").unlink()
            with mock.patch.object(scan_skill, "MAX_TEXT_BYTES", 8):
                codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("opaque-or-oversized-file", codes)

    def test_skipped_directory_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory))
            (skill / "node_modules").mkdir()
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("skipped-directory", codes)

    def test_skipped_directory_is_blocking_for_public_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(root)
            (skill / "node_modules").mkdir()
            findings = scan_skill.scan_skill(skill, policy)
            public_skips = [
                item
                for item in findings
                if item.code == "public-unscanned-directory"
            ]
            self.assertTrue(public_skips)
            self.assertTrue(all(item.severity == "blocking" for item in public_skips))

    def test_inline_link_title_and_reference_link_are_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body=(
                    "# Demo\n"
                    "Read [guide](references/guide.md \"Guide\") and [notes][notes].\n\n"
                    "[notes]: references/notes.md \"Notes\"\n"
                ),
            )
            references = skill / "references"
            references.mkdir()
            (references / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (references / "notes.md").write_text("# Notes\n", encoding="utf-8")
            findings = scan_skill.scan_skill(skill)
            self.assertFalse([item for item in findings if item.severity == "blocking"])

    def test_missing_reference_definition_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body="# Demo\nRead [missing][unknown].\n",
            )
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertIn("reference-definition-missing", codes)

    def test_links_and_json_access_inside_fenced_code_are_not_references(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body=(
                    "# Demo\n"
                    "```json\n"
                    '{"value": "items[0][\\"content\\"]"}\n'
                    "```\n"
                    "```markdown\n"
                    "[Example title](placeholder-link)\n"
                    "```\n"
                    "~~~markdown\n"
                    "[Another title](another-placeholder)\n"
                    "~~~\n"
                ),
            )
            codes = {item.code for item in scan_skill.scan_skill(skill)}
            self.assertNotIn("reference-definition-missing", codes)
            self.assertNotIn("reference-missing", codes)

    def test_links_in_reference_markdown_are_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory))
            references = skill / "references"
            references.mkdir()
            (references / "notes.md").write_text(
                "Read [missing](missing.md).\n",
                encoding="utf-8",
            )
            findings = scan_skill.scan_skill(skill)
            missing = [item for item in findings if item.code == "reference-missing"]
            self.assertTrue(missing)
            self.assertEqual(missing[0].path, "references/notes.md")

    def test_crlf_frontmatter_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "demo-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_bytes(
                b"---\r\n"
                b"name: demo-skill\r\n"
                b"description: Improve a demo. Use when testing the scanner.\r\n"
                b"---\r\n\r\n# Demo\r\n"
            )
            findings = scan_skill.scan_skill(skill)
            self.assertFalse([item for item in findings if item.severity == "blocking"])

    def test_target_directory_symlink_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = write_skill(root)
            linked_skill = root / "linked-skill"
            linked_skill.symlink_to(skill, target_is_directory=True)
            codes = {item.code for item in scan_skill.scan_skill(linked_skill)}
            self.assertIn("target-symlink", codes)

    def test_entrypoint_length_budgets_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review_skill = write_skill(
                root,
                name="review-skill",
                body="# Demo\n" + ("detail\n" * 250),
            )
            review_codes = {item.code for item in scan_skill.scan_skill(review_skill)}
            self.assertIn("skill-entrypoint-large", review_codes)
            self.assertNotIn("skill-entrypoint-over-limit", review_codes)

            limit_skill = write_skill(
                root,
                name="limit-skill",
                body="# Demo\n" + ("detail\n" * 500),
            )
            limit_findings = scan_skill.scan_skill(limit_skill)
            over_limit = [
                item for item in limit_findings
                if item.code == "skill-entrypoint-over-limit"
            ]
            self.assertTrue(over_limit)
            self.assertTrue(all(item.severity == "warning" for item in over_limit))

    def test_dense_entrypoint_and_long_description_are_warnings(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(
                Path(directory),
                body="# Demo\n" + ("word " * 1500) + "\n",
            )
            content = (skill / "SKILL.md").read_text(encoding="utf-8")
            (skill / "SKILL.md").write_text(
                content.replace(
                    "Improve a demo. Use when testing the scanner.",
                    ("D " * 501).strip(),
                ),
                encoding="utf-8",
            )
            findings = scan_skill.scan_skill(skill)
            warning_codes = {
                item.code for item in findings if item.severity == "warning"
            }
            self.assertIn("description-long", warning_codes)
            self.assertIn("skill-entrypoint-wordy", warning_codes)

    def test_public_policy_must_be_valid_and_nonempty(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "public-policy.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "forbidden_literals": [],
                        "forbidden_regexes": [],
                        "forbidden_domains": [],
                        "allowed_environment_variables": [],
                        "allowed_email_domains": [],
                    }
                ),
                encoding="utf-8",
            )
            findings: list[scan_skill.Finding] = []
            policy = scan_skill.load_public_policy(path, findings)
            self.assertIsNone(policy)
            self.assertIn("public-policy-empty", {item.code for item in findings})

    def test_missing_public_policy_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            findings: list[scan_skill.Finding] = []
            policy = scan_skill.load_public_policy(
                Path(directory) / "missing-policy.json",
                findings,
            )
            self.assertIsNone(policy)
            self.assertIn(
                "public-policy-unreadable",
                {item.code for item in findings},
            )

    def test_public_policy_terms_are_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(
                root,
                forbidden_literals=["Private Product"],
                forbidden_regexes=[r"\binternal-topic-[0-9]+\b"],
            )
            skill = write_skill(
                root,
                body="# Demo\nPrivate Product uses internal-topic-42.\n",
            )
            findings = scan_skill.scan_skill(skill, policy)
            blocking_codes = {
                item.code for item in findings if item.severity == "blocking"
            }
            self.assertIn("public-private-term", blocking_codes)
            self.assertIn("public-private-pattern", blocking_codes)
            self.assertFalse(
                [
                    item
                    for item in findings
                    if "Private Product" in item.message
                    or "internal-topic-42" in item.message
                ]
            )

    def test_public_secret_patterns_are_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            token = "gh" + "p_" + ("a" * 40)
            password_assignment = "pass" + "word=real-password-value"
            scheme = "post" + "gresql"
            credential_url = scheme + "://" + "user:real-password@" + "db.example/db"
            skill = write_skill(
                root,
                body=(
                    "# Demo\n"
                    f"credential = {token}\n"
                    f"{password_assignment}\n"
                    f"database = {credential_url}\n"
                ),
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertIn("public-provider-token", codes)
            self.assertIn("public-secret-assignment", codes)
            self.assertIn("public-credential-url", codes)

    def test_public_private_key_and_jwt_are_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            private_key = "-----BEGIN " + "PRIVATE KEY-----"
            jwt = (
                "eyJ"
                + ("a" * 10)
                + ".eyJ"
                + ("b" * 10)
                + "."
                + ("c" * 10)
            )
            skill = write_skill(
                root,
                body=f"# Demo\n{private_key}\n{jwt}\n",
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertIn("public-private-key", codes)
            self.assertIn("public-jwt", codes)

    def test_public_secret_placeholders_are_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(
                root,
                body="# Demo\npassword=<PASSWORD>\napi_key=YOUR_API_KEY\n",
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertNotIn("public-secret-assignment", codes)

    def test_public_environment_variables_require_allowlist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(
                root,
                allowed_environment_variables=["PATH"],
            )
            private_reference = "$" + "PRIVATE_PRODUCT_TOKEN"
            skill = write_skill(
                root,
                body=f"# Demo\nUse $PATH, then read {private_reference}.\n",
            )
            findings = scan_skill.scan_skill(skill, policy)
            environment = [
                item
                for item in findings
                if item.code == "public-environment-variable"
            ]
            self.assertEqual(len(environment), 1)
            self.assertTrue(all(item.severity == "blocking" for item in environment))

    def test_public_bare_environment_assignment_requires_allowlist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(
                root,
                allowed_environment_variables=["PATH"],
            )
            skill = write_skill(
                root,
                body="# Demo\nPRIVATE_SETTING=value\nPATH=/bin\n",
            )
            environment = [
                item
                for item in scan_skill.scan_skill(skill, policy)
                if item.code == "public-environment-variable"
            ]
            self.assertEqual(len(environment), 1)
            self.assertTrue(all(item.severity == "blocking" for item in environment))

    def test_public_private_paths_hosts_and_email_are_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            private_path = "/home/" + "developer/private/source"
            private_host = "service" + ".internal"
            private_address = "10" + ".20.30.40"
            private_email = "engineer@" + "private.company"
            skill = write_skill(
                root,
                body=(
                    "# Demo\n"
                    f"Read {private_path}.\n"
                    f"Call https://{private_host}/api and "
                    f"http://{private_address}/data.\n"
                    f"Contact {private_email}.\n"
                ),
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertIn("public-private-path", codes)
            self.assertIn("public-private-host", codes)
            self.assertIn("public-private-address", codes)
            self.assertIn("public-email", codes)

    def test_public_reserved_example_address_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(
                root,
                body="# Demo\nUse 192.0.2.10 as documentation-only example data.\n",
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertNotIn("public-private-address", codes)

    def test_public_unspecified_bind_address_is_not_private_architecture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(
                root,
                body=(
                    "# Demo\n"
                    "A container process binds to 0.0.0.0 inside its network "
                    "namespace.\n"
                ),
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertNotIn("public-private-address", codes)

    def test_public_malformed_url_is_blocking_not_a_crash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            malformed_url = "https:" + "//[broken.example/path"
            skill = write_skill(
                root,
                body=f"# Demo\nRead {malformed_url}.\n",
            )
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertIn("public-malformed-url", codes)

    def test_public_sensitive_package_file_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(root)
            (skill / (".en" + "v")).write_text("VALUE=example\n", encoding="utf-8")
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertIn("public-sensitive-file", codes)

    def test_public_non_ascii_package_path_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(root)
            confusable_name = "guide.md" + "\N{CYRILLIC SMALL LETTER ES}"
            (skill / confusable_name).write_text("# Guide\n", encoding="utf-8")
            codes = {
                item.code
                for item in scan_skill.scan_skill(skill, policy)
                if item.severity == "blocking"
            }
            self.assertIn("public-non-ascii-path", codes)

    def test_clean_public_skill_passes_public_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(
                root,
                body=(
                    "# Demo\n"
                    "Use documented public APIs and placeholder credentials only.\n"
                    "Read https://docs.github.com/ for provider guidance.\n"
                    "Contact docs@example.com for this fictional example.\n"
                ),
            )
            findings = scan_skill.scan_skill(skill, policy)
            self.assertFalse(
                [item for item in findings if item.severity == "blocking"]
            )


    def test_inline_code_spans_ignore_json_and_links_with_variable_delimiters(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory), body=(
                '# Demo\n`result["reshare"]["id"]` and `` ` [x][absent] ``.\n'
                'Text ```inline [x](missing.md) `` nested ``` and [real][ok].\n'
                '`multiline\n[x](missing.md)`\n\n[ok]: SKILL.md\n'
            ))
            self.assertFalse([f for f in scan_skill.scan_skill(skill) if f.severity == "blocking"])

    def test_inline_mask_does_not_hide_real_or_unmatched_links(self):
        bodies = [
            '`[fake][none]` [real](missing.md)\n[real][unknown]\n',
            '`unclosed [real](missing.md)\n[real][unknown]\n',
            r'\`escaped [real](missing.md) [real][unknown]' + '\n',
            '`one\n\n[real](missing.md) [real][unknown] `\n',
        ]
        for body in bodies:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as directory:
                skill = write_skill(Path(directory), body="# Demo\n" + body)
                findings = scan_skill.scan_skill(skill)
                codes = {f.code for f in findings}
                self.assertIn("reference-missing", codes)
                self.assertIn("reference-definition-missing", codes)

    def test_inline_mask_keeps_offsets_and_backslash_closing_rules(self):
        text = 'before ``a ` [x][y]\n b`` after\n'
        masked = scan_skill.mask_inline_code(text)
        self.assertEqual(len(text), len(masked))
        self.assertEqual([i for i, c in enumerate(text) if c == '\n'],
                         [i for i, c in enumerate(masked) if c == '\n'])
        self.assertNotIn('[x]', masked)
        self.assertEqual(scan_skill.mask_inline_code('`a\\` [x][y]'), '     [x][y]')
        with tempfile.TemporaryDirectory() as directory:
            skill = write_skill(Path(directory), body='`[x][y]`\n[bad](missing.md)\n')
            self.assertEqual(next(f.line for f in scan_skill.scan_skill(skill)
                                  if f.code == "reference-missing"), 7)

    def test_inline_code_still_scans_secrets_private_terms_and_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            token = 'gh' + 'p_' + 'a' * 40
            private_path = '/home/' + 'developer/source'
            environment = '$' + 'UNAPPROVED_VARIABLE'
            skill = write_skill(root, body=(
                f'`{token} Private Product {environment} {private_path}`\n'
                '``[x][y]``\n'
            ))
            codes = {f.code for f in scan_skill.scan_skill(skill, policy)}
            self.assertTrue({'public-provider-token', 'public-private-term',
                             'public-environment-variable', 'public-private-path'} <= codes)
            self.assertNotIn('reference-definition-missing', codes)

    def test_exact_reviewed_png_emits_explicit_evidence_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_png()
            skill = write_skill(root)
            (skill / 'assets').mkdir()
            (skill / 'assets/icon.png').write_bytes(data)
            policy, errors = asset_policy(root, [asset_descriptor(data)])
            self.assertFalse(errors)
            findings = scan_skill.scan_skill(skill, policy)
            self.assertFalse([f for f in findings if f.severity == 'blocking'])
            approval = next(f for f in findings if f.code == 'public-reviewed-asset')
            self.assertEqual(approval.severity, 'warning')
            for evidence in (hashlib.sha256(data).hexdigest(), f'size={len(data)}',
                             'dimensions=1x1', 'skill=demo-skill', 'path=assets/icon.png'):
                self.assertIn(evidence, approval.message)

    def test_png_default_and_unrelated_binary_remain_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = write_skill(root)
            (skill / 'assets').mkdir()
            data = make_png()
            (skill / 'assets/icon.png').write_bytes(data)
            _, default_policy = write_public_policy(root)
            for policy in (None, default_policy):
                self.assertIn('opaque-or-oversized-file',
                              {f.code for f in scan_skill.scan_skill(skill, policy)})
            policy, _ = asset_policy(root, [asset_descriptor(data)])
            (skill / 'other.bin').write_bytes(b'\0unreviewed')
            findings = scan_skill.scan_skill(skill, policy)
            self.assertTrue(any(f.path == 'other.bin' and f.severity == 'blocking'
                                for f in findings))

    def test_reviewed_png_exact_identity_mismatches_fail_closed(self):
        data = make_png()
        changes = [{'sha256': '0' * 64}, {'size': len(data) + 1},
                   {'skill': 'other-skill'}, {'path': 'assets/other.png'}]
        for change in changes:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                skill = write_skill(root)
                (skill / 'assets').mkdir()
                (skill / 'assets/icon.png').write_bytes(data)
                policy, errors = asset_policy(root, [asset_descriptor(data, **change)])
                self.assertFalse(errors)
                findings = scan_skill.scan_skill(skill, policy)
                self.assertTrue(any(f.severity == 'blocking' for f in findings))
                self.assertNotIn('public-reviewed-asset', {f.code for f in findings})

    def test_reviewed_asset_descriptors_are_strictly_typed_and_safe(self):
        data = make_png()
        changes = [
            {'skill': '../demo-skill'}, {'skill': ''}, {'skill': 1},
            {'path': '/icon.png'}, {'path': '../icon.png'},
            {'path': 'assets/../icon.png'}, {'path': './icon.png'},
            {'path': 'assets//icon.png'}, {'path': 'C:\\icon.png'},
            {'path': 'assets/icon.jpg'}, {'path': 'assets/icon.PNG'},
            {'path': 'assets/\u202eicon.png'}, {'path': 1},
            {'sha256': 'g' * 64}, {'sha256': 'a' * 63}, {'sha256': 1},
            {'size': True}, {'size': 1.0}, {'size': '69'}, {'size': 0},
            {'size': -1}, {'size': scan_skill.MAX_TEXT_BYTES + 1},
            {'format': 'jpeg'}, {'format': 1}, {'extra': 'unknown'},
        ]
        entries = [asset_descriptor(data, **c) for c in changes]
        missing = asset_descriptor(data)
        del missing['sha256']
        for value in (None, {}, 'png', [None], [missing], *[[e] for e in entries],
                      [asset_descriptor(data)] * 2):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                policy, errors = asset_policy(Path(directory), value)
                self.assertIsNone(policy)
                self.assertIn('public-policy-invalid', {f.code for f in errors})

    def test_asset_approval_cannot_replace_required_nonempty_private_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = write_public_policy(root)
            data = json.loads(path.read_text())
            data.update(forbidden_literals=[], forbidden_regexes=[],
                        reviewed_assets=[asset_descriptor(make_png())])
            path.write_text(json.dumps(data))
            findings = []
            self.assertIsNone(scan_skill.load_public_policy(path, findings))
            self.assertIn('public-policy-empty', {f.code for f in findings})

    def test_reviewed_png_symlinks_and_path_policy_still_block(self):
        for linked_directory in (False, True):
            with self.subTest(linked_directory=linked_directory), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                skill = write_skill(root)
                outside = root / 'outside'
                outside.mkdir()
                data = make_png()
                (outside / 'icon.png').write_bytes(data)
                if linked_directory:
                    (skill / 'assets').symlink_to(outside, target_is_directory=True)
                else:
                    (skill / 'assets').mkdir()
                    (skill / 'assets/icon.png').symlink_to(outside / 'icon.png')
                policy, _ = asset_policy(root, [asset_descriptor(data)])
                findings = scan_skill.scan_skill(skill, policy)
                self.assertIn('symlink', {f.code for f in findings})
                self.assertNotIn('public-reviewed-asset', {f.code for f in findings})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = write_skill(root)
            (skill / 'assets').mkdir()
            data = make_png()
            (skill / 'assets/icon.png').write_bytes(data)
            policy, _ = asset_policy(root, [asset_descriptor(data)])
            from dataclasses import replace
            policy = replace(policy, forbidden_literals=('assets/icon.png',))
            self.assertIn('public-private-term',
                          {f.code for f in scan_skill.scan_skill(skill, policy)})

    def test_exact_hash_cannot_approve_malformed_or_out_of_bounds_png(self):
        valid = make_png()
        bad_crc = bytearray(valid)
        bad_crc[29] ^= 1
        payloads = [
            b'not a PNG', valid[:-1], bytes(bad_crc), valid + b'trailing payload',
            valid[:-12], b'\x89PNG\r\n\x1a\n' + png_chunk(b'IEND', b''),
            make_png(width=0), make_png(height=0), make_png(width=4097),
            make_png(width=4096, height=4096),
            make_png(raw=b'\0'), make_png(raw=b'\x05\xff\0\0'),
            make_png(compressed=b'invalid zlib'),
            make_png(compressed=zlib.compress(b'\0\xff\0\0') + b'payload'),
            make_png(raw=b'\0' * 100000),
            make_png(extra=png_chunk(b'IHDR', b'\0' * 13)),
            make_png(extra=png_chunk(b'CRIT', b'')),
            make_png(extra=png_chunk(b'acTL', struct.pack('>II', 1, 0))),
            valid[:8] + b'\xff\xff\xff\xffIDAT',
        ]
        for data in payloads:
            with self.subTest(data=data[:40]), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                skill = write_skill(root)
                (skill / 'assets').mkdir()
                (skill / 'assets/icon.png').write_bytes(data)
                policy, errors = asset_policy(root, [asset_descriptor(data)])
                self.assertFalse(errors)
                findings = scan_skill.scan_skill(skill, policy)
                self.assertIn('public-reviewed-asset-invalid', {f.code for f in findings})
                self.assertNotIn('public-reviewed-asset', {f.code for f in findings})

    def test_png_approval_does_not_suppress_other_text_or_self_authorize(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_png()
            descriptor = asset_descriptor(data)
            environment = '$' + 'UNAPPROVED_VARIABLE'
            skill = write_skill(root, body=f'# Demo\n`{environment}`\n'
                                + json.dumps({'reviewed_assets': [descriptor]}) + '\n')
            (skill / 'assets').mkdir()
            (skill / 'assets/icon.png').write_bytes(data)
            _, default = write_public_policy(root)
            self.assertIn('opaque-or-oversized-file',
                          {f.code for f in scan_skill.scan_skill(skill, default)})
            policy, _ = asset_policy(root, [descriptor])
            codes = {f.code for f in scan_skill.scan_skill(skill, policy)}
            self.assertIn('public-environment-variable', codes)
            self.assertIn('public-reviewed-asset', codes)


    def test_exact_email_allowlist_does_not_grant_same_domain_or_substring(self):
        from dataclasses import replace
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = write_public_policy(root)
            data = json.loads(path.read_text())
            data['allowed_email_domains'] = []
            data['allowed_email_addresses'] = ['author@example.com']
            path.write_text(json.dumps(data))
            errors = []
            policy = scan_skill.load_public_policy(path, errors)
            self.assertFalse(errors)
            skill = write_skill(root, body=(
                '# Demo\nauthor@example.com\nother@example.com\n'
                'prefixauthor@example.com\nauthor@sub.example.com\nAuthor@example.com\n'
            ))
            # Reserved example domains are normally allowed; disable only that
            # independent exemption to test exact mailbox grants using safe fixtures.
            with mock.patch.object(scan_skill, 'is_reserved_example_domain', return_value=False):
                findings = scan_skill.scan_skill(skill, policy)
                emails = [f for f in findings if f.code == 'public-email']
                self.assertEqual([f.line for f in emails], [8, 9, 10, 11])
                findings = scan_skill.scan_skill(skill, replace(policy, allowed_email_addresses=frozenset()))
                self.assertEqual(sum(f.code == 'public-email' for f in findings), 5)
                # Existing domain + subdomain behavior is retained independently.
                findings = scan_skill.scan_skill(skill, replace(policy, allowed_email_domains=frozenset({'example.com'})))
                self.assertNotIn('public-email', {f.code for f in findings})

    def test_optional_email_addresses_default_empty_and_invalid_fields_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, policy = write_public_policy(root)
            self.assertEqual(policy.allowed_email_addresses, frozenset())
            baseline = json.loads(path.read_text())
            for value in ([], ['author@example.com']):
                path.write_text(json.dumps({**baseline, 'allowed_email_addresses': value}))
                findings = []
                self.assertIsNotNone(scan_skill.load_public_policy(path, findings))
                self.assertFalse(findings)
            for value in (None, {}, 'author@example.com', [1], [True], [''],
                          [' author@example.com'], ['author@example.com '],
                          ['Author <author@example.com>'], ['*@example.com'],
                          ['author@' + '-example.com'], ['author@' + 'example..com'],
                          ['author@' + 'a' * 64 + '.com'],
                          ['.author@example.com'], ['author..name@example.com'],
                          ['author@localhost'], ['author@exam\u0440le.com']):
                with self.subTest(value=value):
                    path.write_text(json.dumps({**baseline, 'allowed_email_addresses': value}))
                    findings = []
                    self.assertIsNone(scan_skill.load_public_policy(path, findings))
                    self.assertIn('public-policy-invalid', {f.code for f in findings})

    def test_email_approval_does_not_suppress_private_policy_or_secrets(self):
        from dataclasses import replace
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            policy = replace(policy, allowed_email_addresses=frozenset({'author@example.com'}),
                             forbidden_literals=('author@example.com',))
            environment = '$' + 'UNAPPROVED_VARIABLE'
            skill = write_skill(root, body=f'# Demo\n`author@example.com {environment}`\n')
            codes = {f.code for f in scan_skill.scan_skill(skill, policy)}
            self.assertNotIn('public-email', codes)
            self.assertIn('public-private-term', codes)
            self.assertIn('public-environment-variable', codes)

    def test_png_supported_color_and_interlace_scanlines(self):
        for color, depth, raw, palette, interlace in (
            (0, 1, b'\0\0', b'', 0), (0, 16, b'\0\0\0', b'', 0),
            (3, 1, b'\0\0', png_chunk(b'PLTE', b'\xff\0\0'), 0),
            (4, 8, b'\0\0\xff', b'', 0), (6, 8, b'\0\xff\0\0\xff', b'', 0),
            (2, 8, b'\0\xff\0\0', b'', 1),
        ):
            with self.subTest(color=color, depth=depth, interlace=interlace):
                data = (b'\x89PNG\r\n\x1a\n'
                        + png_chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, depth, color, 0, 0, interlace))
                        + palette + png_chunk(b'IDAT', zlib.compress(raw)) + png_chunk(b'IEND', b''))
                self.assertEqual(scan_skill.validate_png(data), (1, 1))

    def test_png_empty_idat_does_not_bypass_order_or_chunk_bound(self):
        valid = make_png()
        invalid = valid[:33] + png_chunk(b'IDAT', b'') + png_chunk(b'tEXt', b'example') + valid[33:]
        with self.assertRaises(ValueError):
            scan_skill.validate_png(invalid)
        with self.assertRaises(ValueError):
            scan_skill.validate_png(make_png(extra=png_chunk(b'tEXt', b'') * 4096))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = write_skill(root)
            (skill / 'assets').mkdir()
            (skill / 'assets/icon.png').write_bytes(valid)
            policy, _ = asset_policy(root, [asset_descriptor(valid)])
            with mock.patch.object(scan_skill, 'MAX_TEXT_BYTES', len(valid) - 1):
                self.assertIn('public-reviewed-asset-invalid',
                              {f.code for f in scan_skill.scan_skill(skill, policy)})


    def test_inline_mask_never_pairs_across_block_boundaries(self):
        link = '[x](missing.md) [y][absent]'
        bodies = [
            f'`a\n# {link}\nb`',
            f'# `a\n{link} b`',
            f'`a\n---\n{link} b`',
            f'`a\n===\n{link} b`',
            f'`a\n* * *\n{link} b`',
            f'`a\n___\n{link} b`',
            f'`a\n- {link}\nb`',
            f'- `a\n- {link} b`',
            f'`a\n1. {link}\nb`',
            f'`a\n> {link}\nb`',
            f'> # `a\n> {link} b`',
            f'    `a\n{link} b`',
            f' \t`a\n{link} b`',
            f'`a\n<div>\n</div>\n{link} b`',
            f'<script>\n`a\ntext </script>\n{link} b`',
            f'<!--\n`a\n-->\n{link} b`',
            f'[id]: /url "`a"\n{link} b`',
            f'[id]: /url\n "`a"\n{link} b`',
            f'`a\n~~~\nnot inline\n~~~\n{link} b`',
        ]
        for body in bodies:
            for newline in ('\n', '\r\n'):
                with self.subTest(body=body, newline=newline), tempfile.TemporaryDirectory() as directory:
                    skill = write_skill(Path(directory), body=body.replace('\n', newline))
                    codes = {f.code for f in scan_skill.scan_skill(skill)}
                    self.assertIn('reference-missing', codes)
                    self.assertIn('reference-definition-missing', codes)

    def test_inline_mask_preserves_ordinary_paragraph_spans_and_offsets(self):
        bodies = [
            '`a\n[x](missing.md) b`',
            '``a ` nested\n[x](missing.md) b``',
            '`a\n  ordinary [x](missing.md) b`',
            '# Heading\n`a\n[x](missing.md) b`',
            '---\n`a\n[x](missing.md) b`',
            '- list\n\n`a\n[x](missing.md) b`',
        ]
        for body in bodies:
            with self.subTest(body=body):
                masked = scan_skill.mask_inline_code(body)
                self.assertEqual(len(masked), len(body))
                self.assertEqual([i for i, c in enumerate(masked) if c == '\n'],
                                 [i for i, c in enumerate(body) if c == '\n'])
                self.assertNotIn('[x]', masked)
        # Same-line code remains supported even in conservative block contexts.
        for prefix in ('# ', '- ', '> ', '    '):
            with self.subTest(prefix=prefix):
                self.assertNotIn('[x]', scan_skill.mask_inline_code(prefix + '`[x](missing.md)`'))


    def test_reference_label_title_cannot_supply_inline_code_opener(self):
        for label in ('foo\nbar', 'foo\\]bar', 'foo\nbar\nbaz'):
            for ticks in ('`', '``'):
                for newline in ('\n', '\r\n'):
                    body = (f'[{label}]: https://example.com "{ticks}a"\n'
                            f'[x](missing.md) [y][absent] b{ticks}')
                    with self.subTest(label=label, ticks=ticks, newline=newline):
                        findings = []
                        scan_skill.scan_links(Path('.'), Path('SKILL.md'),
                                              body.replace('\n', newline), findings)
                        expected_line = body.count('\n') + 1
                        self.assertTrue(any(f.code == 'reference-missing'
                                            and f.line == expected_line for f in findings))
                        self.assertTrue(any(f.code == 'reference-definition-missing'
                                            and f.line == expected_line for f in findings))
                        self.assertNotIn('markdown-parse-error', {f.code for f in findings})

    def test_parser_container_spans_and_source_columns_are_exact(self):
        for body in (
            '> ``a ` nested\n> [fake](missing.md) b``\n> [real](absent.md)',
            '- ``a ` nested\n  [fake](missing.md) b``\n  [real](absent.md)',
            '> - ``a ` nested\n>   [fake](missing.md) b``\n>   [real](absent.md)',
            '[id]: https://example.com\n "`title"\n> ``a\n> [fake](missing.md) b``\n> [real](absent.md)',
            '<div>\n`not inline\n</div>\n\n``a\n[fake](missing.md) b``\n[real](absent.md)',
        ):
            for newline in ('\n', '\r\n'):
                with self.subTest(body=body, newline=newline):
                    text = body.replace('\n', newline)
                    masked = scan_skill.mask_inline_code(text)
                    self.assertEqual(len(masked), len(text))
                    self.assertEqual([(i, c) for i, c in enumerate(masked) if c in '\r\n'],
                                     [(i, c) for i, c in enumerate(text) if c in '\r\n'])
                    self.assertNotIn('[fake]', masked)
                    start = text.index('[real]')
                    self.assertEqual(masked[start:], text[start:])
                    for i, c in enumerate(text):
                        self.assertIn(masked[i], (c, ' '))
                    findings = []
                    scan_skill.scan_links(Path('.'), Path('SKILL.md'), text, findings)
                    missing = [f for f in findings if f.code == 'reference-missing']
                    self.assertEqual([(f.line, f.message) for f in missing],
                                     [(text.count('\n', 0, start) + 1,
                                       'referenced file does not exist: absent.md')])

    def test_parser_failure_blocks_without_blinding_other_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, policy = write_public_policy(root)
            skill = write_skill(root, body='`Private Product $' + 'UNAPPROVED_VARIABLE`\n'
                                '[x](missing.md) [y][absent]\n')
            with mock.patch.object(scan_skill, 'MarkdownIt', side_effect=RuntimeError('test')):
                codes = {f.code for f in scan_skill.scan_skill(skill, policy)}
            self.assertTrue({'markdown-parse-error', 'public-private-term',
                             'public-environment-variable', 'reference-missing',
                             'reference-definition-missing'} <= codes)

    def test_missing_parser_dependency_errors_instead_of_success_json(self):
        import subprocess
        result = subprocess.run([sys.executable, '-S', str(SCRIPT), '.',
                                 '--format', 'json'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('dependency unavailable', result.stderr)
        self.assertIn('scan not performed', result.stderr)

    def test_parsed_reference_definitions_keep_local_targets_and_offsets(self):
        body = '> [foo\n> bar]: missing.md\n> "`title"\n\n[x][foo bar]\n'
        findings = []
        scan_skill.scan_links(Path('.'), Path('SKILL.md'), body, findings)
        self.assertTrue(any(f.code == 'reference-missing' and f.line == 1 for f in findings))
        self.assertNotIn('reference-definition-missing', {f.code for f in findings})
        self.assertNotIn('markdown-parse-error', {f.code for f in findings})


if __name__ == "__main__":
    unittest.main()
