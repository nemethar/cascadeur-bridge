import bpy
from .. import icons


def draw_cascadeur_to_blender_settings(layout, context):
    addon_props = context.scene.cbb_settings

    layout.prop(addon_props.file_format, "cbb_cascadeur_to_blender")

    if addon_props.file_format.cbb_cascadeur_to_blender == "fbx":
        _draw_fbx_settings(layout, addon_props)

    elif addon_props.file_format.cbb_cascadeur_to_blender == "glb":
        row = layout.row(align=True)
        row.label(
            text="Not implemented yet.",
            icon="STATUS_WARNING_FILLED",
        )

    _draw_settings_buttons(layout)


def _draw_fbx_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_cascadeur_export(row.column(align=True), addon_props)
    _draw_blender_import(row.column(align=True), addon_props)


def _draw_cascadeur_export(layout, addon_props):
    box = layout.box()
    box.label(
        text="Cascadeur Export",
        icon_value=icons.get_icon_id("cascadeur"),
    )

    col = box.column(align=True)
    row = col.row()
    row.scale_y = 1.2
    row.prop(addon_props.cascadeur_fbx_export, "cbb_export_methods")
    col.separator(factor=1.5)
    col.prop(
        addon_props.cascadeur_fbx_export,
        "cbb_csc_apply_euler_filter",
    )
    col.prop(
        addon_props.cascadeur_fbx_export,
        "cbb_csc_up_axis",
    )
    col.prop(
        addon_props.cascadeur_fbx_export,
        "cbb_csc_bake_animation",
    )


def _draw_blender_import(layout, addon_props):
    box = layout.box()
    box.label(text="Blender Import", icon="BLENDER")

    _draw_blender_transform(box, addon_props)
    _draw_blender_animation(box, addon_props)
    _draw_blender_armature(box, addon_props)


def _draw_blender_transform(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Transform")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_import

    col.prop(settings, "cbb_import_global_scale")
    col.prop(settings, "cbb_import_apply_transform")
    col.prop(settings, "cbb_import_manual_orientation")
    col.prop(settings, "cbb_import_axis_forward")
    col.prop(settings, "cbb_import_axis_up")


def _draw_blender_animation(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Animation")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_import

    col.prop(settings, "cbb_import_use_anim")
    col.prop(settings, "cbb_import_anim_offset")


def _draw_blender_armature(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Armature")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_import

    col.prop(settings, "cbb_import_ignore_leaf_bones")
    col.prop(settings, "cbb_import_force_connect_children")
    col.prop(settings, "cbb_import_automatic_bone_orientation")
    col.prop(settings, "cbb_import_primary_bone_axis")
    col.prop(settings, "cbb_import_secondary_bone_axis")
    col.prop(settings, "cbb_import_use_prepost_rot")


def _draw_settings_buttons(layout):
    layout.separator()

    row = layout.row(align=True)

    row.operator(
        "cbb.save_fbx_settings",
        text="Save Settings",
        icon="FAKE_USER_ON",
    )

    row.operator(
        "cbb.reset_fbx_settings",
        text="Reset Settings",
        icon="FILE_REFRESH",
    )
