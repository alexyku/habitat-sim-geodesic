import numpy as np

from habitat_sim_geodesic import (
    __version__,
    compute_geodesic_distance,
    is_navigable,
    habitat_to_mp3d,
    mp3d_to_habitat,
)


def test_version():
    assert __version__ == "0.1.2"


def test_compute():
    compute_geodesic_distance(
        "17DRP5sb8fy",
        np.array([3.76632, 0.072447, 0.30173]),
        np.array([0.403801, 0.072447, -0.242499]),
    )


def test_compute():
    assert is_navigable("17DRP5sb8fy", np.array([3.76632, 0.072447, 0.30173]),)


def test_convert():
    pt = np.array([3.76632, 0.072447, 0.30173])

    assert np.allclose(pt, mp3d_to_habitat(habitat_to_mp3d(pt)))
