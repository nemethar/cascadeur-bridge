if "bpy" not in locals():
    from . import operators
    from . import ui
    from . import icons
else:
    import importlib

    importlib.reload(operators)
    importlib.reload(ui)
    importlib.reload(icons)

import bpy
import os

from .utils import config_handling
from .utils.csc_handling import get_default_csc_exe_path, CascadeurHandler
from .addon_info import DEFAULT_ASSET_LIB_NAME


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
        default=DEFAULT_ASSET_LIB_NAME,
    )

    def draw(self, context):
        _ch = CascadeurHandler()
        layout = self.layout
        col = layout.column(align=False)
        col.prop(self, "csc_tab_name")

        col.separator(type="SPACE", factor=1.5)

        box = col.box()

        row = box.row()
        row.label(icon="MODIFIER", text="Cascadeur Setup")

        row = box.row()
        row.alert = not _ch.is_csc_exe_path_valid
        row.prop(self, "csc_exe_path")

        row = box.row()
        box.separator(type="LINE")

        row = box.row()
        row.label(text="Cascadeur Scripts")
        row = box.row()
        if _ch.is_csc_bridge_installed:
            row.label(icon="CHECKMARK", text="Cascadeur scripts are already installed.")
        else:
            row.label(
                icon="INFO",
                text="The Bridge requires additional scripts to be copied to your Cascadeur install folder.",
            )

        row = box.row()
        row.alert = not _ch.is_csc_bridge_installed
        row.operator(
            "cbb.install_required_files",
            text="Install Automatically",
            icon="MODIFIER",
        )
        row = box.row()
        row.label(
            text="or",
        )

        # Manual installation guide
        header, panel = box.panel("cbb_manual_install", default_closed=True)

        header.label(text="Install Manually:")

        if panel:
            source_path = os.path.join(addon_info.ADDON_PATH, "csc_files")
            target_path = _ch.commands_path

            row = panel.row()
            row.label(
                text="1. Copy the entire blender_bridge folder from the add-on's directory:"
            )
            row = panel.row()
            row.operator("wm.path_open", text="", icon="FILE_FOLDER").filepath = (
                source_path
            )

            row = panel.row()
            row.label(
                text="2. Paste the blender_bridge folder to the Cascadeur scripts folder:"
            )
            row = panel.row()
            if target_path:
                row.operator("wm.path_open", text="", icon="FILE_FOLDER").filepath = (
                    target_path
                )
            else:
                row.label(text=" Please enter a valid Cascadeur executable path first!")

            panel.label(text="3. Restart Cascadeur")

        col.separator(type="SPACE", factor=1.5)

        if bpy.app.version >= (5, 2, 0):
            # Remote asset library settings (only available from Blender 5.2.0)
            box = col.box()
            box.label(icon="ASSET_MANAGER", text="Asset Library")
            row = box.row()
            row.prop(self, "csc_asset_lib_name", text="Name")
            row.operator(
                "cbb.add_cascadeur_asset_library",
                text="Add Cascadeur Asset Library",
            )


classes = [CBB_preferences] + operators.classes + ui.classes


def register():
    icons.register()
    operators.addon_properties.register_props()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.timers.register(config_handling.load_settings)


def unregister():
    icons.unregister()
    operators.addon_properties.unregister_props()
    for cls in classes:
        bpy.utils.unregister_class(cls)
