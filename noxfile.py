import os
import subprocess

import nox

try:
    MICROMAMBA = subprocess.check_output(["type", "-p", "micromamba"]).strip().decode()
except:
    MICROMAMBA = None

if MICROMAMBA:
    BIN_DIR = os.path.join("build", "bin")
    CONDA = os.path.join(BIN_DIR, "conda")
    if not os.path.exists(CONDA):
        os.makedirs(BIN_DIR, exist_ok=True)
        os.link(MICROMAMBA, CONDA)
    os.environ["PATH"] = os.pathsep.join([BIN_DIR, os.environ["PATH"]])

# If on Mac OS X Silicon and you need to use Rosetta
# os.environ["CONDA_SUBDIR"] = "osx-64"

args = dict(python=["3.10", "3.11"])


@nox.session(venv_backend="conda", venv_params=["-c", "defaults"], **args)
def test(session):
    # The following fails with micromamba -- gets quoted to '"fftw>=0.3.10"'
    #session.conda_install("fftw>=0.3.10", channel="conda-forge")
    session.conda_install("fftw", channel="conda-forge")
    session.install("pyfftw>=0.13.1", "pytest")
    session.run("pytest", "tests")
