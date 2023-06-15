import numpy as np
import pyfftw
import timeit
import os


def test_fft():
    np.random.seed(2)
    A = np.random.normal(size=64).astype(complex)
    At = np.fft.fft(A)
    fftw = pyfftw.builders.fft(A, threads=os.cpu_count(), planner_effort="FFTW_MEASURE")
    At_ = fftw(A)
    t, t_ = [
        min(timeit.repeat("fft(A)", globals=dict(A=A, fft=fft), number=100))
        for fft in [np.fft.fft, fftw]
    ]
    assert np.allclose(At, At_)
    assert t_ < t
