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


################


class CBB_OT_cascadeur_to_blender_settings(bpy.types.Operator):
    bl_idname = "cbb.cascadeur_to_blender_settings"
    bl_label = "FBX Settings"
    bl_options = {"UNDO"}
    bl_description = "Open the Cascadeur Bridge add-on preferences"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self,
            title="Settings for Cascadeur to Blender file transfer",
            confirm_text="Save Settings",
            cancel_default=False,
            width=600,
        )

    def draw(self, context):
        addon_props = context.scene.cbb_fbx_settings
        layout = self.layout

        layout.prop(addon_props, "cbb_file_format")

        # Two main columns
        row = layout.row(align=True)

        # ---------------------------------------------------------
        # Cascadeur Export
        # ---------------------------------------------------------
        left = row.column(align=True)

        box = left.box()
        box.label(text="Cascadeur Export", icon="EXPORT")

        col = box.column(align=True)
        col.prop(addon_props, "cbb_csc_apply_euler_filter")
        col.prop(addon_props, "cbb_csc_up_axis")
        col.prop(addon_props, "cbb_csc_bake_animation")

        # ---------------------------------------------------------
        # Blender Import
        # ---------------------------------------------------------
        right = row.column(align=True)

        box = right.box()
        box.label(text="Blender Import", icon="IMPORT")

        subbox = box.box()
        subbox.label(text="Transform")
        col = subbox.column(align=True)
        col.prop(addon_props, "cbb_import_global_scale")
        col.prop(addon_props, "cbb_import_apply_transform")
        col.prop(addon_props, "cbb_import_manual_orientation")
        col.prop(addon_props, "cbb_import_axis_forward")
        col.prop(addon_props, "cbb_import_axis_up")

        subbox = box.box()
        subbox.label(text="Animation")
        col = subbox.column(align=True)
        col.prop(addon_props, "cbb_import_use_anim")
        col.prop(addon_props, "cbb_import_anim_offset")

        subbox = box.box()
        subbox.label(text="Armature")
        col = subbox.column(align=True)
        col.prop(addon_props, "cbb_import_ignore_leaf_bones")
        col.prop(addon_props, "cbb_import_force_connect_children")
        col.prop(addon_props, "cbb_import_automatic_bone_orientation")
        col.prop(addon_props, "cbb_import_primary_bone_axis")
        col.prop(addon_props, "cbb_import_secondary_bone_axis")
        col.prop(addon_props, "cbb_import_use_prepost_rot")

        # ---------------------------------------------------------
        # Settings buttons
        # ---------------------------------------------------------
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

    def execute(self, context):
        return {"FINISHED"}
