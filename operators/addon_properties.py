import bpy
from ..utils.properties_handling import (
    apply_preset,
    GLB_EXPORT_PRESETS,
    GLB_IMPORT_PRESETS,
)


def generate_enum_items(options: list[str]) -> list[tuple[str, str, str]]:
    return [(option, option, "") for option in options]


class CBB_PG_cascadeur_to_blender(bpy.types.PropertyGroup):
    cbb_file_format: bpy.props.EnumProperty(
        items=generate_enum_items(["fbx", "glb"]),
        name="File Format",
        description="Fileformat used for Cascadeur to Blender transfer",
        default="fbx",
    )


class CBB_PG_blender_to_cascadeur(bpy.types.PropertyGroup):
    cbb_file_format: bpy.props.EnumProperty(
        items=generate_enum_items(["fbx", "glb"]),
        name="File Format",
        description="Fileformat used for Blender to Cascadeur transfer",
        default="fbx",
    )


class CBB_PG_cascadeur_fbx_import_settings(bpy.types.PropertyGroup):
    cbb_import_methods: bpy.props.EnumProperty(
        name="Cascadeur Import Method",
        items=(
            ("add_model", "Add Model", ""),
            ("add_model_to_selected", "Add Model to Selected", ""),
            ("import_animation", "Animation", ""),
            ("import_animation_to_selected_frames", "Animation - selected frames", ""),
            ("import_animation_to_selected_objects", "Animation - selected joints", ""),
            ("import_model", "Model", ""),
            ("import_scene", "Scene", ""),
        ),
        description="Method to use when exporting from Cascadeur",
        default="import_model",
    )

    cbb_csc_import_selected: bpy.props.BoolProperty(
        name="Selected Interval",
        description="Import selected interval only",
        default=False,
    )

    cbb_csc_apply_euler_filter: bpy.props.BoolProperty(
        name="Apply Euler Filter",
        description="Automatically set objects' rotations to lowes possible values",
        default=False,
    )

    cbb_csc_up_axis: bpy.props.EnumProperty(
        items=generate_enum_items(["Y", "Z"]),
        name="Up Axis",
        description="Up Axis when exporting from Cascadeur",
        default="Y",
    )

    cbb_csc_bake_animation: bpy.props.BoolProperty(
        name="Bake animation",
        description="Key all frames when exporting from Cascadeur",
        default=True,
    )


class CBB_PG_cascadeur_fbx_export_settings(bpy.types.PropertyGroup):
    cbb_export_methods: bpy.props.EnumProperty(
        name="Cascadeur Export Method",
        items=(
            ("export_all_objects", "Export All Objects", ""),
            ("export_joints", "Animation", ""),
            ("export_joints_selected", "Animation - selected joints and frames", ""),
            ("export_joints_selected_frames", "Animation - selected frames", ""),
            ("export_joints_selected_objects", "Animation - selected joints", ""),
            ("export_model", "Model", ""),
            ("export_scene_selected", "Scene - selected objects and frames", ""),
            ("export_scene_selected_frames", "Scene - selected frames", ""),
            ("export_scene_selected_objects", "Scene - selected objects", ""),
        ),
        description="Method to use when exporting from Cascadeur",
        default="export_all_objects",
    )

    cbb_csc_import_selected: bpy.props.BoolProperty(
        name="Selected Interval",
        description="Export selected interval only",
        default=False,
    )

    cbb_csc_apply_euler_filter: bpy.props.BoolProperty(
        name="Apply Euler Filter",
        description="Automatically set objects' rotations to lowes possible values",
        default=False,
    )

    cbb_csc_up_axis: bpy.props.EnumProperty(
        items=generate_enum_items(["Y", "Z"]),
        name="Up Axis",
        description="Up Axis when exporting from Cascadeur",
        default="Y",
    )

    cbb_csc_bake_animation: bpy.props.BoolProperty(
        name="Bake animation",
        description="Key all frames when exporting from Cascadeur",
        default=True,
    )


class CBB_PG_cascadeur_glb_import_settings(bpy.types.PropertyGroup):
    cbb_preset: bpy.props.EnumProperty(
        name="Preset",
        description="GLB import preset",
        items=[
            (
                "MODEL",
                "Model",
                "Import model",
            ),
            (
                "SCENE",
                "Scene",
                "Import scene",
            ),
            (
                "ADD_MODEL",
                "Add model",
                "Add a model",
            ),
            (
                "ADD_MODEL_SELECTED",
                "Add model to selected",
                "Add a model to selected joints",
            ),
            (
                "ANIMATION",
                "Animation",
                "Import animation",
            ),
            (
                "ANIMATION_SELECTED_FRAMES",
                "Animation to selected frames",
                "Import animation to selected frames",
            ),
            (
                "ANIMATION_SELECTED_OBJECTS",
                "Animation to selected objects",
                "Import animation to selected objects",
            ),
        ],
        default="MODEL",
        update=lambda self, context: apply_preset(
            self,
            GLB_IMPORT_PRESETS[self.cbb_preset],
        ),
    )

    cbb_for_selected_interval: bpy.props.BoolProperty(
        name="Selected Interval",
        description="Export or import only the currently selected animation interval",
        default=False,
    )

    cbb_for_selected_objects: bpy.props.BoolProperty(
        name="Selected Objects",
        description="Export or import only the currently selected objects",
        default=False,
    )

    cbb_include_animation: bpy.props.BoolProperty(
        name="Include Animation",
        description="Include animation data",
        default=True,
    )

    cbb_use_scale_factor: bpy.props.BoolProperty(
        name="Use Scale Factor",
        description="Apply a custom scale factor during import or export",
        default=True,
    )

    cbb_scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scale factor applied to mesh and object dimensions",
        default=100.0,
        soft_min=0.01,
        soft_max=100.0,
        min=0.0001,
        max=1000.0,
    )

    cbb_adjust_meshes_rotations: bpy.props.BoolProperty(
        name="Adjust Mesh Rotations",
        description="Adjust mesh rotations to match Cascadeur's coordinate system",
        default=True,
    )

    cbb_ignore_mesh_transform: bpy.props.BoolProperty(
        name="Ignore Mesh Transform",
        description="Ignore transformations stored on imported meshes",
        default=False,
    )

    cbb_include_objects: bpy.props.BoolProperty(
        name="Include Objects",
        description="Include object data when importing the GLB file",
        default=True,
    )

    cbb_is_update_mode: bpy.props.BoolProperty(
        name="Update Mode",
        description="Update existing objects instead of creating new ones when possible",
        default=False,
    )

    cbb_move_meshes_to_root: bpy.props.BoolProperty(
        name="Move Meshes to Root",
        description="Move imported meshes to the root of the scene hierarchy",
        default=False,
    )


