import bpy
from .. import icons


def draw_blender_to_cascadeur_settings(layout, context):
    addon_props = context.scene.cbb_settings

    layout.prop(addon_props.file_format, "cbb_blender_to_cascadeur")

    if addon_props.file_format.cbb_blender_to_cascadeur == "fbx":
        _draw_fbx_settings(layout, addon_props)

    elif addon_props.file_format.cbb_blender_to_cascadeur == "glb":
        row = layout.row(align=True)
        row.label(
            text="Not implemented yet.",
            icon="STATUS_WARNING_FILLED",
        )

    _draw_settings_buttons(layout)


def _draw_fbx_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_blender_export(row.column(align=True), addon_props)
    _draw_cascadeur_import(row.column(align=True), addon_props)


def _draw_blender_export(layout, addon_props):
    box = layout.box()
    box.label(text="Blender Export", icon="BLENDER")

    _draw_blender_include(box, addon_props)
    _draw_blender_transform(box, addon_props)
    _draw_blender_armature(box, addon_props)
    _draw_blender_animation(box, addon_props)


def _draw_blender_include(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Include")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_export

    col.prop(settings, "cbb_export_use_selection")
    col.prop(settings, "cbb_export_object_types")


def _draw_blender_transform(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Transform")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_export

    col.prop(settings, "cbb_export_global_scale")
    col.prop(settings, "cbb_export_axis_forward")
    col.prop(settings, "cbb_export_axis_up")
    col.prop(settings, "cbb_export_apply_transform")


def _draw_blender_armature(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Armature")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_export

    col.prop(settings, "cbb_export_primary_bone_axis")
    col.prop(settings, "cbb_export_secondary_bone_axis")
    col.prop(settings, "cbb_export_deform_only")
    col.prop(settings, "cbb_export_leaf_bones")


def _draw_blender_animation(layout, addon_props):
    subbox = layout.box()
    subbox.label(text="Animation")

    col = subbox.column(align=True)
    settings = addon_props.blender_fbx_export

    col.prop(settings, "cbb_export_bake_anim")
    col.prop(settings, "cbb_export_use_nla_strips")
    col.prop(settings, "cbb_export_use_all_actions")


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


def _draw_cascadeur_import(layout, addon_props):
    box = layout.box()
    box.label(text="Cascadeur Import", icon_value=icons.get_icon_id("cascadeur"))

    col = box.column(align=True)
    col.prop(addon_props.cascadeur_fbx_import, "cbb_import_methods")
    col.scale_y = 1.2
    col.separator(factor=1.5)
    col.label(
        text="Other import settings are not implemented yet!",
        icon="STATUS_WARNING_FILLED",
    )
