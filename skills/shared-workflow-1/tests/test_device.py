"""Local settings and Windows argv contracts, without provider inference."""
import importlib.util
import json
from pathlib import Path
import shlex
import sys
import tempfile
import types
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location('workflow1_device', Path(__file__).parents[1] / 'scripts/orchestrate.py')
w = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w)


class DeviceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = self.root / 'workflow1-local.json'

    def test_missing_settings_use_local_defaults(self):
        settings = w.local_settings(self.config)
        self.assertEqual(settings['commands'], {})
        self.assertIsNone(settings['env_file'])

    def test_relative_env_path_is_relative_to_settings(self):
        self.config.write_text(json.dumps({'commands': {'codex': ['native path/codex.exe']}, 'env_file': 'private/key.env'}), encoding='utf-8')
        settings = w.local_settings(self.config)
        self.assertEqual(settings['env_file'], str(self.root / 'private/key.env'))
        self.assertEqual(settings['commands']['codex'], ['native path/codex.exe'])

    def test_command_string_and_invalid_schema_are_rejected(self):
        for data in [{'commands': {'codex': 'node cli.js'}}, {'schema_version': 99}, {'commands': {'unknown': ['x']}}]:
            self.config.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaises(w.WorkflowError):
                w.local_settings(self.config)

    def test_windows_json_paths_round_trip_without_shell(self):
        argv = [r'C:\Users\Researcher Name\python.exe', r'D:\Research Data\validate.py', 'a&b $(literal)']
        args = types.SimpleNamespace(test=None, test_argv=json.dumps(argv))
        self.assertEqual(shlex.split(w.test_argument(args)), argv)
        self.assertEqual(w.parser().parse_args(['test', '--run', 'x', '--test-argv', args.test_argv, '--artifact', 'file.py']).test_argv, args.test_argv)

    def test_powershell_utf8_bom_argument_file_and_settings(self):
        argv = [r'C:\Program Files\Python\python.exe', '-m', 'unittest']
        path = self.root / 'test command.json'
        path.write_text(json.dumps(argv), encoding='utf-8-sig')
        args = w.parser().parse_args(['test', '--run', 'x', '--test-argv-file', str(path), '--artifact', 'file.py'])
        self.assertEqual(shlex.split(w.test_argument(args)), argv)
        self.config.write_text('{"schema_version":1,"commands":{}}', encoding='utf-8-sig')
        self.assertEqual(w.local_settings(self.config)['commands'], {})

    def test_windows_batch_wrapper_requires_native_launcher(self):
        with mock.patch.object(w.os, 'name', 'nt'), mock.patch.object(w.shutil, 'which', return_value=r'C:\Tools\codex.cmd'):
            with self.assertRaisesRegex(w.WorkflowError, 'batch wrappers'):
                w.executable_argv(['codex', 'literal & text'])
        with mock.patch.object(w.os, 'name', 'nt'), mock.patch.object(w.shutil, 'which', return_value=r'C:\Program Files\node.exe'):
            actual = w.executable_argv(['node', r'C:\Tool Space\cli.js', 'literal & text'])
        self.assertEqual(actual[1:], [r'C:\Tool Space\cli.js', 'literal & text'])

    def test_provider_uses_device_command_and_cli_env_override(self):
        env_file = self.root / 'private.env'
        env_file.write_text('GEMINI_API_KEY=example-only\n', encoding='utf-8')
        self.config.write_text(json.dumps({'commands': {'claude': ['native-claude', 'prefix-option']}, 'env_file': 'missing.env'}), encoding='utf-8')
        run = w.Run.create(self.root / 'project', 'synthetic only')
        args = types.SimpleNamespace(device_config=str(self.config), env_file=str(env_file), allow_external=True, timeout=5)
        provider = w.Providers(run, args)
        with mock.patch.object(w, 'command', return_value=json.dumps({'result': 'review', 'model': 'claude-opus-5-5'})) as call:
            provider.call('claude', 'synthetic prompt')
        self.assertEqual(call.call_args.args[0][:2], ['native-claude', 'prefix-option'])
        self.assertEqual(provider.env['GEMINI_API_KEY'], 'example-only')

    def test_real_test_with_space_and_unicode_path(self):
        project = self.root / 'Research space \u03bb'
        project.mkdir()
        code = project / 'validate space.py'
        code.write_text('print("verified")\n', encoding='utf-8')
        run = w.Run.create(project, 'Verify argument preservation and \u03c3 uncertainty')
        self.assertIn('\u03c3', run.read('objective'))
        for phase in ('plan', 'critique', 'specification'):
            run.record(phase, phase, {'source': 'test_stub'})
        run.freeze()
        run.approve()
        run.record('implementation', 'created validation script', {'source': 'test_stub'})
        args = types.SimpleNamespace(test_argv=json.dumps([sys.executable, str(code)]), test=None)
        result = w.run_test(run, w.test_argument(args), [str(code)])
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(w.test_passes(run))


if __name__ == '__main__':
    unittest.main()