class CBB_PG_cascadeur_glb_export_settings(bpy.types.PropertyGroup):
    cbb_preset: bpy.props.EnumProperty(
        name="Preset",
        description="GLB import preset",
        items=[
            (
                "SCENE",
                "Scene",
                "Export the whole scene",
            ),
            (
                "ANIMATION",
                "Animation",
                "Export the animation data only",
            ),
            (
                "SCENE_SELECTED_OBJECTS",
                "Selected objects and their animation",
                "Export every selected object with their animation",
            ),
            (
                "MODEL",
                "Model",
                "Export objects without animation data",
            ),
        ],
        default="SCENE",
        update=lambda self, context: apply_preset(
            self,
            GLB_EXPORT_PRESETS[self.cbb_preset],
        ),
    )

    cbb_for_selected_interval: bpy.props.BoolProperty(
        name="Selected Interval",
        description="Export or import only the currently selected animation interval",
        default=False,
    )

    cbb_for_selected_objects: bpy.props.BoolProperty(
        name="Selected Objects",
        description="Export or import only the currently selected objects",
        default=False,
    )

    cbb_include_animation: bpy.props.BoolProperty(
        name="Include Animation",
        description="Include animation data",
        default=True,
    )

    cbb_use_scale_factor: bpy.props.BoolProperty(
        name="Use Scale Factor",
        description="Apply a custom scale factor during import or export",
        default=True,
    )

    cbb_scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scale factor applied to mesh and object dimensions",
        default=0.01,
        soft_min=0.001,
        soft_max=100.0,
        min=0.0001,
        max=1000.0,
    )

    cbb_call_process_skinned_mesh: bpy.props.BoolProperty(
        name="Process Skinned Mesh",
        description="Process skinned meshes during export",
        default=True,
    )

    cbb_rotate_meshes_primitive_attributes: bpy.props.BoolProperty(
        name="Rotate Mesh Attributes",
        description="Apply rotation to mesh primitive attributes during export",
        default=True,
    )

    cbb_scale_meshes_primitive_attributes: bpy.props.BoolProperty(
        name="Scale Mesh Attributes",
        description="Apply scaling to mesh primitive attributes during export",
        default=True,
    )

    cbb_translate_meshes_primitive_attributes: bpy.props.BoolProperty(
        name="Translate Mesh Attributes",
        description="Apply translation to mesh primitive attributes during export",
        default=True,
    )


class CBB_PG_blender_fbx_import_settings(bpy.types.PropertyGroup):
    ###########
    # Include #
    ###########
    cbb_use_custom_normals: bpy.props.BoolProperty(
        name="Custom Normals",
        description="Import custom normals, if available",
        default=True,
    )

    cbb_use_subsurf: bpy.props.BoolProperty(
        name="Subdivision Data",
        description="Import FBX subdivision information as subdivision surface modifiers",
        default=False,
    )

    cbb_use_custom_props: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Import user properties as custom properties",
        default=True,
    )

    cbb_use_custom_props_enum_as_string: bpy.props.BoolProperty(
        name="Import Enums As Strings",
        description="Store enumeration values as strings",
        default=True,
    )

    cbb_use_image_search: bpy.props.BoolProperty(
        name="Image Search",
        description="Search subdirs for any associated images (WARNING: may be slow)",
        default=True,
    )

    cbb_colors_type: bpy.props.EnumProperty(
        name="Vertex Colors",
        items=(
            ("NONE", "None", "Do not import color attributes."),
            ("SRGB", "sRGB", "Expect file colors in sRGB color space."),
            ("LINEAR", "Linear", "Expect file colors in linear color space."),
        ),
        description="Import vertex color attributes",
        default="SRGB",
    )

    #############
    # Transform #
    #############
    cbb_global_scale: bpy.props.FloatProperty(
        name="Global Scale",
        description="Scale",
        default=1.0,
        min=0.001,
        max=1000,
    )

    cbb_decal_offset: bpy.props.FloatProperty(
        name="Decal Offset",
        description="Displace geometry of alpha meshes",
        default=1.0,
        min=0.0,
        max=1.0,
    )

    cbb_bake_space_transform: bpy.props.BoolProperty(
        name="Apply Transform",
        description="Bake space transform into object data. EXPERIMENTAL!",
        default=False,
    )

    cbb_use_prepost_rot: bpy.props.BoolProperty(
        name="Use Pre/Post Rotation",
        description="Use pre/post rotation from FBX transform",
        default=True,
    )

    cbb_use_manual_orientation: bpy.props.BoolProperty(
        name="Manual Orientation",
        description="Specify orientation and scale, instead of using embedded data in FBX file",
        default=False,
    )

    cbb_axis_forward: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Forward",
        description="Forward Axis",
        default="-Z",
    )

    cbb_axis_up: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Up",
        description="Forward Up",
        default="Y",
    )

    #############
    # Materials #
    #############
    cbb_mtl_name_collision_mode: bpy.props.EnumProperty(
        name="Vertex Colors",
        items=(
            (
                "MAKE_UNIQUE",
                "Make Unique",
                "Import each FBX material as a unique Blender material.",
            ),
            (
                "REFERENCE_EXISTING",
                "Reference Existing",
                "If a material with the same name already exists, reference that instead of importing.",
            ),
        ),
        description="Import vertex color attributes",
        default="REFERENCE_EXISTING",
    )

    #############
    # Animation #
    #############
    cbb_use_anim: bpy.props.BoolProperty(
        name="Import Animation",
        description="Import FBX animation",
        default=True,
    )

    cbb_anim_offset: bpy.props.FloatProperty(
        name="Animation Offset",
        description=" Offset to apply to animation during import, in frames",
        default=1.0,
    )

    ############
    # Armature #
    ############
    cbb_ignore_leaf_bones: bpy.props.BoolProperty(
        name="Ignore Leaf Bones",
        description="Ignore the last bone at the end of each chain",
        default=False,
    )

    cbb_force_connect_children: bpy.props.BoolProperty(
        name="Force Connect Children",
        description="Force connection of children bones to their parent",
        default=False,
    )

    cbb_automatic_bone_orientation: bpy.props.BoolProperty(
        name="Automatic Bone Orientation",
        description="Try to align the major bone axis with the bone children",
        default=False,
    )

    cbb_primary_bone_axis: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Primary Bone Axis",
        description="",
        default="Y",
    )

    cbb_secondary_bone_axis: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Secondary Bone Axis",
        description="",
        default="X",
    )


