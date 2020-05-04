"""
Classes and functions for generating QC metrics.
"""
import os
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from datman.utils import run, make_temp_directory, nifti_basename
from datman.exceptions import QCException


@dataclass
class QCOutput:
    order: int = -1
    title: str = None
    caption: str = None


class Metric(ABC):

    requires = {
        'images': ['slicer'],
        'montage': ['slicer', 'pngappend']
    }

    @abstractmethod
    def input(self):
        pass

    @abstractmethod
    def output_root(self):
        pass

    @abstractmethod
    def outputs(self):
        pass

    @property
    def manifest_path(self):
        return self.output_root + "_manifest.json"

    def __init__(self, input_nii, output_dir, overwrite=False):
        self.input = input_nii
        self.output_root = os.path.join(output_dir, nifti_basename(input_nii))
        self.outputs = self.set_outputs()
        self.write_manifest(overwrite)

    def write_manifest(self, overwrite=False):
        if os.path.exists(self.manifest_path):
            if not overwrite:
                return
            orig = self.read_json()
        else:
            orig = {}

        manifest = self.make_manifest()

        if orig != manifest:
            self.write_json(manifest)

    def write_json(self, contents):
        with open(self.manifest_path, "w") as fh:
            json.dump(contents, fh, indent=4)

    def read_json(self):
        with open(self.manifest_path, "r") as fh:
            contents = json.load(fh)
        return contents

    def make_manifest(self):
        manifest = {}
        for command in self.outputs:
            for file_path in self.outputs[command]:
                output = self.outputs[command][file_path]
                if output:
                    manifest[file_path] = vars(output)
        return manifest

    def get_requirements(self):
        requires = []
        for command in self.outputs:
            try:
                found = self.requires[command]
            except KeyError:
                found = [command]
            requires.extend(found)
        return requires

    def set_outputs(self):
        outputs = {}
        for command in self.outputs:
            outputs[command] = {}
            for ending in self.outputs[command]:
                full_path = os.path.join(self.output_root + ending)
                outputs[command][full_path] = self.outputs[command][ending]
        return outputs

    def exists(self):
        for command in self.commands:
            if not self.command_succeeded(command)[0]:
                return False
        if not os.path.exists(self.manifest_path):
            return False
        return True

    def command_succeeded(self, command_name):
        if command_name not in self.commands:
            return os.path.isfile(command_name), command_name

        for output in self.commands[command_name]:
            if not os.path.exists(output):
                return False, output
        return True, None

    def run(self, command, output):
        """Run a command if outputs are still needed.

        Args:
            command (str): The exact string command to run.
            output (str): A command name (as defined in self.commands) or a
                full path to a single file.

        Raises:
            QCException: If any expected outputs haven't been generated.
        """
        if self.command_succeeded(output)[0]:
            return

        run(command)

        success, last_output = self.command_succeeded(output)
        if not success:
            raise QCException(
                f"Failed generating {last_output} with command '{command}'")

    def make_image(self, output, img_gap=2, width=1600, nii_input=None):
        """
        Uses FSL's slicer function to generate a png from a nifti file.

        Args:
            output (str): The full path to write the output image to
            img_gap (int, optional): Size of the "gap" to insert between
                slices. Defaults to 2.
            width (int, optional): width (in pixels) of output image.
                Defaults to 1600.
            nii_input (str, optional): The nifti image to visualize. If not
                given, self.input will be used.
        """
        if not nii_input:
            nii_input = self.input
        self.run(f"slicer {nii_input} -S {img_gap} {width} {output}", output)

    def make_montage(self, output):
        """
        Uses FSL's slicer function to generate a montage of three slices from
        each direction that matches FSL's slicesdir output.

        Args:
            output (str): The full path to write the result to.
        """
        if os.path.isfile(output):
            return

        with make_temp_directory() as temp:
            img_command = "slicer {0} -s 1 "\
                "-x 0.4 {1}/grota.png "\
                "-x 0.5 {1}/grotb.png "\
                "-x 0.6 {1}/grotc.png "\
                "-y 0.4 {1}/grotd.png "\
                "-y 0.5 {1}/grote.png "\
                "-y 0.6 {1}/grotf.png "\
                "-z 0.4 {1}/grotg.png "\
                "-z 0.5 {1}/groth.png "\
                "-z 0.6 {1}/groti.png"\
                .format(self.input, temp)
            run(img_command)

            montage_command = "pngappend {0}/grota.png + {0}/grotb.png + "\
                "{0}/grotc.png + {0}/grotd.png + {0}/grote.png + "\
                "{0}/grotf.png + {0}/grotg.png + {0}/groth.png + "\
                "{0}/groti.png {1}"\
                .format(temp, output)
            run(montage_command)

        if not os.path.isfile(output):
            raise QCException(f"Failed generating montage {output}")


