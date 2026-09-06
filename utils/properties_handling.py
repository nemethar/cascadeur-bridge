import bpy


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


def get_csc_glb_settings(direction: str) -> dict:
    settings = {}

    if direction == "export":
        addon_props = bpy.context.scene.cbb_settings.cascadeur_glb_export

        settings["call_process_skinned_mesh"] = (
            addon_props.cbb_call_process_skinned_mesh
        )
        settings["rotate_meshes_primitive_attributes"] = (
            addon_props.cbb_rotate_meshes_primitive_attributes
        )
        settings["scale_meshes_primitive_attributes"] = (
            addon_props.cbb_scale_meshes_primitive_attributes
        )
        settings["translate_meshes_primitive_attributes"] = (
            addon_props.cbb_translate_meshes_primitive_attributes
        )
    elif direction == "import":
        addon_props = bpy.context.scene.cbb_settings.cascadeur_glb_import

        settings["adjust_meshes_rotation"] = addon_props.cbb_adjust_meshes_rotations
        settings["ignore_mesh_transform"] = addon_props.cbb_ignore_mesh_transform
        settings["include_objects"] = addon_props.cbb_include_objects
        settings["is_update_mode"] = addon_props.cbb_is_update_mode
        settings["move_meshes_to_root"] = addon_props.cbb_move_meshes_to_root
    else:
        raise ValueError(f"Invalid GLB direction: {direction}")

    settings["for_selected_interval"] = addon_props.cbb_for_selected_interval
    settings["for_selected_objects"] = addon_props.cbb_for_selected_objects
    settings["include_animation"] = addon_props.cbb_include_animation
    if addon_props.cbb_use_scale_factor:
        settings["scale_factor"] = addon_props.cbb_scale_factor
    else:
        settings["scale_factor"] = None
    return settings


GLB_EXPORT_PRESETS = {
    "ANIMATION": {
        "cbb_for_selected_interval": False,
        "cbb_for_selected_objects": False,
        "cbb_include_animation": True,
    },
    "MODEL": {
        "cbb_for_selected_interval": False,
        "cbb_for_selected_objects": False,
        "cbb_include_animation": False,
    },
    "SCENE": {
        "cbb_for_selected_interval": False,
        "cbb_for_selected_objects": False,
        "cbb_include_animation": True,
    },
    "SCENE_SELECTED_OBJECTS": {
        "cbb_for_selected_interval": False,
        "cbb_for_selected_objects": True,
        "cbb_include_animation": True,
    },
}
GLB_IMPORT_PRESETS = {
    "ADD_MODEL": {
        "cbb_is_update_mode": True,
        "cbb_for_selected_objects": False,
        "cbb_for_selected_interval": False,
        "cbb_include_animation": False,
        "cbb_include_objects": True,
    },
    "ADD_MODEL_SELECTED": {
        "cbb_is_update_mode": True,
        "cbb_for_selected_objects": True,
        "cbb_for_selected_interval": False,
        "cbb_include_animation": False,
        "cbb_include_objects": True,
    },
    "ANIMATION": {
        "cbb_is_update_mode": True,
        "cbb_for_selected_objects": False,
        "cbb_for_selected_interval": False,
        "cbb_include_animation": True,
        "cbb_include_objects": False,
    },
    "ANIMATION_SELECTED_FRAMES": {
        "cbb_is_update_mode": True,
        "cbb_for_selected_objects": False,
        "cbb_for_selected_interval": True,
        "cbb_include_animation": True,
        "cbb_include_objects": False,
    },
    "ANIMATION_SELECTED_OBJECTS": {
        "cbb_is_update_mode": True,
        "cbb_for_selected_objects": True,
        "cbb_for_selected_interval": False,
        "cbb_include_animation": True,
        "cbb_include_objects": False,
    },
    "MODEL": {
        "cbb_is_update_mode": False,
        "cbb_for_selected_objects": False,
        "cbb_for_selected_interval": False,
        "cbb_include_animation": False,
        "cbb_include_objects": True,
    },
    "SCENE": {
        "cbb_is_update_mode": False,
        "cbb_for_selected_objects": False,
        "cbb_for_selected_interval": False,
        "cbb_include_animation": True,
        "cbb_include_objects": True,
    },
}


def apply_preset(settings, preset):
    for property_name, value in preset.items():
        setattr(settings, property_name, value)
