"""Offline contract tests; provider stubs are never persisted as live evidence."""
import importlib.util
from pathlib import Path
import sys
import shlex
import tempfile
import types
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location('workflow1', Path(__file__).parents[1] / 'scripts' / 'orchestrate.py')
w = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w)
PASS_VALIDATION = 'VERDICT: PASS\nTEST_COMMAND: python3 -m unittest\nTEST_EXIT_CODE: 0\nObserved all checks passing'
STUB = {'source': 'test_stub', 'execution': 'simulated', 'requested_model': 'stub', 'actual_model': None}

class Fake:
    def __init__(self, replies, reviewer='claude'):
        self.replies = iter(replies)
        self.args = types.SimpleNamespace(reviewer=reviewer, research=False, test=shlex.join([sys.executable, '-c', 'pass']), artifact=['answer.py', 'test_answer.py'], timeout=5)
        self.prompts = []
    def preflight(self):
        pass
    def call(self, role, prompt, write=False):
        self.prompts.append((role, prompt, write))
        return next(self.replies), STUB

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.run = w.Run.create(self.temp.name, 'Add two numbers', run_id='test')
        (Path(self.temp.name) / 'answer.py').write_text('def add(a, b): return a + b\n', encoding='utf-8')
        (Path(self.temp.name) / 'test_answer.py').write_text('from answer import add\nassert add(2, 3) == 5\n', encoding='utf-8')
    def ready(self):
        for p in ('plan', 'critique', 'specification'):
            self.run.record(p, p + ' evidence', STUB)
        self.run.freeze()
        self.run.approve()
    def test_artifacts_and_ignore(self):
        self.assertTrue(all((self.run.path / (p + '.md')).exists() for p in w.PHASES))
        self.assertEqual('*\n', (Path(self.temp.name) / '.workflow1' / '.gitignore').read_text(encoding='utf-8'))
        self.assertFalse((Path(self.temp.name) / '.gitignore').exists())
        self.assertEqual(self.run.state['state'], 'planning')
    def test_approval_gate_and_frozen_mutation(self):
        with self.assertRaises(w.WorkflowError):
            w.execute(self.run, Fake([]))
        self.ready()
        (self.run.path / 'specification.md').write_text('tampered', encoding='utf-8')
        with self.assertRaises(w.WorkflowError):
            self.run.check_approved()
    def test_upstream_edit_invalidates_downstream(self):
        self.ready()
        self.run.record('plan', 'changed plan', STUB)
        self.assertFalse(self.run.valid('critique'))
        self.assertFalse(self.run.valid('specification'))
        with self.assertRaises(w.WorkflowError):
            self.run.approve()
    def test_plan_stops_and_resume_skips_completed(self):
        fake = Fake(['plan', 'critique', 'spec'])
        w.plan(self.run, fake)
        self.assertEqual(self.run.state['state'], 'awaiting_approval')
        self.assertEqual(len(fake.prompts), 3)
        self.assertFalse(self.run.valid('implementation'))
        w.plan(self.run, Fake([]))
        self.assertEqual(self.run.state['state'], 'awaiting_approval')
    def test_revise_routes_feedback_to_implementation(self):
        self.ready()
        fake = Fake(['impl', 'tests fail', 'DECISION: REVISE\nFix edge case',
                     'fixed', PASS_VALIDATION, 'DECISION: PASS\nEvidence adequate', 'Astra interpretation'])
        w.execute(self.run, fake)
        self.assertEqual(self.run.state['state'], 'awaiting_human_acceptance')
        self.run.accept('accept', 'Human reviewed the observed results')
        self.assertEqual(self.run.state['state'], 'accepted')
        self.assertEqual(self.run.state['repair_rounds'], 1)
        self.assertIn('Fix edge case', fake.prompts[3][1])
        self.assertTrue(fake.prompts[3][2])
        self.assertIn('untrusted_review_feedback', fake.prompts[3][1])
        self.assertTrue(all(p['execution'] == 'simulated' for phase, p in self.run.state['records'].items() if phase != 'acceptance'))
    def test_replan_requires_new_approval_and_keeps_feedback(self):
        self.ready()
        w.execute(self.run, Fake(['impl', 'test', 'DECISION: REPLAN\nChange required metric']))
        self.assertEqual(self.run.state['state'], 'planning')
        with self.assertRaises(w.WorkflowError):
            self.run.check_approved()
        fake = Fake(['new plan', 'new critique', 'new spec'])
        w.plan(self.run, fake)
        self.assertIn('Change required metric', fake.prompts[0][1])
        self.assertEqual(self.run.state['state'], 'awaiting_approval')
    def test_insufficient_and_round_limit(self):
        self.ready()
        w.execute(self.run, Fake(['impl', 'cannot run', 'Unknown outcome']))
        self.assertEqual(self.run.state['state'], 'blocked')
        self.ready()
        w.execute(self.run, Fake(['impl', 'fail', 'DECISION: REVISE'] * 3))
        self.assertEqual(self.run.state['repair_rounds'], 2)
        self.assertEqual(self.run.state['state'], 'blocked')
    def test_missing_providers_no_silent_fallback(self):
        args = types.SimpleNamespace(reviewer='claude', allow_external=True, research=False, env_file=None)
        provider = w.Providers(self.run, args)
        with mock.patch.object(w.shutil, 'which', side_effect=lambda cmd: '/bin/codex' if cmd == 'codex' else None):
            with self.assertRaisesRegex(w.WorkflowError, 'explicitly choose'):
                provider.preflight()
            args.reviewer = 'codex'
            provider.preflight()
    def test_external_and_research_consent(self):
        args = types.SimpleNamespace(reviewer='claude', allow_external=False, allow_research_cost=False, research=False, env_file=None)
        provider = w.Providers(self.run, args)
        with mock.patch.object(w.shutil, 'which', return_value='/bin/stub'):
            with self.assertRaisesRegex(w.WorkflowError, 'allow-external'):
                provider.preflight()
            args.reviewer = 'codex'
            args.research = True
            with self.assertRaisesRegex(w.WorkflowError, 'allow-research-cost'):
                provider.preflight()
    def test_timeout_kills_group(self):
        with self.assertRaisesRegex(w.WorkflowError, 'timed out'):
            w.command([sys.executable, '-c', 'import time; time.sleep(10)'], self.temp.name, {}, .05)
    def test_error_does_not_echo_credentials(self):
        with self.assertRaises(w.WorkflowError) as caught:
            w.command([sys.executable, '-c', "import sys; print('SECRET'); sys.exit(1)"], self.temp.name, {}, 2)
        self.assertNotIn('SECRET', str(caught.exception))
    def test_env_file_is_literal_allowlist_and_preserves_process_env(self):
        envfile = Path(self.temp.name) / 'private.env'
        envfile.write_text('PATH=evil\nGEMINI_API_KEY="$(touch /tmp/never-run-this)"\nOPENAI_API_KEY=filevalue\n', encoding='utf-8')
        with mock.patch.dict(w.os.environ, {'OPENAI_API_KEY': 'existing'}, clear=True):
            env = w.load_env(envfile)
        self.assertNotIn('PATH', env)
        self.assertEqual(env['GEMINI_API_KEY'], '$(touch /tmp/never-run-this)')
        self.assertEqual(env['OPENAI_API_KEY'], 'existing')
    def test_returned_model_not_invented(self):
        content, model = w.codex_result('{"type":"item.completed","item":{"type":"agent_message","text":"done"}}')
        self.assertEqual(content, 'done')
        self.assertIsNone(model)
    def test_mode_change_invalidates_approval_preserves_versions(self):
        self.ready()
        original = self.run.state['records']['plan']['version_path']
        self.run.set_mode('higher')
        self.assertEqual(self.run.state['mode'], 'higher')
        self.assertFalse(self.run.valid('plan'))
        self.assertEqual((self.run.path / original).read_text(encoding='utf-8'), 'plan evidence')
        with self.assertRaises(w.WorkflowError):
            self.run.check_approved()
    def test_acceptance_cannot_override_failing_validation(self):
        self.ready()
        w.execute(self.run, Fake(['impl', 'VERDICT: REVISE', 'DECISION: PASS']))
        self.assertEqual(self.run.state['state'], 'blocked')
        with self.assertRaises(w.WorkflowError):
            self.run.accept('accept', 'Human reviewed the observed results')
    def test_record_versions_are_preserved(self):
        self.run.record('plan', 'first', STUB)
        self.run.record('plan', 'second', STUB)
        entries = self.run.state['history']
        self.assertEqual([(self.run.path / e['version_path']).read_text(encoding='utf-8') for e in entries], ['first', 'second'])
    def test_objective_mutation_invalidates_approval(self):
        self.ready()
        (self.run.path / 'objective.md').write_text('new objective', encoding='utf-8')
        with self.assertRaises(w.WorkflowError):
            self.run.check_approved()
    def test_real_failed_test_overrides_provider_pass(self):
        self.ready()
        fake = Fake(['impl', PASS_VALIDATION, 'DECISION: PASS'])
        fake.args.test = shlex.join([sys.executable, '-c', 'raise SystemExit(3)'])
        w.execute(self.run, fake)
        self.assertEqual(self.run.state['test_result']['exit_code'], 3)
        self.assertEqual(self.run.state['state'], 'blocked')
        with self.assertRaises(w.WorkflowError):
            self.run.accept('accept', 'Attempt to accept failed test')
    def test_test_log_tampering_blocks_acceptance(self):
        self.ready()
        fake = Fake(['impl', PASS_VALIDATION, 'DECISION: PASS', 'Interpretation'])
        w.execute(self.run, fake)
        (self.run.path / self.run.state['test_result']['log_path']).write_text('tampered', encoding='utf-8')
        with self.assertRaises(w.WorkflowError):
            self.run.accept('accept', 'Review complete')
    def test_human_rejection_records_reason(self):
        self.run.accept('reject', 'Need a different objective')
        self.assertEqual(self.run.state['state'], 'rejected')
        self.assertIn('Need a different objective', self.run.read('acceptance'))
    def test_gemini_steps_and_legacy_outputs(self):
        self.assertEqual(w.research_text({'steps': [{'content': [{'type': 'text', 'text': 'new API'}]}]}), 'new API')
        self.assertEqual(w.research_text(types.SimpleNamespace(outputs=[types.SimpleNamespace(text='legacy')])), 'legacy')
    def test_claude_reported_model_and_honest_restriction(self):
        args = types.SimpleNamespace(reviewer='claude', allow_external=True, research=False, env_file=None, timeout=1)
        provider = w.Providers(self.run, args)
        with mock.patch.object(w, 'command', return_value='{"result":"review", "modelUsage":{"different-model":{}}}'):
            text, provenance = provider.call('claude', 'review prompt')
        self.assertEqual(provenance['actual_model'], 'different-model')
        self.assertTrue(provenance['model_mismatch'])
        self.assertIsNone(provenance['sandbox'])
        self.assertIn('Read,Glob,Grep', provenance['tool_restriction'])
    def test_portable_skills_checkout_rejects_run_data(self):
        repo = Path(self.temp.name) / 'portable-skills'
        (repo / 'skills').mkdir(parents=True)
        (repo / 'third-party-skills.toml').write_text('', encoding='utf-8')
        with self.assertRaises(w.WorkflowError):
            w.Run.create(repo / 'scratch', 'objective')
    def test_actual_source_and_test_changes_block_acceptance(self):
        self.ready()
        w.execute(self.run, Fake(['impl', PASS_VALIDATION, 'DECISION: PASS', 'Interpretation']))
        source = Path(self.temp.name) / 'answer.py'
        original = source.read_text(encoding='utf-8')
        source.write_text('def add(a, b): return a - b', encoding='utf-8')
        self.assertFalse(w.test_passes(self.run))
        with self.assertRaises(w.WorkflowError):
            self.run.accept('accept', 'Cannot accept changed code')
        source.write_text(original, encoding='utf-8')
        testfile = Path(self.temp.name) / 'test_answer.py'
        testfile.write_text('assert True', encoding='utf-8')
        self.assertFalse(w.test_passes(self.run))
    def test_accepted_records_closed_and_review_invalidates_downstream(self):
        self.ready()
        w.execute(self.run, Fake(['impl', PASS_VALIDATION, 'DECISION: PASS', 'Interpretation']))
        self.run.record('review', 'DECISION: REPLAN', STUB)
        self.assertFalse(self.run.valid('stage-report'))
        self.assertFalse(self.run.valid('acceptance'))
        self.assertEqual(self.run.state['state'], 'reviewed')
        self.run.record('review', 'DECISION: PASS', STUB)
        self.run.record('stage-report', 'Interpretation', STUB)
        self.run.accept('accept', 'Reviewed evidence')
        with self.assertRaises(w.WorkflowError):
            self.run.record('review', 'DECISION: REPLAN', STUB)
        self.assertEqual(self.run.read('review'), 'DECISION: PASS')
    def test_artifact_manifest_change_forces_revalidation(self):
        self.ready()
        w.execute(self.run, Fake(['impl', PASS_VALIDATION, 'DECISION: PASS', 'Interpretation']))
        extra = Path(self.temp.name) / 'input.txt'
        extra.write_text('5', encoding='utf-8')
        fake = Fake([PASS_VALIDATION, 'DECISION: PASS', 'New interpretation'])
        fake.args.artifact.append('input.txt')
        w.execute(self.run, fake)
        self.assertEqual(len(fake.prompts), 3)
        self.assertIn(str(extra), self.run.state['test_result']['artifacts'])
    def test_test_mutation_during_execution_is_not_passing_evidence(self):
        self.ready()
        self.run.record('implementation', 'Implementation', STUB)
        w.run_test(self.run, shlex.join([sys.executable, '-c', "from pathlib import Path; Path('answer.py').write_text('changed')"]), ['answer.py', 'test_answer.py'])
        self.assertFalse(w.test_passes(self.run))
    def test_failed_test_launch_invalidates_previous_acceptance_evidence(self):
        self.ready()
        w.execute(self.run, Fake(['impl', PASS_VALIDATION, 'DECISION: PASS', 'Interpretation']))
        with self.assertRaises(w.WorkflowError):
            w.run_test(self.run, '/nonexistent/workflow-test-command', ['answer.py', 'test_answer.py'])
        reloaded = w.Run(self.run.path)
        self.assertFalse(w.test_passes(reloaded))
        self.assertFalse(reloaded.valid('review'))
    def research_fixture(self, status):
        old = {'interaction_id': 'old-lower-id', 'requested_model': w.MAP['lower']['gemini'][0],
               'status': status, 'execution': 'test_stub'}
        if status == 'completed':
            text = 'Lower-mode literature'
            (self.run.path / 'research.md').write_text(text, encoding='utf-8')
            old['sha256'] = w.digest(text)
        self.run.state['research'] = old
        self.run.save()
    def test_completed_research_mode_change_archives_labeled_report(self):
        self.research_fixture('completed')
        self.run.set_mode('higher')
        self.assertNotIn('research', self.run.state)
        archive = self.run.state['research_history'][0]
        self.assertEqual(archive['interaction_id'], 'old-lower-id')
        self.assertEqual(archive['requested_model'], w.MAP['lower']['gemini'][0])
        self.assertEqual((self.run.path / archive['report_path']).read_text(encoding='utf-8'), 'Lower-mode literature')
        self.assertFalse((self.run.path / 'research.md').exists())
        self.assertFalse(archive['remote_cancelled'])
    def test_in_progress_mode_mismatch_starts_requested_model_not_old_id(self):
        self.research_fixture('in_progress')
        self.run.state['mode'] = 'higher'  # Also defend against an older run whose mode was edited directly.
        args = types.SimpleNamespace(allow_external=True, allow_research_cost=True, env_file=None, timeout=5)
        provider = w.Providers(self.run, args)
        result = types.SimpleNamespace(id='new-higher-id', status='completed', steps=[{'content': [{'text': 'Higher research'}]}])
        interactions = mock.Mock()
        interactions.create.return_value = result
        google = types.ModuleType('google')
        google.genai = types.SimpleNamespace(Client=mock.Mock(return_value=types.SimpleNamespace(interactions=interactions)))
        with mock.patch.dict(sys.modules, {'google': google}):
            provider.research()
        interactions.get.assert_not_called()
        self.assertEqual(interactions.create.call_args.kwargs['agent'], w.MAP['higher']['gemini'][0])
        self.assertEqual(self.run.state['research']['interaction_id'], 'new-higher-id')
        archive = self.run.state['research_history'][0]
        self.assertEqual(archive['interaction_id'], 'old-lower-id')
        self.assertTrue(archive['remote_may_continue'])
        self.assertFalse(archive['remote_cancelled'])
    def test_research_after_mode_change_still_requires_cost_consent(self):
        self.research_fixture('completed')
        self.run.set_mode('higher')
        args = types.SimpleNamespace(allow_external=True, allow_research_cost=False, env_file=None, timeout=5)
        with self.assertRaises(w.WorkflowError):
            w.Providers(self.run, args).research()
        self.assertNotIn('research', self.run.state)
    def test_windows_process_tree_termination_and_fallback(self):
        proc = mock.Mock(pid=123)
        with mock.patch.object(w.os, 'name', 'nt'), mock.patch.object(w.subprocess, 'run', return_value=types.SimpleNamespace(returncode=0)) as terminate:
            w.terminate_process_tree(proc)
            self.assertEqual(terminate.call_args.args[0], ['taskkill', '/PID', '123', '/T', '/F'])
            proc.kill.assert_not_called()
        with mock.patch.object(w.os, 'name', 'nt'), mock.patch.object(w.subprocess, 'run', side_effect=OSError):
            w.terminate_process_tree(proc)
            proc.kill.assert_called_once()
    def test_acceptance_requires_all_evidence(self):
        self.ready()
        self.run.record('acceptance', 'DECISION: PASS', STUB)
        with self.assertRaises(w.WorkflowError):
            self.run.accept('accept', 'Human reviewed the observed results')

if __name__ == '__main__':
    unittest.main()
