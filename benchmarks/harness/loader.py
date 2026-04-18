"""Dynamic loading of LCM message classes from the dimos_lcm tree."""

import importlib
import os
import sys


def _ensure_on_path() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    candidate = os.path.join(repo_root, "generated", "python_lcm_msgs")
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


def load_class(type_name: str):
    """Look up a generated LCM class by its underscore name.

    e.g. ``sensor_msgs_Image`` → ``lcm_msgs.sensor_msgs.Image.Image``
    """
    _ensure_on_path()
    parts = type_name.split("_")
    if len(parts) < 2:
        raise ValueError(f"type name {type_name!r} is not in <package>_<Class> form")
    # ROS packages contain underscores (std_msgs, sensor_msgs), so walk
    # right-to-left looking for the longest valid module path.
    for split in range(len(parts) - 1, 0, -1):
        pkg = "_".join(parts[:split])
        cls = "_".join(parts[split:])
        module_path = f"lcm_msgs.{pkg}.{cls}"
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            continue
        if hasattr(module, cls):
            return getattr(module, cls)
    raise ImportError(f"could not resolve LCM class for {type_name!r}")
