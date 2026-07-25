if "bpy" not in locals():
    from . import fbx_transfer
    from . import cascadeur
    from . import addon_properties
    from . import preferences
else:
    import importlib

    importlib.reload(fbx_transfer)
    importlib.reload(cascadeur)
    importlib.reload(addon_properties)
    importlib.reload(preferences)

classes = [
    fbx_transfer.CBB_OT_export_blender_fbx,
    fbx_transfer.CBB_OT_import_cascadeur_fbx,
    fbx_transfer.CBB_OT_import_action_to_selected,
    cascadeur.CBB_OT_start_cascadeur,
    preferences.CBB_OT_install_required_files,
    preferences.CBB_OT_add_cascadeur_asset_library,
    addon_properties.CBB_OT_save_fbx_settings,
    addon_properties.CBB_OT_reset_fbx_settings,
    addon_properties.CBB_OT_save_port_number,
]
