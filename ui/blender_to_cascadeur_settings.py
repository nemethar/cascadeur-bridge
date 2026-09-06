import bpy
from .. import icons


def draw_blender_to_cascadeur_settings(layout, context):
    addon_props = context.scene.cbb_settings

    row = layout.row(align=False)
    split = row.split(factor=0.75, align=False)

    # Left side
    left = split.row()
    left.prop(
        addon_props.blender_to_cascadeur,
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
    props.reset_group = "BLENDER_TO_CASCADEUR"

    if addon_props.blender_to_cascadeur.cbb_file_format == "fbx":
        _draw_fbx_settings(layout, addon_props)

    elif addon_props.blender_to_cascadeur.cbb_file_format == "glb":
        _draw_glb_settings(layout, addon_props)


# FBX


def _draw_fbx_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_blender_fbx_export(row.column(align=True), addon_props)
    _draw_cascadeur_fbx_import(row.column(align=True), addon_props)


def _draw_blender_fbx_export(layout, addon_props):
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
        default_closed=True,
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
        default_closed=True,
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


def _draw_cascadeur_fbx_import(layout, addon_props):
    box = layout.box()
    box.label(text="Cascadeur Import", icon_value=icons.get_icon_id("cascadeur"))
    box.separator(type="LINE", factor=1.2)

    col = box.column(align=True)
    row = col.row()
    row.scale_y = 1.2
    row.prop(addon_props.cascadeur_fbx_import, "cbb_import_methods")

    col.separator(factor=1.5)
    col.prop(
        addon_props.cascadeur_fbx_import,
        "cbb_csc_up_axis",
    )


# GLB


def _draw_glb_settings(layout, addon_props):
    row = layout.row(align=True)

    _draw_blender_glb_export(row.column(align=True), addon_props)
    _draw_cascadeur_glb_import(row.column(align=True), addon_props)


def _draw_blender_glb_export(layout, addon_props):
    box = layout.box()
    box.label(text="Blender Export", icon="BLENDER")
    box.separator(type="LINE", factor=1.2)

    box.use_property_split = False
    box.use_property_decorate = False

    settings = addon_props.blender_glb_export

    _draw_glb_export_include_panel(box, settings)
    _draw_glb_export_transform_panel(box, settings)
    _draw_glb_export_data_panel(box, settings)
    _draw_glb_export_animation_panel(box, settings)


def _draw_glb_export_include_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_include",
        default_closed=True,
    )
    header.label(text="Include")

    if body:
        col = body.column(heading="Limit to", align=True)
        col.prop(settings, "cbb_selection")
        col.prop(settings, "cbb_visible")
        col.prop(settings, "cbb_renderable")
        col.prop(settings, "cbb_active_collection")

        if settings.cbb_active_collection:
            col.prop(settings, "cbb_active_collection_with_nested")

        col.prop(settings, "cbb_active_scene")

        col = body.column(heading="Data", align=True)
        col.prop(settings, "cbb_extras")
        col.prop(settings, "cbb_cameras")
        col.prop(settings, "cbb_lights")


def _draw_glb_export_transform_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_transform",
        default_closed=True,
    )
    header.label(text="Transform")

    if body:
        body.prop(settings, "cbb_yup")


def _draw_glb_export_data_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data",
        default_closed=True,
    )
    header.label(text="Data")

    if body:
        _draw_glb_export_scene_graph_panel(body, settings)
        _draw_glb_export_mesh_panel(body, settings)
        _draw_glb_export_material_panel(body, settings)
        _draw_glb_export_shapekeys_panel(body, settings)
        _draw_glb_export_armature_panel(body, settings)
        _draw_glb_export_skinning_panel(body, settings)
        _draw_glb_export_lighting_panel(body, settings)
        _draw_glb_export_draco_panel(body, settings)
        _draw_glb_export_meshopt_panel(body, settings)


def _draw_glb_export_scene_graph_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_scene_graph",
        default_closed=True,
    )
    header.label(text="Scene Graph")

    if body:
        body.prop(settings, "cbb_hierarchy_flatten_objs")
        body.prop(settings, "cbb_hierarchy_full_collections")


