from bpy.utils import previews
import os

_preview_collections = {}


def register():
    pcoll = previews.new()

    icon_dir = os.path.join(os.path.dirname(__file__))

    icons = {
        "cascadeur": "cascadeur-icon.png",
        "github": "github-icon.png",
        "youtube": "youtube-icon.png",
    }

    for name, filename in icons.items():
        icon_path = os.path.join(icon_dir, filename)
        pcoll.load(name, icon_path, "IMAGE")

    _preview_collections["main"] = pcoll


def unregister():
    for pcoll in _preview_collections.values():
        previews.remove(pcoll)

    _preview_collections.clear()


def get_icon_id(name):
    return _preview_collections["main"][name].icon_id
