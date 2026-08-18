import bpy
from .. import icons


def draw_blender_to_cascadeur_settings(layout, context):
    addon_props = context.scene.cbb_settings

    row = layout.row(align=False)
    split = row.split(factor=0.75, align=False)

    # Left side
    left = split.row()
    left.prop(
        addon_props.file_format,
        "cbb_blender_to_cascadeur",
    )

    # Right side
    right = split.row()
    right.alignment = "RIGHT"
    right.alert = True
    right.operator(
        "cbb.reset_fbx_settings",
        text="Reset Settings",
        icon="FILE_REFRESH",
    )

    if addon_props.file_format.cbb_blender_to_cascadeur == "fbx":
        _draw_fbx_settings(layout, addon_props)

    elif addon_props.file_format.cbb_blender_to_cascadeur == "glb":
        row = layout.row(align=True)
        row.label(
            text="Not implemented yet.",
            icon="STATUS_WARNING_FILLED",
        )


def _draw_fbx_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_blender_export(row.column(align=True), addon_props)
    _draw_cascadeur_import(row.column(align=True), addon_props)


def _draw_blender_export(layout, addon_props):
    box = layout.box()
    box.label(text="Blender Export", icon="BLENDER")
    box.separator(type="LINE", factor=1.2)

    _draw_blender_path_mode(box, addon_props)
    _draw_blender_include(box, addon_props)
    _draw_blender_transform(box, addon_props)
    _draw_blender_geometry(box, addon_props)
    _draw_blender_armature(box, addon_props)
    _draw_blender_animation(box, addon_props)


def _draw_blender_path_mode(layout, addon_props):
    settings = addon_props.blender_fbx_export

    row = layout.row(align=True)
    row.prop(settings, "cbb_path_mode")
    sub = row.row(align=True)

    sub.enabled = settings.cbb_path_mode == "COPY"
    sub.prop(
        settings,
        "cbb_embed_textures",
        text="",
        icon="PACKAGE" if settings.cbb_embed_textures else "UGLYPACKAGE",
    )


def _draw_blender_include(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_export_include",
        default_closed=False,
    )
    header.label(text="Include")

    if panel:
        settings = addon_props.blender_fbx_export

        col = panel.column(align=True)
        col.prop(settings, "cbb_use_selection")
        col.prop(settings, "cbb_use_visible")
        col.prop(settings, "cbb_use_active_collection")
        col.prop(settings, "cbb_object_types")
        col.prop(settings, "cbb_use_custom_props")
        col.separator(type="LINE")


def _draw_blender_transform(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_export_transform",
        default_closed=False,
    )

    header.label(text="Transform")

    if panel:
        settings = addon_props.blender_fbx_export

        col = panel.column(align=True)
        col.prop(settings, "cbb_global_scale")
        col.prop(settings, "cbb_apply_scale_options")
        col.prop(settings, "cbb_axis_forward")
        col.prop(settings, "cbb_axis_up")
        col.prop(settings, "cbb_apply_unit_scale")
        col.prop(settings, "cbb_use_space_transform")
        col.prop(settings, "cbb_apply_transform")
        col.separator(type="LINE")


def _draw_blender_geometry(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_export_geometry",
        default_closed=True,
    )

    header.label(text="Geometry")

    if panel:
        settings = addon_props.blender_fbx_export

        col = panel.column(align=True)
        col.prop(settings, "cbb_mesh_smooth_type")
        col.prop(settings, "cbb_use_subsurf")
        col.prop(settings, "cbb_use_mesh_modifiers")
        col.prop(settings, "cbb_use_mesh_edges")
        col.prop(settings, "cbb_use_triangles")
        col.prop(settings, "cbb_use_tspace")
        col.prop(settings, "cbb_colors_type")
        col.prop(settings, "cbb_prioritize_active_color")
        col.separator(type="LINE")


def _draw_blender_armature(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_export_armature",
        default_closed=True,
    )

    header.label(text="Armature")

    if panel:
        settings = addon_props.blender_fbx_export

        col = panel.column(align=True)
        col.prop(settings, "cbb_primary_bone_axis")
        col.prop(settings, "cbb_secondary_bone_axis")
        col.prop(settings, "cbb_armature_nodetype")
        col.prop(settings, "cbb_deform_only")
        col.prop(settings, "cbb_leaf_bones")
        col.separator(type="LINE")


def _draw_blender_animation(layout, addon_props):
    header, panel = layout.panel(
        "cbb_blender_export_animation",
        default_closed=True,
    )
    settings = addon_props.blender_fbx_export

    header.use_property_split = False
    header.prop(settings, "cbb_bake_anim", text="")
    header.label(text="Animation")

    if panel:
        col = panel.column(align=True)
        col.prop(settings, "cbb_bake_anim_use_all_bones")
        col.prop(settings, "cbb_use_nla_strips")
        col.prop(settings, "cbb_use_all_actions")
        col.prop(settings, "cbb_bake_anim_force_startend_keying")
        col.prop(settings, "cbb_bake_anim_step")
        col.prop(settings, "cbb_bake_anim_simplify_factor")


def _draw_cascadeur_import(layout, addon_props):
    box = layout.box()
    box.label(text="Cascadeur Import", icon_value=icons.get_icon_id("cascadeur"))
    box.separator(type="LINE", factor=1.2)

    col = box.column(align=True)
    col.prop(addon_props.cascadeur_fbx_import, "cbb_import_methods")
    col.scale_y = 1.2
    col.separator(factor=1.5)
    col.label(
        text="Other import settings are not implemented yet!",
        icon="STATUS_WARNING_FILLED",
    )
