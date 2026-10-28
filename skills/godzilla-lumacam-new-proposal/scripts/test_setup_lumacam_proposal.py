"""Isolated proposal setup tests: no detector, live proposal, notebook, or email."""
import contextlib
import configparser
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import setup_lumacam_proposal as setup


class ProposalSetupLayoutTests(unittest.TestCase):
    def fixture(self, base, spelling):
        repo = base / "repo"
        template = repo / "lumacam_proposal_template"
        for name in ("tpx3Files", "final", "derived", "logs", "metadata", ".work"):
            (template / "data" / spelling / name).mkdir(parents=True)
        (template / "documentation").mkdir()
        for name in ("experiment_log.md", "measurement_protocol.md"):
            (template / "documentation" / name).write_text("test")
        (repo / "python").mkdir()
        (repo / "python/settings_installation.py").write_text(
            "config_pixel_path = '/old/settings.bpc'\nconfig_dacs_path = '/old/settings.bpc.dacs'\n")
        (repo / "acquisitionSettings.sh").write_text("LUMACAM_PROPOSAL_DIR='/old/proposal'\n")
        (repo / "monitor_dataAcq_sumImages.py").write_text("DEFAULT_EMAIL_TO = 'old@example.org'\n")
        (repo / "parameterSettings.json").write_text('{}')
        photon = base / "photon"
        photon.mkdir()
        (photon / "tpxAcqPhotonTest.py").write_text(
            "requests.get('http://localhost/config/load?format=pixelconfig', params={'file': '/old/settings.bpc'})\n"
            "requests.get('http://localhost/config/load?format=dacs', params={'file': '/old/settings.bpc.dacs'})\n")
        calib = base / "calib"
        calib.mkdir()
        (calib / "settings.bpc").write_bytes(b'pixel')
        (calib / "settings.bpc.dacs").write_bytes(b'dacs')
        notebook = base / "focus.ipynb"
        notebook.write_text(json.dumps({"cells": [{"cell_type": "code", "source": [
            "from pathlib import Path\n", "series_dir = Path('/old')\n",
            "cache_dir = Path('/old/cache')\n", "output_csv = Path('/old/result.csv')\n"]}]}))
        data = base / "data"
        data.mkdir()
        args = ["--repository", str(repo), "--proposal", "campaign",
            "--data-base", str(data), "--calibration-dir", str(calib),
            "--email-to", "tester@example.org", "--photon-test-root", str(photon),
            "--batch-focus-notebook", str(notebook)]
        return repo, data / "campaign", notebook, args

    def test_setup_and_focus_paths_follow_actual_template_root(self):
        for spelling in ("experiment", "experiments"):
            with self.subTest(spelling=spelling), tempfile.TemporaryDirectory() as tmp:
                repo, proposal, notebook, args = self.fixture(Path(tmp), spelling)
                with patch.object(setup, "detector_warnings", return_value=[]), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(setup.main(args), 0)
                root = proposal / "data" / spelling
                self.assertTrue((root / "tpx3Files").is_dir())
                self.assertEqual(setup.validate_template(proposal), root)
                cells = json.loads(notebook.read_text())["cells"]
                namespace = {}
                exec(''.join(cells[0]["source"]), namespace)
                self.assertEqual(namespace["series_dir"], root / "tpx3Files")
                self.assertEqual(namespace["cache_dir"], root / ".work/batch_focus_cache")
                self.assertEqual(namespace["output_csv"], proposal / "documentation/batch_focus_summary.csv")
                self.assertIn(str(proposal), (repo / "acquisitionSettings.sh").read_text())
                self.assertIn("tester@example.org", (repo / "monitor_dataAcq_sumImages.py").read_text())
                config_path = proposal / "analysis/lumacam_pipeline.ini"
                setup.validate_pipeline_config(config_path, proposal)
                parser = configparser.ConfigParser()
                parser.read(config_path)
                self.assertEqual(parser["project"]["data_path"], str(proposal))
                self.assertEqual(parser["electrochemistry"]["path"], str(proposal / "data/echem"))
                beam_path = str(proposal / "data/beamhistory")
                self.assertEqual(parser["corrections"]["beamhistory_path"], beam_path)
                self.assertEqual(parser["corrections"]["reference_beamhistory_path"], beam_path)
                self.assertFalse(parser.getboolean("background", "enabled"))
                for section, keys in {
                    "project": ("experiment", "variant", "result_root", "analysis_name"),
                    "corrections": ("reference_dir", "prepared_reference_path", "file_filter"),
                    "background": ("background_path",),
                    "shared_setup": ("reference_set", "ob_experiment", "background_experiment",
                        "reference_source_path", "prepared_reference_path",
                        "prepared_background_path", "metadata_path"),
                }.items():
                    for key in keys:
                        self.assertEqual(parser[section][key], "", (section, key))
                self.assertFalse((root / "metadata/layout.json").exists())

    def test_template_campaign_settings_are_not_inherited(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            template_config = repo / "lumacam_proposal_template/analysis/lumacam_pipeline.ini"
            template_config.parent.mkdir()
            old_text = (
                "[project]\ndata_path = /old/campaign\nexperiment = exp999\n"
                "[shared_setup]\nob_experiment = ob999\nbackground_experiment = bg999\n"
                "[background]\nenabled = True\nbackground_path = /old/background.tiff\n"
            )
            template_config.write_text(old_text)
            with patch.object(setup, "detector_warnings", return_value=[]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(setup.main(args), 0)
            generated = proposal / "analysis/lumacam_pipeline.ini"
            setup.validate_pipeline_config(generated, proposal)
            self.assertNotIn("/old/", generated.read_text())
            self.assertEqual(template_config.read_text(), old_text)

    def test_existing_proposal_config_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            config = proposal / "analysis/lumacam_pipeline.ini"
            config.parent.mkdir(parents=True)
            config.write_text("[project]\nexperiment = exp123\n")
            originals = {p: p.read_bytes() for p in (config, notebook, repo / "acquisitionSettings.sh")}
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(setup.main(args), 1)
            self.assertEqual(originals, {p: p.read_bytes() for p in originals})

    def test_invalid_pipeline_template_targets_fail_before_writes(self):
        for relative in ("analysis", "data/beamhistory", "data/echem"):
            for kind in ("file", "symlink"):
                with self.subTest(relative=relative, kind=kind), tempfile.TemporaryDirectory() as tmp:
                    repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
                    target = repo / "lumacam_proposal_template" / relative
                    if kind == "file":
                        target.write_text("not a directory")
                    else:
                        outside = Path(tmp) / "outside"
                        outside.mkdir()
                        target.symlink_to(outside, target_is_directory=True)
                    before = notebook.read_bytes()
                    with contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(setup.main(args), 1)
                    self.assertFalse(proposal.exists())
                    self.assertEqual(notebook.read_bytes(), before)

    def test_config_write_failure_does_not_activate_new_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            originals = {p: p.read_bytes() for p in (notebook, repo / "acquisitionSettings.sh",
                repo / "python/settings_installation.py", repo / "monitor_dataAcq_sumImages.py")}
            with patch.object(setup, "atomic_write_text", side_effect=OSError("test write failure")), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(setup.main(args), 1)
            self.assertEqual(originals, {p: p.read_bytes() for p in originals})

    def test_config_paths_support_spaces_and_percent_characters(self):
        proposal = Path("/data01/beam time 100%/campaign")
        parser = configparser.ConfigParser()
        parser.read_string(setup.prepare_pipeline_config_text(proposal))
        self.assertEqual(parser["project"]["data_path"], str(proposal))
        self.assertEqual(parser["electrochemistry"]["path"], str(proposal / "data/echem"))

    def test_ambiguous_template_refused_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            (repo / "lumacam_proposal_template/data/experiments").mkdir()
            before = notebook.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(setup.main(args), 1)
            self.assertFalse(proposal.exists())
            self.assertEqual(notebook.read_bytes(), before)

    def test_dry_run_does_not_change_settings_or_create_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            originals = {p: p.read_bytes() for p in (notebook, repo / "acquisitionSettings.sh",
                repo / "python/settings_installation.py", repo / "monitor_dataAcq_sumImages.py")}
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(setup.main(args + ["--dry-run"]), 0)
            self.assertFalse(proposal.exists())
            self.assertEqual(originals, {p: p.read_bytes() for p in originals})
            self.assertIn(str(proposal / "analysis/lumacam_pipeline.ini"), output.getvalue())
            self.assertIn(str(proposal / "data/echem"), output.getvalue())
            self.assertIn(str(proposal / "data/beamhistory"), output.getvalue())





class SplitProposalSetupTests(unittest.TestCase):
    fixture = ProposalSetupLayoutTests.fixture
    def test_split_template_setup_keeps_raw_and_reduced_paths_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            template = repo / "lumacam_proposal_template"
            (template / "data/experiment/tpx3Files").rename(template / "raw")
            (template / "reduced").mkdir()
            for name in ("data", "documentation"):
                (template / name).rename(template / "reduced" / name)
            with patch.object(setup, "detector_warnings", return_value=[]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(setup.main(args), 0)
            self.assertEqual(setup.validate_template(proposal), proposal / "reduced/data/experiment")
            self.assertFalse((proposal / "reduced/data/experiment/tpx3Files").exists())
            namespace = {}
            exec(''.join(json.loads(notebook.read_text())["cells"][0]["source"]), namespace)
            self.assertEqual(namespace["series_dir"], proposal / "raw")
            self.assertEqual(namespace["cache_dir"], proposal / "reduced/data/experiment/.work/batch_focus_cache")
            self.assertEqual(namespace["output_csv"], proposal / "reduced/documentation/batch_focus_summary.csv")
            config = proposal / "reduced/analysis/lumacam_pipeline.ini"
            setup.validate_pipeline_config(config, proposal)
            parser = configparser.ConfigParser()
            parser.read(config)
            self.assertEqual(parser["project"]["data_path"], str(proposal))
            self.assertEqual(parser["electrochemistry"]["path"], str(proposal / "reduced/data/echem"))
            self.assertEqual(parser["corrections"]["beamhistory_path"], str(proposal / "reduced/data/beamhistory"))

    def test_mixed_split_and_old_template_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, proposal, notebook, args = self.fixture(Path(tmp), "experiment")
            (repo / "lumacam_proposal_template/reduced/data/experiment").mkdir(parents=True)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(setup.main(args), 1)
            self.assertFalse(proposal.exists())


if __name__ == "__main__":
    unittest.main()