class CBB_PG_blender_fbx_export_settings(bpy.types.PropertyGroup):
    #############
    # Path mode #
    #############
    cbb_path_mode: bpy.props.EnumProperty(
        name="Path Mode",
        items=(
            ("AUTO", "Auto", "Use relative paths with subdirectories only."),
            ("ABSOLUTE", "Absolute", "Always write absolute paths."),
            ("RELATIVE", "Relative", "Write relative paths where possible."),
            ("MATCH", "Match", "Match absolute/relative setting with input path."),
            ("STRIP", "Strip", "Filename only."),
            (
                "COPY",
                "Copy",
                "Copy the file to the destination path (or subdirectory).",
            ),
        ),
        description="Method used to reference paths.",
        default="AUTO",
    )

    cbb_embed_textures: bpy.props.BoolProperty(
        name="Embed Textures",
        description="Embed textures in FBX binary file (only for “Copy” path mode!)",
        default=False,
    )

    ###########
    # Include #
    ###########
    cbb_use_selection: bpy.props.BoolProperty(
        name="Selected Objects",
        description="Export selected and visible objects only",
        default=False,
    )

    cbb_use_visible: bpy.props.BoolProperty(
        name="Visible Objects",
        description="Export visible objects only",
        default=False,
    )

    cbb_use_active_collection: bpy.props.BoolProperty(
        name="Active Collection",
        description="Export only objects from the active collection (and its children)",
        default=False,
    )

    cbb_object_types: bpy.props.EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        items=(
            ("EMPTY", "Empty", ""),
            ("CAMERA", "Camera", ""),
            ("LIGHT", "Lamp", ""),
            ("ARMATURE", "Armature", "WARNING: not supported in dupli/group instances"),
            ("MESH", "Mesh", ""),
            (
                "OTHER",
                "Other",
                "Other geometry types, like curve, metaball, etc. (converted to meshes)",
            ),
        ),
        description="Which kind of object to export",
        default={"EMPTY", "CAMERA", "LIGHT", "ARMATURE", "MESH", "OTHER"},
    )

    cbb_use_custom_props: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Export custom properties",
        default=False,
    )

    #############
    # Transform #
    #############
    cbb_global_scale: bpy.props.FloatProperty(
        name="Global Scale",
        description="Scale",
        default=1.0,
        min=0.001,
        max=1000,
    )

    cbb_apply_scale_options: bpy.props.EnumProperty(
        items=(
            (
                "FBX_SCALE_NONE",
                "All Local",
                "Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0.",
            ),
            (
                "FBX_SCALE_UNITS",
                "FBX Units Scale",
                "Apply custom scaling to each object transformation, and units scaling to FBX scale.",
            ),
            (
                "FBX_SCALE_CUSTOM",
                "FBX Custom Scale",
                "Apply custom scaling to FBX scale, and units scaling to each object transformation.",
            ),
            (
                "FBX_SCALE_ALL",
                "FBX All",
                "Apply custom scaling and units scaling to FBX scale.",
            ),
        ),
        name="Forward",
        description="Forward Axis",
        default="FBX_SCALE_NONE",
    )

    cbb_axis_forward: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Forward",
        description="Forward Axis",
        default="-Z",
    )

    cbb_axis_up: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Up",
        description="Forward Up",
        default="Y",
    )

    cbb_apply_unit_scale: bpy.props.BoolProperty(
        name="Apply Unit",
        description="Apply Unit, Take into account current Blender units settings",
        default=True,
    )

    cbb_use_space_transform: bpy.props.BoolProperty(
        name="Use Space Transform",
        description="Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is",
        default=True,
    )

    cbb_apply_transform: bpy.props.BoolProperty(
        name="Apply Transform",
        description="Bake space transform into object data. EXPERIMENTAL!",
        default=False,
    )

    ############
    # Geometry #
    ############

    cbb_mesh_smooth_type: bpy.props.EnumProperty(
        items=(
            (
                "OFF",
                "Normals Only",
                "Export only normals instead of writing edge or face smoothing data.",
            ),
            (
                "FACE",
                "Face",
                "Write face smoothing.",
            ),
            (
                "EDGE",
                "Edge",
                "Write edge smoothing.",
            ),
            (
                "SMOOTH_GROUP",
                "Smoothing Groups",
                "Write face smoothing groups.",
            ),
        ),
        name="Smoothing",
        description="Export smoothing information",
        default="OFF",
    )

    cbb_use_subsurf: bpy.props.BoolProperty(
        name="Export Subdivision Surface",
        description="Export the last Catmull-Rom subdivision modifier as FBX subdivision",
        default=False,
    )

    cbb_use_mesh_modifiers: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to mesh objects (except Armature ones) - WARNING: prevents exporting shape keys",
        default=True,
    )

    cbb_use_mesh_edges: bpy.props.BoolProperty(
        name="Loose Edges",
        description="Export loose edges (as two-vertices polygons)",
        default=False,
    )

    cbb_use_triangles: bpy.props.BoolProperty(
        name="Triangulate Faces",
        description="Convert all faces to triangles",
        default=False,
    )

    cbb_use_tspace: bpy.props.BoolProperty(
        name="Tangent Space",
        description="Add binormal and tangent vectors, together with normal they form the tangent space (will only work correctly with tris/quads only meshes!)",
        default=False,
    )

    cbb_colors_type: bpy.props.EnumProperty(
        items=(
            ("NONE", "None", "Do not export color attributes."),
            ("SRGB", "sRGB", "Export colors in sRGB color space."),
            ("LINEAR", "Linear", "Export colors in linear color space."),
        ),
        name="Vertex Colors",
        description="Export vertex color attributes",
        default="SRGB",
    )

    cbb_prioritize_active_color: bpy.props.BoolProperty(
        name="Prioritize Active Color",
        description="Make sure active color will be exported first. Could be important since some other software can discard other color attributes besides the first one",
        default=False,
    )

    ############
    # Armature #
    ############
    cbb_primary_bone_axis: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Primary Bone Axis",
        description="",
        default="Y",
    )

    cbb_secondary_bone_axis: bpy.props.EnumProperty(
        items=generate_enum_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Secondary Bone Axis",
        description="",
        default="X",
    )

    cbb_armature_nodetype: bpy.props.EnumProperty(
        items=(
            (
                "NULL",
                "Null",
                "‘Null’ FBX node, similar to Blender’s Empty (default).",
            ),
            (
                "ROOT",
                "Root",
                "‘Root’ FBX node, supposed to be the root of chains of bones...",
            ),
            (
                "LIMBNODE",
                "LimbNode",
                "‘LimbNode’ FBX node, a regular joint between two bones...",
            ),
        ),
        name="Armature FBXNode Type",
        description="FBX type of node (object) used to represent Blender’s armatures (use the Null type unless you experience issues with the other app, as other choices may not import back perfectly into Blender…)",
        default="NULL",
    )

    cbb_deform_only: bpy.props.BoolProperty(
        name="Only Deform Bones",
        description="Only write deforming bones",
        default=True,
    )

    cbb_leaf_bones: bpy.props.BoolProperty(
        name="Add Leaf Bones",
        description="Append a final bone to the end of each chain to specify last bone length",
        default=False,
    )

    #############
    # Animation #
    #############
    cbb_bake_anim: bpy.props.BoolProperty(
        name="Baked Animation",
        description="Export baked keyframe animation",
        default=True,
    )

    cbb_bake_anim_use_all_bones: bpy.props.BoolProperty(
        name="Key All Bones",
        description="Force exporting at least one key of animation for all bones",
        default=True,
    )

    cbb_use_nla_strips: bpy.props.BoolProperty(
        name="NLA Strips",
        description="Export each non-muted NLA strip as a separated FBX’s AnimStack, if any, instead of global scene animation",
        default=False,
    )

    cbb_use_all_actions: bpy.props.BoolProperty(
        name="All Actions",
        description="Export each action as a separated FBX’s AnimStack, instead of global scene animation",
        default=False,
    )

    cbb_bake_anim_force_startend_keying: bpy.props.BoolProperty(
        name="Force Start/End Keying",
        description="Always add a keyframe at start and end of actions for animated channels",
        default=True,
    )

    cbb_bake_anim_step: bpy.props.FloatProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        default=1.0,
        soft_min=0.01,
        soft_max=10,
        min=0.1,
        max=100,
    )

    cbb_bake_anim_simplify_factor: bpy.props.FloatProperty(
        name="Simplify",
        description="How much to simplify baked values (0.0 to disable, the higher the more simplified)",
        default=1.0,
        soft_min=0.0,
        soft_max=10,
        min=0.0,
        max=100,
    )


