import bpy
from ..utils.csc_handling import CascadeurHandler
from ..utils.config_handling import get_panel_name
from .. import addon_info


class PanelBasics:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = get_panel_name()


class CBB_PT_parent_panel(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_parent"
    bl_label = "Cascadeur Bridge"

    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self, context):
        _ch = CascadeurHandler()
        addon_props = context.scene.cbb_fbx_settings
        layout = self.layout

        if not self._draw_verification(layout, _ch):
            return

        if self._draw_operation_status(layout):
            return

        self._draw_cascadeur_controls(layout)
        self._draw_blender_to_cascadeur(layout, addon_props)
        self._draw_cascadeur_to_blender(layout, addon_props)

    def _draw_verification(self, layout, cascadeur_handler):
        errors = []

        if not cascadeur_handler.is_csc_exe_path_valid:
            errors.append("- No valid Cascadeur exe path set in preferences!")

        if not cascadeur_handler.is_csc_bridge_installed:
            errors.append("- Cascadeur side of the add-on is not installed!")

        if not errors:
            return True

        box = layout.box()

        box.label(
            text="Cascadeur Bridge is not ready:",
            icon="ERROR",
        )

        col = box.column()
        for error in errors:
            col.label(text=error)

        box.separator(type="LINE")

        row = box.row()
        row.alert = True
        row.operator(
            "cbb.open_preferences",
            text="Open Preferences",
            icon="PREFERENCES",
        )

        return False

    def _draw_cascadeur_controls(self, layout):
        col = layout.column()

        row = col.row()
        row.operator(
            "cbb.start_cascadeur",
            text="Start Cascadeur",
            icon="MESH_UVSPHERE",
        )
        row.scale_y = 1.5

        col.separator()

    def _draw_operation_status(self, layout):
        if not addon_info.operation_completed:
            col = layout.column()
            col.label(icon="LOCKED", text="Operation in progress!")
            return True
        else:
            return False

    def _draw_blender_to_cascadeur(self, layout, addon_props):
        box = layout.box()
        col = box.column()

        row = col.row()
        row.label(text="Blender > Cascadeur")
        row.scale_y = 1.2

        row = col.row()
        row.prop(addon_props, "cbb_import_methods")
        row.scale_y = 1.2

        row = col.row()
        row.operator(
            "cbb.export_blender_fbx",
            text="Export To Cascadeur",
            icon="EXPORT",
        )

    def _draw_cascadeur_to_blender(self, layout, addon_props):
        box = layout.box()
        col = box.column(align=True)

        row = col.row()
        row.label(text="Cascadeur > Blender")
        row.scale_y = 1.2

        row = col.row()
        row.prop(addon_props, "cbb_export_methods")

        self._draw_import_actions(col)
        self._draw_batch_import(col)

    def _draw_import_actions(self, layout):
        props = layout.operator(
            "cbb.import_cascadeur_action",
            text="Import Action",
            icon="ARMATURE_DATA",
        )
        props.batch_export = False

        props = layout.operator(
            "cbb.import_cascadeur_fbx",
            text="Import Scene",
            icon="IMPORT",
        )
        props.batch_export = False

    def _draw_batch_import(self, layout):
        layout.separator()
        layout.label(text="Batch Import")

        props = layout.operator(
            "cbb.import_cascadeur_action",
            text="Import All Actions",
            icon="CON_ARMATURE",
        )
        props.batch_export = True

        props = layout.operator(
            "cbb.import_cascadeur_fbx",
            text="Import All Scenes",
            icon="DOCUMENTS",
        )
        props.batch_export = True
