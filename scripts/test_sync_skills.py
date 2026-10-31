"""Exercise safe sync against disposable local Git repos; no network access."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('sync-skills.ps1').resolve()
SHELL = shutil.which('pwsh') or shutil.which('powershell')


def git(path, *args):
    return subprocess.check_output(
        ['git', '-C', str(path), *args], stderr=subprocess.STDOUT, text=True
    ).strip()


@unittest.skipUnless(SHELL, 'PowerShell required')
class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skill-sync-test-')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.remote = root / 'remote.git'
        self.seed = root / 'seed'
        self.clone = root / 'clone'
        self.remote.mkdir()
        self.seed.mkdir()
        git(self.remote, 'init', '--bare', '--initial-branch=main')
        git(self.seed, 'init', '--initial-branch=main')
        self.commit(self.seed, 'initial.txt')
        git(self.seed, 'remote', 'add', 'origin', str(self.remote))
        git(self.seed, 'push', '-u', 'origin', 'main')
        git(root, 'clone', str(self.remote), str(self.clone))

    def commit(self, repo, name):
        (repo / name).write_text(name, encoding='utf-8')
        git(repo, 'add', name)
        git(repo, '-c', 'user.name=Sync Test', '-c', 'user.email=sync@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-m', name)

    def sync(self, success, status):
        before = git(self.clone, 'rev-parse', 'HEAD')
        result = subprocess.run([SHELL, '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', str(SCRIPT), '-RepoPath', str(self.clone),
            '-ExpectedRemote', str(self.remote)], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        output = json.loads(result.stdout.strip())
        self.assertEqual(output['status'], status)
        if not success:
            self.assertEqual(git(self.clone, 'rev-parse', 'HEAD'), before)

    def test_up_to_date(self):
        self.sync(True, 'up_to_date')

    def test_fast_forward(self):
        self.commit(self.seed, 'remote.txt')
        git(self.seed, 'push')
        self.sync(True, 'updated')
        self.assertTrue((self.clone / 'remote.txt').exists())

    def test_untracked(self):
        (self.clone / 'unfinished.txt').write_text('keep')
        self.sync(False, 'needs_attention')
        self.assertEqual((self.clone / 'unfinished.txt').read_text(), 'keep')

    def test_modified(self):
        (self.clone / 'initial.txt').write_text('keep')
        self.sync(False, 'needs_attention')
        self.assertEqual((self.clone / 'initial.txt').read_text(), 'keep')

    def test_ahead(self):
        self.commit(self.clone, 'local.txt')
        self.sync(False, 'needs_attention')
        self.assertNotEqual(git(self.remote, 'rev-parse', 'main'), git(self.clone, 'rev-parse', 'HEAD'))

    def test_diverged(self):
        self.commit(self.clone, 'local.txt')
        self.commit(self.seed, 'remote.txt')
        git(self.seed, 'push')
        self.sync(False, 'needs_attention')

    def test_wrong_branch(self):
        git(self.clone, 'switch', '-c', 'work')
        self.sync(False, 'needs_attention')

    def test_git_lock(self):
        (self.clone / '.git' / 'index.lock').touch()
        self.sync(False, 'needs_attention')

    def test_wrong_remote(self):
        git(self.clone, 'remote', 'set-url', 'origin', str(self.seed))
        self.sync(False, 'needs_attention')


if __name__ == '__main__':
    unittest.main()