class CBB_PG_blender_glb_import_settings(bpy.types.PropertyGroup):
    cbb_import_shading: bpy.props.EnumProperty(
        name="Shading",
        items=(
            (
                "NORMALS",
                "Normals",
                "Use normals from the glTF file",
            ),
            (
                "FLAT",
                "Flat",
                "Use flat shading",
            ),
            (
                "SMOOTH",
                "Smooth",
                "Use smooth shading",
            ),
        ),
        description="How normals are computed during import",
        default="NORMALS",
    )

    cbb_convert_lighting_mode: bpy.props.EnumProperty(
        name="Lighting Mode",
        items=(
            (
                "SPEC",
                "Standard",
                "Physically-based glTF lighting units (cd, lx, nt).",
            ),
            (
                "COMPAT",
                "Unitless",
                "Non-physical, unitless lighting. Useful when exposure controls are not available.",
            ),
            (
                "RAW",
                "Raw",
                "Blender lighting strengths with no conversion. Deprecated.",
            ),
        ),
        description="Optional backwards compatibility for non-standard render engines. Applies to lights",
        default="SPEC",
    )

    ########
    # Mesh #
    ########

    cbb_merge_vertices: bpy.props.BoolProperty(
        name="Merge Vertices",
        description=(
            "Attempt to combine co-located vertices where possible. "
            "Currently cannot combine vertices with different normals"
        ),
        default=False,
    )

    cbb_import_merge_material_slots: bpy.props.BoolProperty(
        name="Merge Material Slots",
        description="Merge material slots when possible",
        default=True,
    )

    cbb_import_point_as_pointcloud: bpy.props.BoolProperty(
        name="Import Points as Point Cloud",
        description=("Import mesh with only POINTS primitives as Point Cloud objects"),
        default=False,
    )

    ###########
    # Texture #
    ###########

    cbb_import_pack_images: bpy.props.BoolProperty(
        name="Pack Images",
        description="Pack all images into .blend file",
        default=True,
    )

    cbb_import_webp_texture: bpy.props.BoolProperty(
        name="Import WebP Textures",
        description=(
            "If a texture exists in WebP format, load the WebP texture "
            "instead of the fallback PNG/JPEG one"
        ),
        default=False,
    )

    cbb_import_unused_materials: bpy.props.BoolProperty(
        name="Import Unused Materials & Images",
        description="Import materials and images not assigned to any mesh",
        default=False,
    )

    ################
    # Bones & Skin #
    ################

    cbb_bone_heuristic: bpy.props.EnumProperty(
        name="Bone Dir",
        items=(
            (
                "BLENDER",
                "Blender",
                "Best for import/export round trip. "
                "Bone tips are placed on their local +Y axis in glTF space.",
            ),
            (
                "TEMPERANCE",
                "Temperance",
                "Decent all-around strategy. A bone with one child has "
                "its tip placed on the local axis closest to its child.",
            ),
            (
                "FORTUNE",
                "Fortune",
                "May look better, but can be less accurate. A bone with "
                "one child has its tip placed at its child's root.",
            ),
        ),
        description="Heuristic for placing bones",
        default="BLENDER",
    )

    cbb_guess_original_bind_pose: bpy.props.BoolProperty(
        name="Guess Original Bind Pose",
        description=(
            "Try to guess the original bind pose for skinned meshes "
            "from the inverse bind matrices. When off, use the "
            "default/rest pose as bind pose"
        ),
        default=True,
    )

    cbb_disable_bone_shape: bpy.props.BoolProperty(
        name="Disable Bone Shape",
        description="Do not create bone shapes",
        default=True,
    )

    cbb_bone_shape_scale_factor: bpy.props.FloatProperty(
        name="Bone Shape Scale",
        description="Scale factor for bone shapes",
        default=1.0,
    )

    ############
    # Pipeline #
    ############

    cbb_import_scene_as_collection: bpy.props.BoolProperty(
        name="Import Scene as Collection",
        description="Import the scene as a collection",
        default=True,
    )

    cbb_import_select_created_objects: bpy.props.BoolProperty(
        name="Select Imported Objects",
        description="Select created objects at the end of the import",
        default=True,
    )

    cbb_import_scene_extras: bpy.props.BoolProperty(
        name="Import Scene Extras",
        description=(
            "Import scene extras as custom properties. "
            "Existing custom properties will be overwritten"
        ),
        default=True,
    )


