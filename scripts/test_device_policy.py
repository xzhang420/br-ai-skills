"""Local-only installer tests; fixtures never touch the real Codex profile."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('policy', Path(__file__).with_name('install-device-policy.py'))
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skill-policy-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.profile = self.root / 'profile'
        (self.repo / 'scripts/templates').mkdir(parents=True)
        self.profile.mkdir()
        for name in ('AGENTS.md', 'third-party-skills.toml'):
            (self.repo / name).write_text('fixture', encoding='utf-8')
        template = Path(__file__).parent / 'templates/global-skills-instructions.md'
        (self.repo / 'scripts/templates/global-skills-instructions.md').write_text(
            template.read_text(encoding='utf-8'), encoding='utf-8')

    def install(self):
        return policy.install(self.repo, self.profile, 'workstation')

    def test_preserves_existing_and_idempotent(self):
        target = self.profile / 'AGENTS.md'
        target.write_text('Existing user instructions.\n', encoding='utf-8')
        self.assertEqual(self.install()['status'], 'installed')
        first = target.read_bytes()
        self.assertTrue(first.startswith(b'Existing user instructions.'))
        self.assertNotIn(b'{{', first)
        self.assertEqual(self.install()['status'], 'up_to_date')
        self.assertEqual(target.read_bytes(), first)
        self.assertEqual((self.profile / 'AGENTS.before-skills-policy.md.bak').read_text(),
                         'Existing user instructions.\n')

    def test_new_profile_identity(self):
        self.install()
        identity = json.loads((self.profile / 'skills-device.json').read_text())
        self.assertEqual(identity['device'], 'workstation')
        self.assertEqual(identity['repository'], self.repo.resolve().as_posix())

    def test_override_blocks(self):
        (self.profile / 'AGENTS.override.md').write_text('Override')
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse((self.profile / 'AGENTS.md').exists())

    def test_conflicting_identity_blocks(self):
        (self.profile / 'skills-device.json').write_text('{"device":"personal"}')
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse((self.profile / 'AGENTS.md').exists())

    def test_malformed_markers_block(self):
        for value in (policy.BEGIN, policy.END, policy.END + policy.BEGIN,
                      policy.BEGIN * 2 + policy.END * 2):
            with self.subTest(value=value), self.assertRaises(ValueError):
                policy.merge_block(value, 'new')

    def test_replacement_preserves_suffix(self):
        old = 'before\n' + policy.BEGIN + '\nold\n' + policy.END + '\nafter'
        new = policy.BEGIN + '\nnew\n' + policy.END
        self.assertEqual(policy.merge_block(old, new), 'before\n' + new + '\nafter')

    def test_invalid_device_blocks(self):
        with self.assertRaises(ValueError):
            policy.install(self.repo, self.profile, 'bad\npolicy')


if __name__ == '__main__':
    unittest.main()
