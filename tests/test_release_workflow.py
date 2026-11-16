"""Verify the version check used when preparing a release."""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/draft-release.yml"


@pytest.mark.parametrize(
    ("version", "prerelease", "existing_tag", "error"),
    [
        ("2.0.0", "false", None, None),
        ("2.1.0rc1", "true", None, None),
        ("2.1.0rc1", "false", None, "must be marked as a prerelease"),
        ("2.0.0", "true", "v2.0.0", "already exists"),
        ("not-a-version", "true", None, "Unsupported version"),
    ],
)
def test_release_version_check(tmp_path, version, prerelease, existing_tag, error):
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    command = workflow["jobs"]["draft"]["steps"][1]["run"]
    manifest = tmp_path / "custom_components" / "card" / "manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({"version": version}), encoding="utf-8")
    output = tmp_path / "output"
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    if existing_tag:
        subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
        subprocess.run(
            [
                "git", "-C", str(tmp_path), "-c", "user.name=Test",
                "-c", "user.email=test@example.invalid", "commit", "-qm", "test",
            ],
            check=True,
        )
        subprocess.run(["git", "-C", str(tmp_path), "tag", existing_tag], check=True)
    result = subprocess.run(
        ["bash", "-e", "-c", command],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
            "GITHUB_OUTPUT": str(output),
            "PRERELEASE": prerelease,
        },
        capture_output=True,
        text=True,
    )
    if error:
        assert result.returncode != 0
        assert error in result.stderr
    else:
        assert result.returncode == 0, result.stderr
        assert output.read_text(encoding="utf-8") == f"tag=v{version}\n"


@pytest.mark.parametrize("prerelease", [True, False])
def test_draft_targets_tested_commit(tmp_path, prerelease):
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    command = workflow["jobs"]["draft"]["steps"][2]["run"]
    gh = tmp_path / "gh"
    gh.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, sys\n"
        "with open(os.environ['ARGS_FILE'], 'w') as f:\n"
        "    json.dump(sys.argv[1:], f)\n",
        encoding="utf-8",
    )
    gh.chmod(0o755)
    args_file = tmp_path / "args.json"
    subprocess.run(
        ["bash", "-e", "-c", command],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": f"{tmp_path}{os.pathsep}{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
            "ARGS_FILE": str(args_file),
            "GITHUB_SHA": "0123456789abcdef",
            "PRERELEASE": str(prerelease).lower(),
            "TAG": "v2.0.0",
        },
        check=True,
    )
    args = json.loads(args_file.read_text(encoding="utf-8"))
    assert args[:3] == ["release", "create", "v2.0.0"]
    assert "--draft" in args
    assert args[args.index("--target") + 1] == "0123456789abcdef"
    assert ("--prerelease" in args) is prerelease
