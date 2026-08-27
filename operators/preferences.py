import bpy
import os

from .. import addon_info
from ..utils import file_handling
from ..utils.csc_handling import CascadeurHandler


class CBB_OT_install_required_files(bpy.types.Operator):
    """Copy the necessary python script to Cascadeurs folder"""

    bl_idname = "cbb.install_required_files"
    bl_label = "Install Required Files"

    @classmethod
    def poll(cls, context):
        return CascadeurHandler().is_csc_exe_path_valid

    def execute(self, context):
        ch = CascadeurHandler()
        # Copy scripts
        commands_source = os.path.join(
            addon_info.ADDON_PATH, "csc_files", "blender_bridge"
        )
        commands_path = os.path.join(ch.commands_path, "blender_bridge")
        if not file_handling.path_exists(commands_path):
            self.report(
                {"ERROR"},
                "Cascadeur scripts folder not found. Make sure Cascadeur 2026.2 or newer is installed.",
            )
            return {"CANCELLED"}
        result = file_handling.copy_files(
            commands_source, commands_path, os.listdir(commands_source)
        )
        if not result:
            self.report(
                {"ERROR"}, "You don't have permission to copy the files for Cascadeur"
            )
            self.report(
                {"INFO"},
                "Check the Manual Installation Guide or Restart Blender as Admin and try again",
            )
            return {"CANCELLED"}
        self.report({"INFO"}, "All necessary files have been successfully copied")
        return {"FINISHED"}


class CBB_OT_add_cascadeur_asset_library(bpy.types.Operator):
    """Add the Cascadeur asset library to Blender"""

    bl_idname = "cbb.add_cascadeur_asset_library"
    bl_label = "Add Cascadeur Asset Library"

    def execute(self, context):
        addon_prefs = context.preferences.addons[addon_info.PACKAGE_NAME].preferences
        asset_lib_name = addon_prefs.csc_asset_lib_name
        asset_lib_url = addon_info.ASSET_LIB_URL

        asset_libraries = context.preferences.filepaths.asset_libraries

        # Check if asset library with the same name already exists
        if asset_lib_name in asset_libraries:
            self.report(
                {"ERROR"},
                f"There is already an asset library with the name {asset_lib_name}",
            )
            return {"CANCELLED"}

        # Add the remote asset library
        try:
            bpy.ops.preferences.asset_library_add(
                name=asset_lib_name,
                remote_url=asset_lib_url,
                type="REMOTE",
            )
        except Exception as e:
            self.report({"ERROR"}, f"Failed to add asset library: {e}")
            return {"CANCELLED"}

        # Change import method
        lib = asset_libraries[asset_lib_name]
        lib.import_method = "APPEND"

        self.report({"INFO"}, "Asset library added. Remember to save your preferences.")
        return {"FINISHED"}


class CBB_OT_open_preferences(bpy.types.Operator):
    bl_idname = "cbb.open_preferences"
    bl_label = "Open Cascadeur Bridge Preferences"
    bl_description = "Open the Cascadeur Bridge add-on preferences"

    def execute(self, context):
        bpy.ops.preferences.addon_show(module="bl_ext.user_default.cascadeur_bridge")
        return {"FINISHED"}
