import bpy
import os

_preview_collections = {}


def register():
    pcoll = bpy.utils.previews.new()

    icon_path = os.path.join(
        os.path.dirname(__file__),
        "cascadeur-icon.png",
    )

    pcoll.load("cascadeur", icon_path, "IMAGE")

    _preview_collections["main"] = pcoll


def unregister():
    for pcoll in _preview_collections.values():
        bpy.utils.previews.remove(pcoll)

    _preview_collections.clear()


def get_icon_id(name):
    return _preview_collections["main"][name].icon_id
