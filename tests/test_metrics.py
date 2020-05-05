import os
from unittest.mock import patch

import pytest

import datman.metrics


class TestMetric:

    input_basename = "STUDY_SITE_SUBID_01_01"
    nii_input = f"/tmp/{input_basename}.nii.gz"
    output_dir = "/tmp/test_metrics/"

    def test_manifest_path_set_to_expected_output_name(self):
        fmri = datman.metrics.FMRIMetrics(self.nii_input, self.output_dir)

        expected = self.output_dir + self.input_basename + "_manifest.json"
        assert fmri.manifest_path == expected

    @patch("datman.metrics.open")
    @patch("os.path.exists")
    def test_manifest_not_written_when_exists(self, mock_exist, mock_fh):
        mock_exist.return_value = True
        fmri = datman.metrics.FMRIMetrics(self.nii_input, self.output_dir)
        fmri.write_manifest()

        assert mock_fh.call_count == 0

    @patch("datman.metrics.open")
    @patch("os.path.exists")
    def test_manifest_written_when_overwrite_given_or_file_doesnt_exist(
            self, mock_exists, mock_fh):
        fmri = datman.metrics.FMRIMetrics(self.nii_input, self.output_dir)
        manifest = fmri.manifest_path
        mock_exists.side_effect = lambda x: x != manifest
        fmri.write_manifest()

        expected_call = f"call('{manifest}', 'w')"

        assert mock_fh.call_count == 1
        assert str(mock_fh.call_args) == expected_call

        mock_fh.reset_mock()
        mock_exists.return_value = True
        fmri.write_manifest(overwrite=True)

        assert mock_fh.call_count == 1
        assert str(mock_fh.call_args) == expected_call

    @patch("os.path.exists")
    def test_exists_is_false_when_at_least_one_file_missing(self, mock_exist):
        fmri = datman.metrics.FMRIMetrics(self.nii_input, self.output_dir)
        outputs = self.get_outputs(fmri)

        mid = len(outputs) // 2
        mock_exist.side_effect = lambda x: x != outputs[mid]
        assert not fmri.exists()

        mock_exist.side_effect = lambda x: x != fmri.manifest_path
        assert not fmri.exists()

    @patch("os.path.exists")
    def test_exists_is_true_when_outputs_and_manifest_found(self, mock_exist):
        fmri = datman.metrics.FMRIMetrics(self.nii_input, self.output_dir)
        outputs = self.get_outputs(fmri)
        outputs.append(fmri.manifest_path)

        mock_exist.side_effect = lambda x: x in outputs

        assert fmri.exists()

    def test_dti_metric_raises_exception_if_bvec_or_bval_missing(self):
        bval = self.nii_input.replace(".nii.gz", ".bval")
        bvec = self.nii_input.replace(".nii.gz", ".bvec")

        assert not os.path.exists(bval)
        assert not os.path.exists(bvec)

        with pytest.raises(datman.exceptions.QCException):
            datman.metrics.DTIMetrics(self.nii_input, self.output_dir)

    @patch("datman.metrics.run")
    def test_is_runnable_returns_false_if_required_software_missing(
            self, mock_run):
        fmri = datman.metrics.FMRIMetrics(self.nii_input, self.output_dir)
        requires = fmri.get_requirements()

        mid = len(requires) // 2

        def mock_which(command):
            if "which" in command and command == f"which {requires[mid]}":
                return 1, b""
            return 0, b""

        mock_run.side_effect = mock_which
        assert not fmri.is_runnable()

    @patch("datman.metrics.run")
    def test_is_runnable_returns_true_if_requirements_met(self, mock_run):
        mock_run.return_value = (0, b"")

        anat = datman.metrics.AnatMetrics(self.nii_input, self.output_dir)
        assert anat.is_runnable()

    def get_outputs(self, metric):
        outputs = []
        for command in metric.outputs:
            outputs.extend(metric.outputs[command])
        return outputs
