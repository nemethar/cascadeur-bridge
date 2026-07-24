if "bpy" not in locals():
    from . import operators
    from . import ui
else:
    import importlib

    importlib.reload(operators)
    importlib.reload(ui)

import bpy

from .utils import config_handling
from .utils.csc_handling import get_default_csc_exe_path
from .addon_info import ASSET_LIB_NAME


def update_all_tab_names(self, context) -> None:
    try:
        # Unregister everything
        for c in ui.classes:
            bpy.utils.unregister_class(c)
    except:
        pass

    # Set panel name for base class
    new_name = bpy.context.preferences.addons[__package__].preferences.csc_tab_name
    ui.main_panel.PanelBasics.bl_category = new_name
    # Save to file
    config_handling.set_config_parameter("Addon Settings", "panel_name", new_name)

    # Register everything
    for c in ui.classes:
        bpy.utils.register_class(c)


class CBB_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    csc_exe_path: bpy.props.StringProperty(
        name="Cascadeur executable",
        subtype="FILE_PATH",
        default=get_default_csc_exe_path(),
    )

    csc_tab_name: bpy.props.StringProperty(
        name="N Panel Name",
        description="Name of the add-on on the N Panel",
        default=config_handling.get_panel_name(),
        update=update_all_tab_names,
    )

    csc_asset_lib_name: bpy.props.StringProperty(
            name="Asset library name",
            description="Name of the asset library with the Cascadeur Sample Scenes",
            default=ASSET_LIB_NAME,
        )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=False)
        row = col.row()
        row.prop(self, "csc_tab_name")
        col.separator()
        row = col.row()
        row.prop(self, "csc_exe_path")
        row = col.row()
        row.operator(
            "cbb.install_required_files",
            text="Install Requirements",
            icon="MODIFIER",
        )
        col.separator()
        row = col.row()
        row.prop(self, "csc_asset_lib_name")
        row.operator(
            "cbb.setup_asset_library",
            text="Add Cascadeur Asset Library",
            icon="ASSET_MANAGER",
        )


classes = [CBB_preferences] + operators.classes + ui.classes


def register():
    operators.addon_properties.register_props()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    operators.addon_properties.unregister_props()
    for cls in classes:
        bpy.utils.unregister_class(cls)
