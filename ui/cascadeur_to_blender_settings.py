import bpy
from .. import icons


def draw_cascadeur_to_blender_settings(layout, context):
    addon_props = context.scene.cbb_settings

    row = layout.row(align=False)
    split = row.split(factor=0.75, align=False)

    # Left side
    left = split.row()
    left.prop(
        addon_props.cascadeur_to_blender,
        "cbb_file_format",
    )

    # Right side
    right = split.row()
    right.alignment = "RIGHT"
    right.alert = True
    props = right.operator(
        "cbb.reset_settings",
        text="Reset Settings",
        icon="FILE_REFRESH",
    )
    props.reset_group = "CASCADEUR_TO_BLENDER"

    if addon_props.cascadeur_to_blender.cbb_file_format == "fbx":
        _draw_fbx_settings(layout, addon_props)

    elif addon_props.cascadeur_to_blender.cbb_file_format == "glb":
        _draw_glb_settings(layout, addon_props)


# FBX


def _draw_fbx_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_cascadeur_fbx_export(row.column(align=True), addon_props)
    _draw_blender_fbx_import(row.column(align=True), addon_props)


def _draw_cascadeur_fbx_export(layout, addon_props):
    box = layout.box()
    box.label(
        text="Cascadeur Export",
        icon_value=icons.get_icon_id("cascadeur"),
    )
    box.separator(type="LINE", factor=1.2)

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


def _draw_blender_fbx_import(layout, addon_props):
    box = layout.box()
    box.label(text="Blender Import", icon="BLENDER")
    box.separator(type="LINE", factor=1.2)

    _draw_blender_include(box, addon_props)
    _draw_blender_transform(box, addon_props)
    _draw_blender_materials(box, addon_props)
    _draw_blender_animation(box, addon_props)
    _draw_blender_armature(box, addon_props)


def _draw_blender_include(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_import_include",
        default_closed=False,
    )
    header.label(text="Include")

    if panel:
        settings = addon_props.blender_fbx_import

        col = panel.column(align=True)
        col.prop(settings, "cbb_use_custom_normals")
        col.prop(settings, "cbb_use_subsurf")
        col.prop(settings, "cbb_use_custom_props")
        col.prop(settings, "cbb_use_custom_props_enum_as_string")
        col.prop(settings, "cbb_use_image_search")
        col.prop(settings, "cbb_colors_type")
        col.separator(type="LINE")


def _draw_blender_transform(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_import_transform",
        default_closed=False,
    )
    header.label(text="Transform")

    if panel:
        settings = addon_props.blender_fbx_import

        col = panel.column(align=True)
        col.prop(settings, "cbb_global_scale")
        col.prop(settings, "cbb_decal_offset")
        col.prop(settings, "cbb_bake_space_transform")
        col.prop(settings, "cbb_use_prepost_rot")

        # Manual Orientation sub panel
        header_orientation, panel_orientation = panel.panel(
            "cbb_blender_import_transform_orientation",
            default_closed=False,
        )
        header_orientation.use_property_split = False
        header_orientation.prop(settings, "cbb_use_manual_orientation", text="")
        header_orientation.label(text="Manual Orientation")

        if panel_orientation:
            panel_orientation.enabled = settings.cbb_use_manual_orientation
            panel_orientation.prop(settings, "cbb_axis_forward")
            panel_orientation.prop(settings, "cbb_axis_up")
            panel_orientation.separator(type="LINE")
        else:
            panel.separator(type="LINE")


def _draw_blender_materials(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_import_materials",
        default_closed=True,
    )
    header.label(text="Materials")

    if panel:
        settings = addon_props.blender_fbx_import

        col = panel.column(align=True)
        col.prop(settings, "cbb_mtl_name_collision_mode")
        col.separator(type="LINE")


def _draw_blender_animation(layout, addon_props):
    settings = addon_props.blender_fbx_import

    header, panel = layout.panel(
        "cbb_blender_import_animation",
        default_closed=True,
    )
    header.use_property_split = False
    header.prop(settings, "cbb_use_anim", text="")
    header.label(text="Animation")

    if panel:
        col = panel.column(align=True)
        col.prop(settings, "cbb_anim_offset")
        col.separator(type="LINE")


def _draw_blender_armature(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_import_armature",
        default_closed=True,
    )
    header.label(text="Armature")

    if panel:
        settings = addon_props.blender_fbx_import

        col = panel.column(align=True)
        col.prop(settings, "cbb_ignore_leaf_bones")
        col.prop(settings, "cbb_force_connect_children")
        col.prop(settings, "cbb_automatic_bone_orientation")
        col.prop(settings, "cbb_primary_bone_axis")
        col.prop(settings, "cbb_secondary_bone_axis")


# GLB


def _draw_glb_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_cascadeur_glb_export(row.column(align=True), addon_props)
    _draw_blender_glb_import(row.column(align=True), addon_props)


def _draw_cascadeur_glb_export(layout, addon_props):
    box = layout.box()
    box.label(
        text="Cascadeur Export",
        icon_value=icons.get_icon_id("cascadeur"),
    )
    box.separator(type="LINE", factor=1.2)

    settings = addon_props.cascadeur_glb_export

    # Preset
    row = box.row(align=True)
    row.prop(settings, "cbb_preset")

    # Cascadeur import options
    col = box.column(align=True)
    col.prop(settings, "cbb_for_selected_interval")
    col.prop(settings, "cbb_for_selected_objects")
    col.prop(settings, "cbb_include_animation")

    # Scale factor
    col = box.column(align=True)
    col.prop(settings, "cbb_use_scale_factor")

    row = col.row(align=True)
    row.enabled = settings.cbb_use_scale_factor
    row.prop(settings, "cbb_scale_factor")

    # Mesh options
    col = box.column(align=True)
    col.prop(settings, "cbb_call_process_skinned_mesh")
    col.prop(settings, "cbb_translate_meshes_primitive_attributes")
    col.prop(settings, "cbb_rotate_meshes_primitive_attributes")
    col.prop(settings, "cbb_scale_meshes_primitive_attributes")


def _draw_blender_glb_import(layout, addon_props):
    box = layout.box()
    box.label(text="Blender Import", icon="BLENDER")
    box.separator(type="LINE", factor=1.2)

    col = box.column(align=True)
    row = col.row()

    row.label(
        text="Not implemented yet.",
        icon="STATUS_WARNING_FILLED",
    )

    # _draw_blender_include(box, addon_props)
