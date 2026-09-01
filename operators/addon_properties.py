import bpy
from ..utils import config_handling


def generate_items(options: list) -> list:
    return [(option, option, "") for option in options]


class CBB_PG_cascadeur_to_blender(bpy.types.PropertyGroup):
    cbb_file_format: bpy.props.EnumProperty(
        items=generate_items(["fbx", "glb"]),
        name="File Format",
        description="Fileformat used for Cascadeur to Blender transfer",
        default="fbx",
    )


class CBB_PG_blender_to_cascadeur(bpy.types.PropertyGroup):
    cbb_file_format: bpy.props.EnumProperty(
        items=generate_items(["fbx", "glb"]),
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
        items=generate_items(["Y", "Z"]),
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
        items=generate_items(["Y", "Z"]),
        name="Up Axis",
        description="Up Axis when exporting from Cascadeur",
        default="Y",
    )

    cbb_csc_bake_animation: bpy.props.BoolProperty(
        name="Bake animation",
        description="Key all frames when exporting from Cascadeur",
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
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Forward",
        description="Forward Axis",
        default="-Z",
    )

    cbb_axis_up: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
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
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Primary Bone Axis",
        description="",
        default="Y",
    )

    cbb_secondary_bone_axis: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
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
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Forward",
        description="Forward Axis",
        default="-Z",
    )

    cbb_axis_up: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
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
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Primary Bone Axis",
        description="",
        default="Y",
    )

    cbb_secondary_bone_axis: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
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

    blender_fbx_import: bpy.props.PointerProperty(
        type=CBB_PG_blender_fbx_import_settings,
    )

    blender_fbx_export: bpy.props.PointerProperty(
        type=CBB_PG_blender_fbx_export_settings,
    )

    network: bpy.props.PointerProperty(
        type=CBB_PG_networking_settings,
    )


PROPERTY_GROUPS = (
    CBB_PG_cascadeur_to_blender,
    CBB_PG_blender_to_cascadeur,
    CBB_PG_cascadeur_fbx_import_settings,
    CBB_PG_cascadeur_fbx_export_settings,
    CBB_PG_blender_fbx_import_settings,
    CBB_PG_blender_fbx_export_settings,
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


def get_csc_fbx_settings(direction: str) -> dict:
    settings = {}

    if direction == "export":
        addon_props = bpy.context.scene.cbb_settings.cascadeur_fbx_export
    elif direction == "import":
        addon_props = bpy.context.scene.cbb_settings.cascadeur_fbx_import
    else:
        raise ValueError(f"Invalid FBX direction: {direction}")

    settings["selected_interval"] = addon_props.cbb_csc_import_selected
    settings["euler_filter"] = addon_props.cbb_csc_apply_euler_filter
    settings["up_axis"] = addon_props.cbb_csc_up_axis
    settings["bake_animation"] = addon_props.cbb_csc_bake_animation
    return settings
