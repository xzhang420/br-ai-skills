"""Installer integration tests in isolated homes; no real account changes."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location('workflow1_install', ROOT / 'scripts/install.py')
i = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(i)


class InstallTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.home = self.root / 'Home with spaces'
        self.codex = self.home / '.codex'
        self.codex.mkdir(parents=True)
        self.base = self.codex / 'config.toml'
        self.base.write_text('model = "existing-model"\n', encoding='utf-8')
        self.source = self.root / 'checkout/skills/shared-workflow-1'
        shutil.copytree(ROOT, self.source, ignore=i.IGNORES)

    def install(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return i.install(self.source, self.home, self.codex, **kwargs)

    def link(self, path, target):
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest('This host cannot create symlinks; copy installation is tested separately.')

    def test_dry_run_makes_no_changes(self):
        result = self.install()
        self.assertGreater(result['actions'], 0)
        self.assertFalse((self.home / '.agents').exists())
        self.assertEqual(list(self.codex.iterdir()), [self.base])

    def test_copy_install_and_repeat_preserve_base_and_local_settings(self):
        self.install(apply=True, strategy='copy')
        target = self.home / '.agents/skills/workflow-1'
        self.assertFalse(target.is_symlink())
        self.assertEqual(i.source_files(target), i.source_files(self.source))
        local = self.codex / 'workflow1-local.json'
        local.write_text('{"schema_version":1,"commands":{"claude":["custom-claude"]}}', encoding='utf-8')
        before = local.read_bytes()
        self.assertEqual(self.install(apply=True, strategy='copy')['actions'], 0)
        self.assertEqual(local.read_bytes(), before)
        self.assertEqual(self.base.read_text(encoding='utf-8'), 'model = "existing-model"\n')

    def test_no_symlink_privilege_falls_back_to_copy(self):
        with mock.patch.object(Path, 'symlink_to', side_effect=OSError('privilege unavailable')):
            self.install(apply=True)
        self.assertTrue((self.home / '.agents/skills/workflow-1' / i.MARKER).is_file())

    def test_copy_refresh_backs_up_old_content(self):
        self.install(apply=True, strategy='copy')
        target = self.home / '.agents/skills/workflow-1'
        original = (target / 'SKILL.md').read_bytes()
        (self.source / 'SKILL.md').write_bytes(original + b'\nUpdated shared source.\n')
        self.install(apply=True, strategy='copy')
        self.assertEqual((target / 'SKILL.md').read_bytes(), (self.source / 'SKILL.md').read_bytes())
        backups = list((self.codex / 'backups').glob('*/.agents/skills/workflow-1/SKILL.md'))
        self.assertTrue(any(p.read_bytes() == original for p in backups))

    def test_shared_root_reuse_and_old_name_migration(self):
        self.link(self.codex / 'skills', self.source.parent)
        old = self.source.parent / 'godzilla-workflow-1'
        old.mkdir()
        (old / 'SKILL.md').write_text('old skill', encoding='utf-8')
        (self.codex / 'AGENTS.md').write_text('Keep me\n\n## Workflow 1 entry point\nOld pointer\n\n## Other rule\nKeep this too\n', encoding='utf-8')
        result = self.install(apply=True, replace_legacy=True)
        self.assertEqual(result['discovery'], str(self.codex / 'skills/shared-workflow-1'))
        self.assertFalse(old.exists())
        self.assertFalse((self.home / '.agents/skills/workflow-1').exists())
        guidance = (self.codex / 'AGENTS.md').read_text(encoding='utf-8')
        self.assertIn('shared-workflow-1/SKILL.md', guidance)
        self.assertIn('Keep this too', guidance)
        self.assertEqual(self.install(apply=True)['actions'], 0)

    def test_unmanaged_existing_skill_needs_explicit_migration(self):
        target = self.home / '.agents/skills/workflow-1'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('local customization', encoding='utf-8')
        with self.assertRaisesRegex(RuntimeError, 'replace-legacy'):
            self.install(apply=True)
        self.assertEqual((target / 'SKILL.md').read_text(encoding='utf-8'), 'local customization')
        self.assertFalse((self.codex / 'backups').exists())

    def test_config_symlink_refused_before_retiring_skill(self):
        target = self.home / '.agents/skills/workflow-1'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('old', encoding='utf-8')
        alternate = self.root / 'profile.toml'
        alternate.write_text('custom = true\n', encoding='utf-8')
        self.link(self.codex / 'workflow1-lower.config.toml', alternate)
        with self.assertRaisesRegex(RuntimeError, 'config symlink'):
            self.install(apply=True, replace_legacy=True)
        self.assertTrue(target.exists())
        self.assertFalse((self.codex / 'backups').exists())

    def test_external_codex_home_backups(self):
        self.codex = self.root / 'External Codex'
        self.codex.mkdir()
        (self.codex / 'AGENTS.md').write_text('External guidance\n', encoding='utf-8')
        self.install(apply=True, strategy='copy')
        backups = list((self.codex / 'backups').glob('*/external-codex-home/AGENTS.md'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding='utf-8'), 'External guidance\n')


if __name__ == '__main__':
    unittest.main()
