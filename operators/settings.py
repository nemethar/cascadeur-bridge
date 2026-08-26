import bpy
from ..ui.cascadeur_to_blender_settings import draw_cascadeur_to_blender_settings
from ..ui.blender_to_cascadeur_settings import draw_blender_to_cascadeur_settings
from ..utils import config_handling

TRANSFER_PROPERTY_GROUPS = {
    "CASCADEUR_TO_BLENDER": [
        "cascadeur_to_blender",
        "cascadeur_fbx_export",
        "blender_fbx_import",
    ],
    "BLENDER_TO_CASCADEUR": [
        "blender_to_cascadeur",
        "blender_fbx_export",
        "cascadeur_fbx_import",
    ],
}


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
        if not config_handling.save_settings(
            TRANSFER_PROPERTY_GROUPS["CASCADEUR_TO_BLENDER"]
        ):
            self.report({"ERROR"}, "Failed to save settings.")
            return {"CANCELLED"}
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
        if not config_handling.save_settings(
            TRANSFER_PROPERTY_GROUPS["BLENDER_TO_CASCADEUR"]
        ):
            self.report({"ERROR"}, "Failed to save settings.")
            return {"CANCELLED"}
        return {"FINISHED"}


class CBB_OT_reset_settings(bpy.types.Operator):
    """Reset the corresponding settings"""

    bl_idname = "cbb.reset_settings"
    bl_label = "Reset Settings"

    reset_group: bpy.props.EnumProperty(
        name="Settings",
        items=[
            (
                "CASCADEUR_TO_BLENDER",
                "Cascadeur to Blender",
                "Reset settings for Cascadeur to Blender",
            ),
            (
                "BLENDER_TO_CASCADEUR",
                "Blender to Cascadeur",
                "Reset settings for Blender to Cascadeur",
            ),
        ],
    )

    def execute(self, context):
        try:
            groups = TRANSFER_PROPERTY_GROUPS[self.reset_group]
            config_handling.reset_settings(groups)

            # Update UI panel:
            bpy.context.area.tag_redraw()
        except Exception as e:
            self.report({"ERROR"}, f"Couldn't reset settings: {e}")
            return {"CANCELLED"}
        self.report({"INFO"}, "Settings reset")
        return {"FINISHED"}


class CBB_OT_save_port_number(bpy.types.Operator):
    """Save port settings for Cascadeur and Blender"""

    bl_idname = "cbb.save_port_settings"
    bl_label = "Save Port"

    def execute(self, context):
        result = config_handling.save_port_number()

        if not result:
            self.report(
                {"ERROR"}, "You don't have permission to write the config file."
            )
            self.report({"INFO"}, "Restart Blender as Admin and try again")
            return {"CANCELLED"}
        self.report({"INFO"}, "Settings saved")
        return {"FINISHED"}