class CBB_PG_blender_glb_export_settings(bpy.types.PropertyGroup):

    ###########
    # Include #
    ###########

    cbb_selection: bpy.props.BoolProperty(
        name="Selected Objects",
        description="Export selected objects only",
        default=False,
    )

    cbb_visible: bpy.props.BoolProperty(
        name="Visible Objects",
        description="Export visible objects only",
        default=False,
    )

    cbb_renderable: bpy.props.BoolProperty(
        name="Renderable Objects",
        description="Export renderable objects only",
        default=False,
    )

    cbb_active_collection: bpy.props.BoolProperty(
        name="Active Collection",
        description="Export objects in the active collection only",
        default=False,
    )

    cbb_active_collection_with_nested: bpy.props.BoolProperty(
        name="Include Nested Collections",
        description="Include active collection and nested collections",
        default=True,
    )

    cbb_active_scene: bpy.props.BoolProperty(
        name="Active Scene",
        description="Export active scene only",
        default=False,
    )

    cbb_extras: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Export custom properties as glTF extras",
        default=False,
    )

    cbb_cameras: bpy.props.BoolProperty(
        name="Cameras",
        description="Export cameras",
        default=False,
    )

    cbb_lights: bpy.props.BoolProperty(
        name="Punctual Lights",
        description=(
            "Export directional, point, and spot lights. "
            'Uses "KHR_lights_punctual" glTF extension'
        ),
        default=False,
    )

    #############
    # Transform #
    #############

    cbb_yup: bpy.props.BoolProperty(
        name="+Y Up",
        description="Export using glTF convention, +Y up",
        default=True,
    )

    ########
    # Data #
    ########
    #  Scene Graph
    cbb_hierarchy_flatten_objs: bpy.props.BoolProperty(
        name="Flatten Object Hierarchy",
        description=(
            "Flatten Object Hierarchy. Useful in case of non decomposable transformation matrix"
        ),
        default=False,
    )

    cbb_hierarchy_full_collections: bpy.props.BoolProperty(
        name="Full Collection Hierarchy",
        description="Export full hierarchy, including intermediate collections",
        default=False,
    )

    #  Mesh
    cbb_apply: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description=(
            "Apply modifiers (excluding Armatures) to mesh objects. "
            "WARNING: prevents exporting shape keys"
        ),
        default=False,
    )

    cbb_texcoords: bpy.props.BoolProperty(
        name="UVs",
        description="Export UVs (texture coordinates) with meshes",
        default=True,
    )

    cbb_normals: bpy.props.BoolProperty(
        name="Normals",
        description="Export vertex normals with meshes",
        default=True,
    )

    cbb_tangents: bpy.props.BoolProperty(
        name="Tangents",
        description="Export vertex tangents with meshes",
        default=False,
    )

    cbb_attributes: bpy.props.BoolProperty(
        name="Attributes",
        description="Export Attributes (when starting with underscore)",
        default=False,
    )

    cbb_mesh_edges: bpy.props.BoolProperty(
        name="Loose Edges",
        description=(
            "Export loose edges as lines, using the material from "
            "the first material slot"
        ),
        default=False,
    )

    cbb_mesh_vertices: bpy.props.BoolProperty(
        name="Loose Points",
        description=(
            "Export loose points as glTF points, using the material "
            "from the first material slot"
        ),
        default=False,
    )

    cbb_shared_accessors: bpy.props.BoolProperty(
        name="Shared Accessors",
        description="Export Primitives using shared accessors for attributes",
        default=False,
    )

    cbb_vertex_color: bpy.props.EnumProperty(
        name="Use Vertex Color",
        items=(
            (
                "MATERIAL",
                "Material",
                "Export vertex color when used by material.",
            ),
            (
                "ACTIVE",
                "Active",
                "Export active vertex color.",
            ),
            (
                "NAME",
                "Name",
                "Export vertex color with this name.",
            ),
            (
                "NONE",
                "None",
                "Do not export vertex color.",
            ),
        ),
        description="How to export vertex color",
        default="MATERIAL",
    )

    cbb_vertex_color_name: bpy.props.StringProperty(
        name="Name",
        description="Name of the vertex color attribute to export",
        default="Color",
    )

    cbb_all_vertex_colors: bpy.props.BoolProperty(
        name="Export All Vertex Colors",
        description=(
            "Export all vertex colors, even if not used by any material. "
            "If no Vertex Color is used in the mesh materials, a fake "
            "COLOR_0 will be created, in order to keep material unchanged"
        ),
        default=True,
    )

    cbb_active_vertex_color_when_no_material: bpy.props.BoolProperty(
        name="Export Active Vertex Color When No Material",
        description="When there is no material on object, export active vertex color",
        default=True,
    )

    #  Materials
    cbb_materials: bpy.props.EnumProperty(
        name="Materials",
        items=(
            (
                "EXPORT",
                "Export",
                "Export all materials used by included objects.",
            ),
            (
                "PLACEHOLDER",
                "Placeholder",
                "Do not export materials, but write multiple primitive groups "
                "per mesh, keeping material slot information.",
            ),
            (
                "VIEWPORT",
                "Viewport",
                "Export minimal materials as defined in Viewport display properties.",
            ),
            (
                "NONE",
                "No export",
                "Do not export materials, and combine mesh primitive groups, "
                "losing material slot information.",
            ),
        ),
        description="Export materials",
        default="EXPORT",
    )

    cbb_image_format: bpy.props.EnumProperty(
        name="Images",
        items=(
            (
                "AUTO",
                "Automatic",
                "Save PNGs as PNGs, JPEGs as JPEGs, WebPs as WebPs. "
                "For other formats, use PNG.",
            ),
            (
                "JPEG",
                "JPEG Format (.jpg)",
                "Save images as JPEGs. Images that need alpha are saved as PNGs. "
                "Be aware of a possible loss in quality.",
            ),
            (
                "WEBP",
                "WebP Format",
                "Save images as WebPs as main image (no fallback).",
            ),
            (
                "NONE",
                "None",
                "Don't export images.",
            ),
        ),
        description="Output format for images",
        default="AUTO",
    )

    cbb_image_quality: bpy.props.IntProperty(
        name="Image Quality",
        description="Quality of image export",
        default=75,
        min=0,
        max=100,
    )

    cbb_image_add_webp: bpy.props.BoolProperty(
        name="Create WebP",
        description=(
            "Creates WebP textures for every texture. "
            "For already WebP textures, nothing happens"
        ),
        default=False,
    )

    cbb_image_webp_fallback: bpy.props.BoolProperty(
        name="WebP Fallback",
        description="For all WebP textures, create a PNG fallback texture",
        default=False,
    )

    cbb_unused_images: bpy.props.BoolProperty(
        name="Unused Images",
        description="Export images not assigned to any material",
        default=False,
    )

    cbb_unused_textures: bpy.props.BoolProperty(
        name="Prepare Unused Textures",
        description=(
            "Export image texture nodes not assigned to any material. "
            "This feature is not standard and needs an external extension "
            "to be included in the glTF file"
        ),
        default=False,
    )

    #  Shape Keys
    cbb_morph: bpy.props.BoolProperty(
        name="Shape Keys",
        description="Export shape keys (morph targets)",
        default=True,
    )

    cbb_morph_normal: bpy.props.BoolProperty(
        name="Shape Key Normals",
        description="Export vertex normals with shape keys (morph targets)",
        default=True,
    )

    cbb_morph_tangent: bpy.props.BoolProperty(
        name="Shape Key Tangents",
        description="Export vertex tangents with shape keys (morph targets)",
        default=False,
    )

    #  Armature
    cbb_rest_position_armature: bpy.props.BoolProperty(
        name="Use Rest Position Armature",
        description=(
            "Export armatures using rest position as joints' rest pose. "
            "When off, current frame pose is used as rest pose"
        ),
        default=True,
    )

    cbb_def_bones: bpy.props.BoolProperty(
        name="Export Deformation Bones Only",
        description="Export Deformation bones only",
        default=True,
    )

    cbb_armature_object_remove: bpy.props.BoolProperty(
        name="Remove Armature Object",
        description=(
            "Remove Armature object if possible. If Armature has multiple root bones, "
            "object will not be removed"
        ),
        default=False,
    )
    cbb_hierarchy_flatten_bones: bpy.props.BoolProperty(
        name="Flatten Bone Hierarchy",
        description=(
            "Flatten Bone Hierarchy. Useful in case of non decomposable transformation matrix"
        ),
        default=False,
    )

    cbb_leaf_bone: bpy.props.BoolProperty(
        name="Add Leaf Bones",
        description=(
            "Append a final bone to the end of each chain to specify last bone length. "
            "Use this when you intend to edit the armature from exported data"
        ),
        default=False,
    )

    #  Skinning
    cbb_skins: bpy.props.BoolProperty(
        name="Skinning",
        description="Export skinning (armature) data",
        default=True,
    )

    cbb_influence_nb: bpy.props.IntProperty(
        name="Bone Influences",
        description="Choose how many Bone influences to export",
        default=4,
        min=1,
    )

    cbb_all_influences: bpy.props.BoolProperty(
        name="Include All Bone Influences",
        description=(
            "Allow export of all joint vertex influences. "
            "Models may appear incorrectly in many viewers"
        ),
        default=False,
    )

    #  Lighting

    cbb_convert_lighting_mode: bpy.props.EnumProperty(
        name="Lighting Mode",
        items=(
            (
                "SPEC",
                "Standard",
                "Physically-based glTF lighting units (cd, lx, nt).",
            ),
            (
                "COMPAT",
                "Unitless",
                "Non-physical, unitless lighting. Useful when exposure controls are not available.",
            ),
            (
                "RAW",
                "Raw",
                "Blender lighting strengths with no conversion. Deprecated.",
            ),
        ),
        description=(
            "Optional backwards compatibility for non-standard render engines. "
            "Applies to lights"
        ),
        default="SPEC",
    )

    #  Draco Compression
    cbb_draco_mesh_compression_enable: bpy.props.BoolProperty(
        name="Draco Mesh Compression",
        description="Compress mesh using Draco",
        default=False,
    )

    cbb_draco_mesh_compression_level: bpy.props.IntProperty(
        name="Compression Level",
        description=(
            "Compression level (0 = most speed, 6 = most compression, "
            "higher values currently not supported)"
        ),
        default=6,
        min=0,
        max=10,
    )

    cbb_draco_position_quantization: bpy.props.IntProperty(
        name="Position Quantization Bits",
        description="Quantization bits for position values (0 = no quantization)",
        default=14,
        min=0,
        max=30,
    )

    cbb_draco_normal_quantization: bpy.props.IntProperty(
        name="Normal Quantization Bits",
        description="Quantization bits for normal values (0 = no quantization)",
        default=10,
        min=0,
        max=30,
    )

    cbb_draco_texcoord_quantization: bpy.props.IntProperty(
        name="Texcoord Quantization Bits",
        description="Quantization bits for texture coordinate values (0 = no quantization)",
        default=12,
        min=0,
        max=30,
    )

    cbb_draco_color_quantization: bpy.props.IntProperty(
        name="Color Quantization Bits",
        description="Quantization bits for color values (0 = no quantization)",
        default=10,
        min=0,
        max=30,
    )

    cbb_draco_generic_quantization: bpy.props.IntProperty(
        name="Generic Quantization Bits",
        description="Quantization bits for generic values like weights or joints (0 = no quantization)",
        default=12,
        min=0,
        max=30,
    )

    #  Meshopt Compression
    cbb_meshopt_compression_enable: bpy.props.BoolProperty(
        name="Meshopt Compression",
        description="Compress mesh using Meshopt",
        default=False,
    )

    cbb_meshopt_extension: bpy.props.EnumProperty(
        name="Meshopt Extension",
        items=(
            (
                "EXT_meshopt_compression",
                "EXT_meshopt_compression",
                "Use EXT_meshopt_compression extension for mesh compression.",
            ),
            (
                "KHR_meshopt_compression",
                "KHR_meshopt_compression",
                "Use KHR_meshopt_compression extension for mesh compression.",
            ),
        ),
        description="Extension to use for meshopt compression",
        default="EXT_meshopt_compression",
    )

    #############
    # Animation #
    #############
    cbb_animations: bpy.props.BoolProperty(
        name="Animations",
        description="Export active actions and NLA tracks as glTF animations",
        default=True,
    )

    cbb_animation_mode: bpy.props.EnumProperty(
        name="Animation Mode",
        items=(
            (
                "ACTIONS",
                "Actions",
                "Export actions (actives and on NLA tracks) as separate animations.",
            ),
            (
                "ACTIVE_ACTIONS",
                "Active actions merged",
                "All the currently assigned actions become one glTF animation.",
            ),
            (
                "BROADCAST",
                "Broadcast actions",
                "Broadcast all compatible actions to all objects.",
            ),
            (
                "NLA_TRACKS",
                "NLA Tracks",
                "Export individual NLA Tracks as separate animation.",
            ),
            (
                "SCENE",
                "Scene",
                "Export baked scene as a single animation.",
            ),
        ),
        description="Export Animation mode",
        default="ACTIONS",
    )

    #  Bake & Merge
    cbb_bake_animation: bpy.props.BoolProperty(
        name="Bake All Objects Animations",
        description=(
            "Force exporting animation on every object. Can be useful when using "
            "constraints or driver. Also useful when exporting only selection"
        ),
        default=False,
    )

    cbb_merge_animation: bpy.props.EnumProperty(
        name="Merge Animation",
        items=(
            (
                "NLA_TRACK",
                "NLA Track Names",
                "Merge by NLA Track Names.",
            ),
            (
                "ACTION",
                "Actions",
                "Merge by Actions.",
            ),
            (
                "NONE",
                "No Merge",
                "Do Not Merge Animations.",
            ),
        ),
        description="Merge Animations",
        default="ACTION",
    )

    #  Rest & Ranges
    cbb_current_frame: bpy.props.BoolProperty(
        name="Use Current Frame as Object Rest Transformations",
        description=(
            "Export the scene in the current animation frame. When off, "
            "frame 0 is used as rest transformations for objects"
        ),
        default=False,
    )

    cbb_frame_range: bpy.props.BoolProperty(
        name="Limit to Playback Range",
        description="Clips animations to selected playback range",
        default=False,
    )

    cbb_anim_slide_to_zero: bpy.props.BoolProperty(
        name="Set All glTF Animation Starting at 0",
        description="Set all glTF animation starting at 0.0s. Can be useful for looping animations",
        default=False,
    )

    cbb_negative_frame: bpy.props.EnumProperty(
        name="Negative Frames",
        items=(
            (
                "SLIDE",
                "Slide",
                "Slide animation to start at frame 0.",
            ),
            (
                "CROP",
                "Crop",
                "Keep only frames above frame 0.",
            ),
        ),
        description="Negative Frames are slid or cropped",
        default="SLIDE",
    )

    #  Armature
    cbb_anim_single_armature: bpy.props.BoolProperty(
        name="Export all Armature Actions",
        description=(
            "Export all actions bound to a single armature. "
            "WARNING: Option does not support exports including multiple armatures"
        ),
        default=True,
    )

    cbb_reset_pose_bones: bpy.props.BoolProperty(
        name="Reset Pose Bones Between Actions",
        description=(
            "Reset pose bones between each action exported. This is needed "
            "when some bones are not keyed on some animations"
        ),
        default=True,
    )

    #  Shape Keys Animation
    cbb_morph_animation: bpy.props.BoolProperty(
        name="Shape Key Animations",
        description="Export shape keys animations (morph targets)",
        default=True,
    )

    cbb_morph_reset_sk_data: bpy.props.BoolProperty(
        name="Reset Shape Keys Between Actions",
        description=(
            "Reset shape keys between each action exported. This is needed "
            "when some SK channels are not keyed on some animations"
        ),
        default=True,
    )

    #  Sampling Animations
    cbb_force_sampling: bpy.props.BoolProperty(
        name="Always Sample Animations",
        description="Apply sampling to all animations",
        default=True,
    )

    cbb_frame_step: bpy.props.IntProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        default=1,
        min=1,
        max=120,
    )

    cbb_sampling_interpolation_fallback: bpy.props.EnumProperty(
        name="Sampling Interpolation Fallback",
        items=(
            (
                "LINEAR",
                "Linear",
                "Linear interpolation between keyframes.",
            ),
            (
                "STEP",
                "Step",
                "No interpolation between keyframes.",
            ),
        ),
        description="Interpolation fallback for sampled animations, when the property is not keyed",
        default="LINEAR",
    )
    #  Optimize Animations
    cbb_optimize_animation_size: bpy.props.BoolProperty(
        name="Optimize Animation Size",
        description="Reduce exported file size by removing duplicate keyframes",
        default=True,
    )

    cbb_optimize_animation_keep_anim_armature: bpy.props.BoolProperty(
        name="Force Keeping Channels for Bones",
        description=(
            "If all keyframes are identical in a rig, force keeping the minimal animation. "
            "When off, all possible channels for the bones will be exported, even if empty"
        ),
        default=True,
    )

    cbb_optimize_animation_keep_anim_object: bpy.props.BoolProperty(
        name="Force Keeping Channel for Objects",
        description=(
            "If all keyframes are identical for object transformations, "
            "force keeping the minimal animation"
        ),
        default=False,
    )

    cbb_optimize_disable_viewport: bpy.props.BoolProperty(
        name="Disable Viewport for Other Objects",
        description=(
            "When exporting animations, disable viewport for other objects, "
            "for performance"
        ),
        default=False,
    )


