import bpy
from .. import icons
from ..operators.free_version_handling import CASCADEUR_AFFILIATE_URL
from .main_panel import PanelBasics


class CBB_PT_csc_bridge_info(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_bridge_info"
    bl_label = "Information"
    bl_parent_id = "CBB_PT_parent"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        row = column.row(align=True)
        row.scale_y = 1.2
        op = row.operator(
            "cbb.open_url",
            text="YouTube",
            icon_value=icons.get_icon_id("youtube"),
        )
        op.url = "https://youtu.be/0muo9EPIPSE"
        op.link_name = "YouTube"
        op.tooltip = "Tutorial video about this add-on"

        op = row.operator(
            "cbb.open_url",
            text="GitHub",
            icon_value=icons.get_icon_id("github"),
        )
        op.url = "https://github.com/nemethar/cascadeur-bridge/"
        op.link_name = "GitHub"
        op.tooltip = "The add-ons main github page"

        column.separator()
        row = column.row()
        row.scale_y = 1.2
        op = row.operator(
            "cbb.open_url",
            text="Get Cascadeur (Affiliate)",
            icon_value=icons.get_icon_id("cascadeur"),
        )
        op.url = CASCADEUR_AFFILIATE_URL
        op.link_name = "Cascadeur"
        op.tooltip = (
            "Purchasing through this link supports the development of Cascadeur Bridge"
        )


class CBB_OT_open_url(bpy.types.Operator):
    bl_idname = "cbb.open_url"
    bl_label = "Open URL"

    url: bpy.props.StringProperty()
    link_name: bpy.props.StringProperty(default="")
    tooltip: bpy.props.StringProperty(default="")

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def execute(self, context):
        if bpy.app.online_access:
            bpy.ops.wm.url_open(url=self.url)
        else:
            context.window_manager.clipboard = self.url
            self.report(
                {"INFO"},
                f"Online access is disabled in Preferences. "
                f"The {self.link_name} link was copied to your clipboard.",
            )

        return {"FINISHED"}