class DTIMetrics(Metric):
    input = None
    output_root = None
    outputs = {
        'montage': {
            '_montage.png': QCOutput(1)
        },
        'images': {
            '_b0.png': QCOutput(2, 'b0 Montage')
        },
        'qc-dti': {
            '_stats.csv': None,
            '_directions.png': QCOutput(3, 'bvec Directions')
        },
        'qc-spikecount': {
            '_spikecount.csv': None
        }
    }

    def __init__(self, nii_input, output_dir):
        input_root = os.path.join(os.path.basename(nii_input),
                                  nifti_basename(nii_input))
        bvec = input_root + ".bvec"
        bval = input_root + ".bval"
        if not os.path.exists(bvec) or not os.path.exists(bval):
            raise QCException(f"Can't process {nii_input} - bvec or bval file "
                              "missing.")

        super().__init__(nii_input, output_dir)

    def generate(self, img_gap=None, width=None):
        self.run(f"qc-dti {self.input} {self.bvec} {self.bval} "
                 f"{self.output_root + '_stats.csv'}", 'qc-dti')

        self.run(f"qc-spikecount {self.input} "
                 f"{self.output_root + '_spikecount.csv'} {self.bval}")

        self.make_montage(self.output_root + "_montage.png")
        self.make_image(self.output_root + "_b0.png", img_gap, width)


class AnatMetrics(Metric):
    input = None
    output_root = None
    outputs = {
        'images': {
            '.png': QCOutput(1)
        }
    }

    def generate(self, img_gap=5, width=None):
        self.make_image(self.output_root + ".png", img_gap, width)


class FMRIMetrics(Metric):
    input = None
    output_root = None
    outputs = {
        'qc-scanlength': {
            '_scanlengths.csv': None
        },
        'qc-fmri': {
            '_stats.csv': None,
            '_sfnr.nii.gz': None,
            '_corr.nii.gz': None
        },
        'montage': {
            '_montage.png': QCOutput(1),
        },
        'images': {
            '_raw.png': QCOutput(2, 'BOLD Montage'),
            '_sfnr.png': QCOutput(3, 'SFNR Map'),
            '_corr.nii.gz': QCOutput(4, 'Correlation Map')
        }
    }

    def generate(self, img_gap=None, width=None):
        scanlengths = self.output_root + "_scanlengths.csv"
        self.run(f"qc-scanlength {self.input} {scanlengths}", "qc-scanlength")

        stats = self.output_root + "_stats.csv"
        self.run(f"qc-fmri {self.input} {stats}", "qc-fmri")

        self.make_montage(self.output_root + "_montage.png")
        self.make_image(self.output_root + "_raw.png", img_gap, width)
        self.make_image(self.output_root + "_sfnr.png",
                        img_gap,
                        width,
                        nii_input=self.output_root + "_sfnr.nii.gz")
        self.make_image(self.output.root + "_corr.png",
                        img_gap,
                        width,
                        nii_input=self.output_root + "_corr.nii.gz")