class CBB_PG_networking_settings(bpy.types.PropertyGroup):
    cbb_port: bpy.props.IntProperty(
        name="Port",
        description="Port number used for communicating with Cascadeur",
        default=53145,
        min=0,
        max=65535,
    )


class CBB_PG_settings(bpy.types.PropertyGroup):
    cascadeur_to_blender: bpy.props.PointerProperty(
        type=CBB_PG_cascadeur_to_blender,
    )

    blender_to_cascadeur: bpy.props.PointerProperty(
        type=CBB_PG_blender_to_cascadeur,
    )

    cascadeur_fbx_import: bpy.props.PointerProperty(
        type=CBB_PG_cascadeur_fbx_import_settings,
    )

    cascadeur_fbx_export: bpy.props.PointerProperty(
        type=CBB_PG_cascadeur_fbx_export_settings,
    )

    cascadeur_glb_import: bpy.props.PointerProperty(
        type=CBB_PG_cascadeur_glb_import_settings
    )

    cascadeur_glb_export: bpy.props.PointerProperty(
        type=CBB_PG_cascadeur_glb_export_settings
    )

    blender_fbx_import: bpy.props.PointerProperty(
        type=CBB_PG_blender_fbx_import_settings,
    )

    blender_fbx_export: bpy.props.PointerProperty(
        type=CBB_PG_blender_fbx_export_settings,
    )

    blender_glb_import: bpy.props.PointerProperty(
        type=CBB_PG_blender_glb_import_settings
    )

    blender_glb_export: bpy.props.PointerProperty(
        type=CBB_PG_blender_glb_export_settings
    )

    network: bpy.props.PointerProperty(
        type=CBB_PG_networking_settings,
    )


PROPERTY_GROUPS = (
    CBB_PG_cascadeur_to_blender,
    CBB_PG_blender_to_cascadeur,
    CBB_PG_cascadeur_fbx_import_settings,
    CBB_PG_cascadeur_fbx_export_settings,
    CBB_PG_cascadeur_glb_import_settings,
    CBB_PG_cascadeur_glb_export_settings,
    CBB_PG_blender_fbx_import_settings,
    CBB_PG_blender_fbx_export_settings,
    CBB_PG_blender_glb_import_settings,
    CBB_PG_blender_glb_export_settings,
    CBB_PG_networking_settings,
    # Parent property group. Should be registered last:
    CBB_PG_settings,
)


def register_props():
    for cls in PROPERTY_GROUPS:
        bpy.utils.register_class(cls)

    bpy.types.Scene.cbb_settings = bpy.props.PointerProperty(
        type=CBB_PG_settings,
    )


def unregister_props():
    del bpy.types.Scene.cbb_settings

    for cls in reversed(PROPERTY_GROUPS):
        bpy.utils.unregister_class(cls)
