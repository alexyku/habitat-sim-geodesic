from pathlib import Path
import collections
import os.path as osp

import cppimport.import_hook

from habitat_sim_geodesic.bindings import PathFinder, ShortestPath


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GeodesicDistanceComputer(metaclass=Singleton):
    ROOT_DIR = Path(__file__).parent.absolute()
    NAVMESH_DIR = ROOT_DIR.joinpath("navmeshes")

    def __init__(self):
        self._pathfinders = collections.OrderedDict()
        self._cache_size = 1

    def _get_pathfinder(self, scene_id: str) -> PathFinder:
        scene_name = osp.splitext(osp.basename(scene_id))[0]

        if scene_name not in self._pathfinders:
            if len(self._pathfinders) == self._cache_size:
                self._pathfinders.popitem(last=True)

            navmesh = self.NAVMESH_DIR.joinpath(scene_name + ".navmesh")
            pf = PathFinder()
            pf.load_nav_mesh(str(navmesh))

            if not pf.is_loaded:
                raise RuntimeError(
                    f"Could not find navmesh to load for scene_id '{scene_id}'\n"
                    + f"Tried to load from '{navmesh}'"
                )

            self._pathfinders[scene_name] = pf

        self._pathfinders.move_to_end(scene_name, last=False)
        return self._pathfinders[scene_name]

    def compute_distance(self, scene_id, start_pt, end_pt):
        path = ShortestPath()
        path.requested_start = start_pt
        path.requested_end = end_pt

        self._get_pathfinder(scene_id).find_path(path)

        return path.geodesic_distance

    def is_navigable(self, scene_id, pt):
        return self._get_pathfinder(scene_id).is_navigable(pt)

    def snap_point(self, scene_id, pt):
        return self._get_pathfinder(scene_id).snap_point(pt)


def compute_geodesic_distance(scene_id, start_pt, end_pt):
    r"""Comptues the geodesic distance between two points

    :param scene_id: The ID of the scene to compute the distance in.
        Assumes scene_id is a file name in the format /anything/<scene_name>.<ext>
        where <scene_name> is the hash name of an mp3d scene. i.e. `17DRP5sb8fy`

        Note that providing the hash name directly will also work

    :param start_pt: The starting point.  Assumed to already be in habitat's coordinate frame
    :param end_pt: The ending point. Assumed to already be in habitat's coordinate frame

    :return: The geodesic distance between the two points
    """
    print(scene_id, start_pt, end_pt)
    return GeodesicDistanceComputer().compute_distance(scene_id, start_pt, end_pt)


def is_navigable(scene_id, pt):
    return GeodesicDistanceComputer().is_navigable(scene_id, pt)


def snap_point(scene_id, pt):
    return GeodesicDistanceComputer().snap_point(scene_id, pt)