def _draw_glb_export_mesh_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_mesh",
        default_closed=True,
    )
    header.label(text="Mesh")

    if body:
        body.prop(settings, "cbb_apply")
        body.prop(settings, "cbb_texcoords")
        body.prop(settings, "cbb_normals")

        col = body.column()
        col.active = settings.cbb_normals
        col.prop(settings, "cbb_tangents")

        body.prop(settings, "cbb_attributes")
        body.prop(settings, "cbb_mesh_edges")
        body.prop(settings, "cbb_mesh_vertices")
        body.prop(settings, "cbb_shared_accessors")

        # Vertex Colors
        header, sub_body = body.panel(
            "CBB_GLB_export_data_vertex_color",
            default_closed=True,
        )
        header.label(text="Vertex Colors")

        if sub_body:
            sub_body.prop(settings, "cbb_vertex_color")

            if settings.cbb_vertex_color == "NAME":
                layout.prop(settings, "cbb_vertex_color_name")
            row = sub_body.row()
            row.active = settings.cbb_vertex_color != "NONE"
            row.prop(settings, "cbb_all_vertex_colors")

            row = sub_body.row()
            row.active = settings.cbb_vertex_color != "NONE"
            row.prop(
                settings,
                "cbb_active_vertex_color_when_no_material",
            )


def _draw_glb_export_material_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_material",
        default_closed=True,
    )
    header.label(text="Material")

    if body:
        body.prop(settings, "cbb_materials")

        col = body.column()
        col.active = settings.cbb_materials == "EXPORT"

        col.prop(settings, "cbb_image_format")

        if settings.cbb_image_format in {"AUTO", "JPEG", "WEBP"}:
            col.prop(settings, "cbb_image_quality")

        col = body.column()
        col.active = (
            settings.cbb_image_format != "WEBP"
            and settings.cbb_materials
            not in {
                "PLACEHOLDER",
                "NONE",
                "VIEWPORT",
            }
        )
        col.prop(settings, "cbb_image_add_webp")

        col = body.column()
        col.active = (
            settings.cbb_image_format != "WEBP"
            and settings.cbb_materials
            not in {
                "PLACEHOLDER",
                "NONE",
                "VIEWPORT",
            }
        )
        col.prop(settings, "cbb_image_webp_fallback")

        # Unused Textures & Images
        header, sub_body = body.panel(
            "CBB_GLB_export_data_material_unused",
            default_closed=True,
        )
        header.label(text="Unused Textures & Images")
        header.active = settings.cbb_materials == "EXPORT"

        if sub_body:
            sub_body.active = settings.cbb_materials == "EXPORT"
            sub_body.prop(settings, "cbb_unused_images")
            sub_body.prop(settings, "cbb_unused_textures")


def _draw_glb_export_shapekeys_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_shapekeys",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(settings, "cbb_morph", text="")
    header.label(text="Shape Keys")

    if body:
        body.active = settings.cbb_morph

        body.prop(settings, "cbb_morph_normal")

        col = body.column()
        col.active = settings.cbb_morph_normal
        col.prop(settings, "cbb_morph_tangent")


def _draw_glb_export_armature_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_armature",
        default_closed=True,
    )
    header.label(text="Armature")

    if body:
        body.active = settings.cbb_skins

        body.prop(settings, "cbb_rest_position_armature")

        body.prop(settings, "cbb_def_bones")
        body.prop(settings, "cbb_armature_object_remove")
        body.prop(settings, "cbb_hierarchy_flatten_bones")
        body.prop(settings, "cbb_leaf_bone")


def _draw_glb_export_skinning_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_skinning",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(settings, "cbb_skins", text="")
    header.label(text="Skinning")

    if body:
        body.active = settings.cbb_skins

        row = body.row()
        row.prop(settings, "cbb_influence_nb")
        row.active = not settings.cbb_all_influences

        body.prop(settings, "cbb_all_influences")


def _draw_glb_export_lighting_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_lighting",
        default_closed=True,
    )
    header.label(text="Lighting")

    if body:
        body.prop(settings, "cbb_convert_lighting_mode")


def _draw_glb_export_draco_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_compression",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(
        settings,
        "cbb_draco_mesh_compression_enable",
        text="",
    )
    header.label(text="Draco Compression")

    if body:
        body.active = settings.cbb_draco_mesh_compression_enable

        body.prop(
            settings,
            "cbb_draco_mesh_compression_level",
        )

        col = body.column(align=True)
        col.prop(
            settings,
            "cbb_draco_position_quantization",
            text="Quantize Position",
        )
        col.prop(
            settings,
            "cbb_draco_normal_quantization",
            text="Normal",
        )
        col.prop(
            settings,
            "cbb_draco_texcoord_quantization",
            text="Tex Coord",
        )
        col.prop(
            settings,
            "cbb_draco_color_quantization",
            text="Color",
        )
        col.prop(
            settings,
            "cbb_draco_generic_quantization",
            text="Generic",
        )


def _draw_glb_export_meshopt_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_data_meshopt_compression",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(
        settings,
        "cbb_meshopt_compression_enable",
        text="",
    )
    header.label(text="Meshopt Compression")

    if body:
        body.active = settings.cbb_meshopt_compression_enable
        body.prop(settings, "cbb_meshopt_extension")


