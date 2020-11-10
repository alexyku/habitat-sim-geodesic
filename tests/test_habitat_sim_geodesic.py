import numpy as np

from habitat_sim_geodesic import (
    __version__,
    compute_geodesic_distance,
    is_navigable,
    habitat_to_mp3d,
    mp3d_to_habitat,
    snap_point,
)


def test_version():
    assert __version__ == "0.1.3"


def test_compute():
    assert np.isclose(
        compute_geodesic_distance(
            "17DRP5sb8fy",
            np.array([3.76632, 0.072447, 0.30173]),
            np.array([0.403801, 0.072447, -0.242499]),
        ),
        3.4097445011138916,
    )


def test_nav():
    assert is_navigable("17DRP5sb8fy", np.array([3.76632, 0.072447, 0.30173]),)


def test_snap():
    pt = np.array([3.76632, 0.072447, 0.30173])
    assert np.allclose(
        snap_point("17DRP5sb8fy", np.array([3.76632, 0.072447, 0.30173]),), pt
    )


def test_convert():
    pt = np.array([3.76632, 0.072447, 0.30173])

    assert np.allclose(pt, mp3d_to_habitat(habitat_to_mp3d(pt)))
