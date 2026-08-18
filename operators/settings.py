import bpy
from ..ui.cascadeur_to_blender_settings import draw_cascadeur_to_blender_settings
from ..ui.blender_to_cascadeur_settings import draw_blender_to_cascadeur_settings


class CBB_OT_cascadeur_to_blender_settings(bpy.types.Operator):
    bl_idname = "cbb.cascadeur_to_blender_settings"
    bl_label = "Cascadeur to Blender"
    bl_options = {"UNDO"}
    bl_description = "Settings for file transfer from Cascadeur to Blender"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self,
            title="Settings for Cascadeur to Blender file transfer",
            confirm_text="Save Settings",
            cancel_default=False,
            width=600,
        )

    def draw(self, context):
        draw_cascadeur_to_blender_settings(self.layout, context)

    def execute(self, context):
        # Save Cascadeur to Blender settings here
        return {"FINISHED"}


class CBB_OT_blender_to_cascadeur_settings(bpy.types.Operator):
    bl_idname = "cbb.blender_to_cascadeur_settings"
    bl_label = "Blender to Cascadeur"
    bl_options = {"UNDO"}
    bl_description = "Settings for file transfer from Blender to Cascadeur"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self,
            title="Settings for Blender to Cascadeur file transfer",
            confirm_text="Save Settings",
            cancel_default=False,
            width=650,
        )

    def draw(self, context):
        draw_blender_to_cascadeur_settings(self.layout, context)

    def execute(self, context):
        # Save Blender to Cascadeur settings here
        return {"FINISHED"}