def _draw_glb_export_animation_panel(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(settings, "cbb_animations", text="")
    header.label(text="Animation")

    if body:
        body.active = settings.cbb_animations

        body.prop(settings, "cbb_animation_mode")

        _draw_glb_export_animation_bake_and_merge(body, settings)
        _draw_glb_export_animation_ranges(body, settings)
        _draw_glb_export_animation_armature(body, settings)
        _draw_glb_export_animation_shapekeys(body, settings)
        _draw_glb_export_animation_sampling(body, settings)
        _draw_glb_export_animation_optimize(body, settings)


def _draw_glb_export_animation_bake_and_merge(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation_bake_and_merge",
        default_closed=True,
    )
    header.label(text="Bake & Merge")

    if body:
        row = body.row()
        row.active = settings.cbb_force_sampling and settings.cbb_animation_mode in {
            "ACTIONS",
            "ACTIVE_ACTIONS",
            "BROADCAST",
        }
        row.prop(settings, "cbb_bake_animation")

        row = body.row()
        row.active = (
            settings.cbb_force_sampling and settings.cbb_animation_mode == "ACTIONS"
        )
        row.prop(settings, "cbb_merge_animation")


def _draw_glb_export_animation_ranges(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation_ranges",
        default_closed=True,
    )
    header.label(text="Rest & Ranges")

    if body:
        body.prop(settings, "cbb_current_frame")

        row = body.row()
        row.active = settings.cbb_animation_mode in {
            "ACTIONS",
            "ACTIVE_ACTIONS",
            "BROADCAST",
            "NLA_TRACKS",
        }
        row.prop(settings, "cbb_frame_range")

        body.prop(settings, "cbb_anim_slide_to_zero")

        row = body.row()
        row.active = settings.cbb_animation_mode in {
            "ACTIONS",
            "ACTIVE_ACTIONS",
            "BROADCAST",
            "NLA_TRACKS",
        }
        row.prop(settings, "cbb_negative_frame")


def _draw_glb_export_animation_armature(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation_armature",
        default_closed=True,
    )
    header.label(text="Armature")

    if body:
        row = body.row()
        row.active = settings.cbb_animation_mode == "ACTIONS"
        row.prop(settings, "cbb_anim_single_armature")

        body.prop(settings, "cbb_reset_pose_bones")


def _draw_glb_export_animation_shapekeys(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation_shapekeys",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(settings, "cbb_morph_animation", text="")
    header.label(text="Shape Keys Animation")

    if body:
        body.active = settings.cbb_animations and settings.cbb_morph

        row = body.row()
        row.active = settings.cbb_morph_animation
        row.prop(settings, "cbb_morph_reset_sk_data")


def _draw_glb_export_animation_sampling(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation_sampling",
        default_closed=True,
    )

    header.use_property_split = False
    header.prop(settings, "cbb_force_sampling", text="")
    header.label(text="Sampling Animations")

    if body:
        body.active = settings.cbb_animations and settings.cbb_force_sampling

        body.prop(settings, "cbb_frame_step")
        body.prop(settings, "cbb_sampling_interpolation_fallback")


def _draw_glb_export_animation_optimize(layout, settings):
    header, body = layout.panel(
        "CBB_GLB_export_animation_optimize",
        default_closed=True,
    )
    header.label(text="Optimize Animations")

    if body:
        body.active = settings.cbb_animations

        body.prop(settings, "cbb_optimize_animation_size")
        body.prop(
            settings,
            "cbb_optimize_animation_keep_anim_armature",
        )
        body.prop(
            settings,
            "cbb_optimize_animation_keep_anim_object",
        )
        body.prop(
            settings,
            "cbb_optimize_disable_viewport",
        )


def _draw_cascadeur_glb_import(layout, addon_props):
    box = layout.box()
    box.label(text="Cascadeur Import", icon_value=icons.get_icon_id("cascadeur"))
    box.separator(type="LINE", factor=1.2)

    settings = addon_props.cascadeur_glb_import

    # Preset
    row = box.row(align=True)
    row.prop(settings, "cbb_preset")

    # Cascadeur import options
    col = box.column(align=True)
    col.prop(settings, "cbb_is_update_mode")
    col.prop(settings, "cbb_for_selected_objects")
    col.prop(settings, "cbb_for_selected_interval")
    col.prop(settings, "cbb_include_animation")
    col.prop(settings, "cbb_include_objects")

    # Scale factor
    col = box.column(align=True)
    col.prop(settings, "cbb_use_scale_factor")

    row = col.row(align=True)
    row.enabled = settings.cbb_use_scale_factor
    row.prop(settings, "cbb_scale_factor")

    # Mesh options
    col = box.column(align=True)
    col.prop(settings, "cbb_ignore_mesh_transform")
    col.prop(settings, "cbb_adjust_meshes_rotations")
    col.prop(settings, "cbb_move_meshes_to_root")
