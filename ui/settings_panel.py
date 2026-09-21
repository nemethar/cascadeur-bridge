import bpy
from .main_panel import PanelBasics


class CBB_PT_csc_bridge_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_bridge_settings"
    bl_label = "Advnaced Settings"
    bl_parent_id = "CBB_PT_parent"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="SETTINGS")

    def draw(self, context):
        addon_props = context.scene.cbb_settings
        layout = self.layout
        box = layout.box()
        box.label(text="Port")
        row = box.row()
        row.prop(addon_props.network, "cbb_port")
        row.operator(
            "cbb.save_port_settings",
            text="Save",
            icon="FAKE_USER_ON",
        )
