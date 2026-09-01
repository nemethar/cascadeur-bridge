if "bpy" not in locals():
    from . import fbx_transfer
    from . import cascadeur
    from . import addon_properties
    from . import preferences
    from . import settings
    from . import free_version_handling
else:
    import importlib

    importlib.reload(fbx_transfer)
    importlib.reload(cascadeur)
    importlib.reload(addon_properties)
    importlib.reload(preferences)
    importlib.reload(settings)
    importlib.reload(free_version_handling)

classes = [
    fbx_transfer.CBB_OT_export_blender_fbx,
    fbx_transfer.CBB_OT_import_cascadeur_fbx,
    fbx_transfer.CBB_OT_import_action_to_selected,
    cascadeur.CBB_OT_start_cascadeur,
    preferences.CBB_OT_install_required_files,
    preferences.CBB_OT_add_cascadeur_asset_library,
    preferences.CBB_OT_open_preferences,
    settings.CBB_OT_cascadeur_to_blender_settings,
    settings.CBB_OT_blender_to_cascadeur_settings,
    settings.CBB_OT_reset_settings,
    settings.CBB_OT_save_port_number,
    free_version_handling.CBB_OT_license_required_popup,
    free_version_handling.CBB_OT_copy_discount_code,
]
