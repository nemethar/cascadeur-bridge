import bpy
from .. import icons
from .main_panel import PanelBasics


class CBB_PT_csc_bridge_arp_wrapper(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_bridge_arp_wrapper"
    bl_label = "Auto Rig Pro Wrapper"
    bl_parent_id = "CBB_PT_parent"

    @classmethod
    def poll(cls, context):
        # Only show this panel when Auto-Rig Pro is enabled
        # and its FBX exporter is registered.
        return (
            "bl_ext.user_default.auto_rig_pro" in context.preferences.addons
            and hasattr(bpy.ops.arp, "arp_export_fbx_panel")
        )

    def draw_header(self, context):
        self.layout.label(text="", icon="ARMATURE_DATA")

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # FBX
        row = col.row(align=True)
        op = row.operator(
            "cbb.export_arp_fbx",
            text="Export FBX...",
            icon_value=icons.get_icon_id("arp-export"),
        )
        op.arp_quick_export = False

        op = row.operator(
            "cbb.export_arp_fbx",
            text="",
            icon_value=icons.get_icon_id("arp-quick-export"),
        )
        op.arp_quick_export = True

        # GLB
        row = col.row(align=True)
        op = row.operator(
            "cbb.export_arp_glb",
            text="Export GLB...",
            icon_value=icons.get_icon_id("arp-export"),
        )
        op.arp_quick_export = False

        op = row.operator(
            "cbb.export_arp_glb",
            text="",
            icon_value=icons.get_icon_id("arp-quick-export"),
        )
        op.arp_quick_export = True

        addon_props = context.scene.cbb_settings
        col.prop(addon_props.blender_to_cascadeur, "cbb_delete_arp_export")

        # Notes
        header, panel = layout.panel(
            "cbb_arp_export_info",
            default_closed=True,
        )

        header.label(
            text="Notes",
            icon="INFO",
        )

        if panel:
            col = panel.column(align=True)

            col.label(
                text="Auto-Rig Pro integration is currently in alpha.",
                icon="ERROR",
            )

            col.separator()

            col.label(
                text="Cascadeur import settings are configured",
            )
            col.label(
                text="in the Blender > Cascadeur section.",
            )
