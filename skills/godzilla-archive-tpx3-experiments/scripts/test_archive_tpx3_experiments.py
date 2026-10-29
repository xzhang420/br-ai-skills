"""Exercise archiving on temporary fixtures; never access proposal data."""

import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time
import unittest


SCRIPT = Path(__file__).with_name("archive_tpx3_experiments.sh")


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tpx3-archive-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "proposal" / "raw"
        self.root.mkdir(parents=True)

    def source(self, name="exp001", root=None):
        root = root or self.root
        folder = root / name
        for run in ("run_00000", "continuation_00000"):
            path = folder / run / "timestamp_000000.tpx3"
            path.parent.mkdir(parents=True)
            path.write_bytes(b"synthetic TPX3 fixture\x00\xff\n")
            old = time.time() - 7200
            os.utime(path, (old, old))
        return folder

    def invoke(self, *options, names=("exp001",), root=None, env=None):
        return subprocess.run(
            ["bash", str(SCRIPT), "--root", str(root or self.root),
             "--threads", "1", *options, "--", *names],
            text=True, capture_output=True, env=env,
        )

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_audit_creates_nothing(self):
        self.source()
        before = set(self.base.rglob("*"))
        result = self.invoke()
        self.assert_ok(result)
        self.assertIn("SOURCE_POLICY=retain", result.stdout)
        self.assertIn("AUDIT_OK", result.stdout)
        self.assertEqual(before, set(self.base.rglob("*")))

    def test_raw_preserves_bytes_paths_and_unselected_folders(self):
        source = self.source()
        self.source(".recycle")
        self.source(".legacy_intermediates")
        self.source("exp002")
        before = {p: p.read_bytes() for p in self.root.rglob("*.tpx3")}
        self.assert_ok(self.invoke("--execute"))
        for path, contents in before.items():
            self.assertEqual(path.read_bytes(), contents)
        with tarfile.open(self.root / "exp001.tar.gz", "r:gz") as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            self.assertEqual(len(members), 2)
            for member in members:
                self.assertEqual(archive.extractfile(member).read(),
                                 (self.root / member.name).read_bytes())
                self.assertEqual(Path(member.name).parts[0], source.name)
        log = (self.root.parent / "compression_tpx3_experiments.log").read_text()
        self.assertIn("SOURCE RETAINED: exp001", log)
        self.assertIn("ALL COMPLETE", log)
        self.assertFalse((self.root / "exp002.tar.gz").exists())

    def test_legacy_layout_and_default_log(self):
        root = self.base / "legacy_proposal/data/experiments/tpx3Files"
        root.mkdir(parents=True)
        source = self.source(root=root)
        self.assert_ok(self.invoke("--execute", root=root))
        self.assertTrue(source.exists())
        self.assertTrue((root / "exp001.tar.gz").exists())
        self.assertTrue((self.base / "legacy_proposal/compression_tpx3_experiments.log").exists())

    def test_deletion_requires_option_and_only_removes_selected_fixture(self):
        source = self.source()
        other = self.source("exp002")
        self.assert_ok(self.invoke("--execute", "--delete-sources"))
        self.assertFalse(source.exists())
        self.assertTrue(other.exists())
        with tarfile.open(self.root / "exp001.tar.gz", "r:gz") as archive:
            self.assertEqual(len([m for m in archive.getmembers() if m.isfile()]), 2)

    def test_hidden_targets_refused(self):
        for name in (".recycle", ".legacy_intermediates"):
            self.source(name)
            result = self.invoke("--execute", names=(name,))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("hidden directories", result.stderr)
            self.assertTrue((self.root / name).exists())

    def test_final_and_partial_conflicts_preserved(self):
        self.source()
        for suffix in (".tar.gz", ".tar.gz.partial"):
            with self.subTest(suffix=suffix):
                path = self.root / ("exp001" + suffix)
                path.write_bytes(b"existing archive")
                result = self.invoke("--execute")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(path.read_bytes(), b"existing archive")
                self.assertTrue((self.root / "exp001").exists())
                path.unlink()

    def test_oversize_and_recent_sources_refused(self):
        source = self.source()
        result = self.invoke("--execute", "--max-source-bytes", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source exceeds max bytes", result.stderr)
        os.utime(next(source.rglob("*.tpx3")), None)
        result = self.invoke("--execute")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("recently modified source", result.stderr)
        self.assertFalse((self.root / "exp001.tar.gz").exists())

    def stub_env(self, name, body):
        folder = self.base / "bin"
        folder.mkdir(exist_ok=True)
        path = folder / name
        path.write_text("#!/bin/sh\n" + body)
        path.chmod(0o755)
        return dict(os.environ, PATH=str(folder) + os.pathsep + os.environ["PATH"])

    def test_retention_budgets_all_archives(self):
        one = self.source()
        self.source("exp002")
        size = sum(p.stat().st_size for p in one.rglob("*.tpx3"))
        available = size + size // 100 + 1073741824
        env = self.stub_env("df", f"printf 'Avail\\n{available}\\n'\n")
        keep = self.invoke(names=("exp001", "exp002"), env=env)
        self.assertNotEqual(keep.returncode, 0)
        self.assertIn("insufficient free space", keep.stderr)
        remove = self.invoke("--delete-sources", names=("exp001", "exp002"), env=env)
        self.assert_ok(remove)
        self.assertTrue(one.exists())  # An audit never deletes sources.

    def test_failed_verification_keeps_source_even_with_deletion_option(self):
        source = self.source()
        env = self.stub_env("pigz", "cat >/dev/null\nprintf 'invalid gzip archive'\n")
        result = self.invoke("--execute", "--delete-sources", env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(source.exists())
        self.assertTrue((self.root / "exp001.tar.gz.partial").exists())
        self.assertFalse((self.root / "exp001.tar.gz").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
